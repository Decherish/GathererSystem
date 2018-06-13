# pythonDemo
爬取正方系统，将个人信息或者课表或者成绩录入数据库中
## 项目目的:
输入学号密码，模拟登录正方系统，并爬取学生个人信息和成绩和课程表保存至数据库
##项目环境：
* python版本:3.5;
* 数据库:mysql;
* 库包:requests、BeautifulSoup、pymysql、urllib、re、PIL；
* 数据库可视化工具:Navicat；浏
* 览器:Chrome；
* IDE:Pycharm
##项目开发：
* 数据库设计：按照给出的sql文件设计
首先用浏览器访问[正方系统](http://210.38.162.116/(wk5amj45g5b5dh55roqgh445)/default2.aspx)的网址，同时打开开发者工具，输入一次登录，观察Network捕获到的defau2.ajpx
![](https://github.com/Decherish/pythonDemo/raw/master/image/picture1.png)
根据Headers构造相应的表头和数据data
```python
headers = {
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    "Host": "210.38.162.116",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0"
}
data = {
        'TextBox1': username,
        'TextBox2' : password,
        'TextBox3' : ycode,
        '__VIEWSTATE' : __VIEWSTATE,
        'RadioButtonList1' : '%D1%A7%C9%FA',
        'Button1' : '',
        'lbLanguage' : '',
 }
```
RadioButtonList1的值为学生的gb2312解码
用request.get先请求一次网页的源码，发现其中有
<input type="hidden" name="__VIEWSTATE" value="dDwtMTg3MTM5OTI5MTs7PjJ06Q8x0sjwFTIugwoEgtaDQze7">
用soup解析并将相应的值填充至data
观察Network发现里面有Checkcode.aspx，这里使用第三库将验证码下载至本地在弹出
```python
imgresponse = s.get(imgUrl, stream=True)
image = imgresponse.content
DstDir = os.getcwd()+"\\"
print("保存验证码到："+DstDir+"code.jpg"+"\n")
try:
    with open(DstDir+"code.jpg" ,"wb") as jpg:
        jpg.write(image)
except IOError:
        print("IO Error\n")
finally:
        jpg.close
```
数据全部封装好后，首先开启一个Session,并获得相应的cookies，然后为header添加cookies，利用session提交post请求模拟登录
response = s.post(url,headers=headers,data=data)
<br>后面的操作就是模仿前面的样子，观察Network捕获的aspx，构造相应的表头和data，然后用session去post或者get
<br>返回的数据利用BeautifulSoup来解析，解析方式用"lxml"，想要的值通过find方法获取大概后再通过字符串截取来取得
