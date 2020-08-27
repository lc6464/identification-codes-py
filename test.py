print('preparing...')

from program import GetCode, headers
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import re, os

ele0 = ''
p = re.compile(r'(\d)[^0-9]*(\d)[^0-9]*(\d)[^0-9]*(\d)') # 验证码正则

getCode = GetCode('image%scode.png'%os.sep, 'http://chaxun.heyuanedu.cn:88/validatecode.php?act=getimg') # 实例化对象
getCode.getSession() # 获取 Session

userName = input('姓名：')
identity = input('准考证号：')

while ele0 == '': # 通过正则但错误
	result2 = None
	while result2 == None: # 无法通过正则  #time.sleep(0.2)
		print('Downloading...')
		getCode.download() # 下载验证码
		print('Identifying...')
		result = getCode.identify() # 识别
		result2 = ('%s%s%s%s'%p.search(result).groups() if p.search(result) != None else None) # 正则判断
		result0 = (result2 if result2 != None else result) if result != '' else 'failure!' # 识别结果
		print('Result: ' + result0)

	req = Request('http://chaxun.heyuanedu.cn:88/search.php', urlencode({ 'userName': userName, 'identity': identity, 'code': result0 }).encode(), headers, 'chaxun.heyuanedu.cn:88')
	res = urlopen(req) # 获取结果
	html = res.read().decode() # 获取结果  #print(res.headers) #print(html)
	soup = BeautifulSoup(html,'lxml') # 解析 html
	ele = soup.select('#printGrade') # 获取相应元素
	ele0 = str(ele)[1:-1] # 获取结果(str)
	print(ele0 if ele0 != '' else 'Error!')