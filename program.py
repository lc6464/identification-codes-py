from PIL import Image
import pytesseract, os
from urllib.request import urlopen, Request

headers = {
	'Referer': 'http://chaxun.heyuanedu.cn:88/',
	'Accept': 'text/html,image/webp,image/png,image/jpeg,*/*;q=0.8',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63',
}

class GetCode:
	def __init__(self, path, url=None, headers=headers, origin='chaxun.heyuanedu.cn:88', threshold=185): # 初始化对象实例
		self.path = path # 赋值变量
		self.url = url
		self.headers = headers
		self.origin = origin
		self.threshold = threshold

	def getReq(self, url=None, headers=None, origin='chaxun.heyuanedu.cn:88'): # 获取 Request 对象
		self.url = url if url != None else self.url # 赋值变量
		self.headers = headers if headers != None else self.headers
		self.origin = origin if origin != None else self.origin
		return Request(self.url, None, self.headers, self.origin) # 返回 Request 对象

	def setting(self, path=None, url=None, headers=None, origin=None, threshold=None): # 设置实例的各类变量
		self.path = path if path != None else self.path # 赋值变量
		self.url = url if url != None else self.url
		self.headers = headers if headers != None else self.headers
		self.origin = origin if origin != None else self.origin
		self.threshold = threshold if threshold != None else self.threshold

	def getSession(self, url=None, headers=None, origin=None): # 获取对应系统的 Session ，注意：请勿重复调用！否则将可能导致不可预知的问题！
		self.url = url if url != None else self.url # 赋值变量
		self.headers = headers if headers != None else self.headers
		self.origin = origin if origin != None else self.origin
		self.headers['Cookie'] = urlopen(self.getReq()).info()['Set-Cookie'].split(';')[0] # 写入 Cookie（无法处理多个 Cookies 的情况！如果重复调用也可能导致出现问题）（其实就是因为我懒）
		return self.headers # 返回 headers

	def download(self, url=None, path=None, headers=None, origin=None): # 下载验证码图片
		self.url = url if url != None else self.url # 赋值变量
		self.path = path if path != None else self.path
		self.headers = headers if headers != None else self.headers
		self.origin = origin if origin != None else self.origin
		if not os.path.exists(self.path[:self.path.rfind(os.sep)]): # 防止目录不存在出错
			os.mkdir(self.path[:self.path.rfind(os.sep)]) # 创建目录
		with open(self.path, 'wb') as f: # 开文件
			size = f.write(urlopen(self.getReq()).read()) # 写文件（图片）
		return size # 返回文件大小

	def identify(self, path=None, threshold=None): # 识别验证码
		self.path = path if path != None else self.path # 赋值变量
		self.threshold = threshold if threshold != None else self.threshold
		image = Image.open(self.path) # PIL 打开图片
		pixdata = image.load() # 载入图片到变量
		w, h = image.size # 获取宽高
		for y in range(h): # 处理色彩
			for x in range(w):
				if pixdata[x, y][0] < self.threshold and pixdata[x, y][1] < self.threshold and pixdata[x, y][2] < self.threshold:
					pixdata[x, y] = (0, 0, 0)
				else:
					pixdata[x, y] = (255, 255, 255)
		for y in range(1,h-1): # 处理干扰线
			for x in range(1,w-1):
				count = 0
				if pixdata[x,y-1][0] > 245:
					count = count + 1
				if pixdata[x,y+1][0] > 245:
					count = count + 1
				if pixdata[x-1,y][0] > 245:
					count = count + 1
				if pixdata[x+1,y][0] > 245:
					count = count + 1
				if count > 2:
					pixdata[x,y] = (255,255,255)
		image.save(self.path[:self.path.rfind(os.sep)+1] + 'code-Pretreatment.png') # 保存预处理图片（非必须，生产环境建议删除）
		return pytesseract.image_to_string(image, 'eng')