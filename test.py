print('preparing...')

from program import GetCode, headers
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import re, os

ele0 = ''
p = re.compile(r'(\d)[^0-9]*(\d)[^0-9]*(\d)[^0-9]*(\d)') # 此系统验证码正则

getCode = GetCode('image%scode.png'%os.sep, 'http://chaxun.heyuanedu.cn:88/validatecode.php?act=getimg') # 实例化对象
getCode.getSession() # 获取 Session

userName = input('姓名：')
identity = input('准考证号：')

while ele0 == '': # 识别通过正则但错误循环
	result2 = None
	while result2 == None: # 识别无法通过正则循环
		#time.sleep(0.2)
		print('Downloading...')
		getCode.download()
		print('Identifying...')
		result = getCode.identify()
		result2 = ('%s%s%s%s'%p.search(result).groups() if p.search(result) != None else None)
		result0 = (result2 if result2 != None else result) if result != '' else 'failure!'
		print('Result: ' + result0)

	req = Request('http://chaxun.heyuanedu.cn:88/search.php', urlencode({ 'userName': userName, 'identity': identity, 'code': result0 }).encode(), headers, 'chaxun.heyuanedu.cn:88')
	res = urlopen(req) # 获取结果
	html = res.read().decode()
	#print(res.headers)
	#print(html)
	soup = BeautifulSoup(html,'lxml') # 解析 html
	ele = soup.select('#printGrade')
	ele0 = str(ele)[1:-1]
	print(ele0 if ele0 != '' else 'Error!')