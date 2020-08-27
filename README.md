# 图形验证码识别系统
- 由 Python 编写
- 超级简单
- 不怎么靠谱
- 不建议用于生产环境

## 原理
- 使用 `PIL` 处理验证码图片
- 使用 ORC 方式识别验证码
  - `pytesseract`


## 文件
- `program.py`：程序文件
  - `class GetCode`
  - `dict headers`
  - 75行在生产环境下请删除或注释掉
- `test.py`：测试文件
  - 针对 [http://chaxun.heyuanedu.cn:88/](http://chaxun.heyuanedu.cn:88/ "http://chaxun.heyuanedu.cn:88/") 系统的测试
  - 靠运气和大量尝试来尝试验证码
  - 图片储存至 image/