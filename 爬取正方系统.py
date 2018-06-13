import os
import re
import bs4
import urllib
import pymysql
import requests
from PIL import Image
from urllib import parse
from bs4 import BeautifulSoup

'''
url为访问的网址，括号内值会改变
imagUrl为验证码的网址，括号内值会改变
username为登录名同时也是学号
password为密码
'''
s = requests.session()
url = "http://210.38.162.116/(wk5amj45g5b5dh55roqgh445)/default2.aspx"
imgUrl = "http://210.38.162.116/(wk5amj45g5b5dh55roqgh445)/CheckCode.aspx"
username = input("请输入你的学号：")
password = input("请输入你的密码：")
#headers为第一次post时使用的headers
headers = {
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    "Host": "210.38.162.116",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0"
}
#headers_codew为查询学生信息时使用的headers，为GET请求，其中referer十分重要，没有就会被弹出
headers_code ={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36",
    "Referer": "http://210.38.162.116/(wk5amj45g5b5dh55roqgh445)/xs_main.aspx?xh="+username,
    "Host": "210.38.162.116",
    "Cache-Control": "max-age=0"
}
#headers_code2为查询课表或者成绩时使用的headers，为POST请求，其中referer十分重要，没有就会被弹出
headers_code2 = {
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Referer": "",
    "Host": "210.38.162.116",
    "Origin": "http://210.38.162.116",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0"
}
#根据用户输入的选择来填充相应的二次请求网址，同时补全headers_code2内的数据
def get_headers(action,username,name):
    if( action == '学生信息录入' or action == '1'):
        acion = 'xsgrxx'
    elif(action == '学生课表录入' or action == '2'):
        acion = 'xskbcx'
    elif(action == '学生成绩查询' or action  == '3'):
        acion = 'xscjcx'
    else:
        print("输入指令有误")
    headers_code2['Referer'] = "http://210.38.162.116/(wk5amj45g5b5dh55roqgh445)/" + acion + ".aspx?xh=" + username + "&xm="+name+"&gnmkdm=N121603"
    kburl = "http://210.38.162.116/(wk5amj45g5b5dh55roqgh445)/"+acion+".aspx?xh=" + username + "&xm="+name+"&gnmkdm=N121603"
    return kburl
'''
获得第一次登录时需要的数据，其中__VIEWSTATE需要先用get请求网页源码在解析获得，
验证码则需下载至本地后输入
'''
def get_post_date(url,username,password):
    re = s.get(url)
    soup = bs4.BeautifulSoup(re.text,'lxml')
    __VIEWSTATE = soup.find('input',attrs={'name': '__VIEWSTATE'})['value']
    cookies = requests.utils.dict_from_cookiejar(s.cookies)
    headers.update(cookies)
    headers_code.update(cookies)
    headers_code2.update(cookies)
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
    ycode=input("请输入验证码：")

    data = {
            'TextBox1': username,
            'TextBox2' : password,
            'TextBox3' : ycode,
            '__VIEWSTATE' : __VIEWSTATE,
            'RadioButtonList1' : '%D1%A7%C9%FA',
            'Button1' : '',
            'lbLanguage' : '',
        }
    return data

#获得查询课表的data，其中__VIEWSTATE，__VIEWSTATEGENERATOR需要先用get请求获得源码后在通过解析获得
def get_kb_data(kburl):
    response = s.get(kburl, headers=headers_code)
    html = response.content.decode('gb2312')
    soup = bs4.BeautifulSoup(html, 'lxml')
    __VIEWSTATE = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
    __VIEWSTATEGENERATOR = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
    data = {
        '__EVENTTARGET': 'xqd',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': __VIEWSTATE,
        '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
        'xnd':'',
        'xqd':''
    }
    data['xnd']=input("请输入你要查询的学年：")
    data['xqd']=input("请输入你要查询的学期：")
    return data

#获得查询成绩的data，其中__VIEWSTATE，__VIEWSTATEGENERATOR需要先用get请求获得源码后在通过解析获得，btn_xn的值为学年成绩的gb2312解码
def get_cj_data(kburl):
    response = s.get(kburl, headers=headers_code)
    html = response.content.decode('gb2312')
    soup = bs4.BeautifulSoup(html, 'lxml')
    __VIEWSTATE = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
    __VIEWSTATEGENERATOR = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
    data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': __VIEWSTATE,
        '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
        'hidLanguage': '',
        'ddlXN': '',
        'ddlXQ': '',
        'ddl_kcxz': '',
        'btn_xn': '%C0%FA%C4%EA%B3%C9%BC%A8',
    }
    data['ddlXN'] = input("请输入你要查询的学年:")
    return data

# name为登录成功后的网页源码解析后获得的姓名的gb2312解码
def login(url,data,action):
    r = s.post(url,headers=headers,data=data)
    if judge(r.text)==1:
            soup = bs4.BeautifulSoup(r.text, 'lxml')
            name_code = soup.find('span', attrs={'id': 'xhxm'})
            name = urllib.parse.quote_plus(str(name_code.string[11:14]).encode('gb2312'))
            kburl = get_headers(action,username,name)
            if (action == '学生信息录入' or action == '1' ):
                xxLoading(kburl, headers_code)
            elif (action == '学生课表录入' or action == '2' ):
                data = get_kb_data(kburl)
                kbLoading(kburl, headers_code2,data)
            elif (action == '学生成绩查询' or action == '3'):
                data = get_cj_data(kburl)
                cjLoading(kburl, headers_code2,data)
            else:
                print("输入指令有误")
    else:
        print(judge(r.text))
        print("请重新登录")
        main()
#判断登录的接口
def judge(html):
    soup_judge = bs4.BeautifulSoup(html,'html.parser')
    script = soup_judge.find_all('script')[0].text
    if "验证码不正确" in script:
        return "验证码错误"
    elif "用户名不存在" in script:
        return "用户名不存在"
    elif "密码错误" in script:
        return "密码错误"
    else:
        return 1

#学生信息的获取
def xxLoading(kburl,headers_code):
    db = pymysql.connect(host="localhost", user="root", passwd="123456", db="pystu", charset='utf8')
    cursor = db.cursor()
    response = s.get(kburl, headers=headers_code)
    html = response.content.decode('gb2312')
    soup = bs4.BeautifulSoup(html, 'lxml')
    id = soup.find('span', attrs={'id': 'xh'}).string
    name = soup.find('span', attrs={'id': 'xm'}).string
    sex = soup.find('span', attrs={'id': 'lbl_xb'}).string
    phone = soup.find('span', attrs={'id': 'lbl_bdh'}).string
    birthday = soup.find('span', attrs={'id': 'lbl_csrq'}).string
    idCord = soup.find('span', attrs={'id': 'lbl_sfzh'}).string
    profession = soup.find('span', attrs={'id': 'lbl_zymc'}).string
    cs = soup.find('span', attrs={'id': 'lbl_xzb'}).string
    enumber = soup.find('span', attrs={'id': 'lbl_ksh'}).string

    sql1 = "select * from student where sid='"+id+"'"
    cursor.execute(sql1)
    data = cursor.fetchone()
    if data == None:
        sql = "insert into student values('" + id + "','" + name + "','" + password + "','" + sex + "','" + phone + "','" + birthday + "','" + idCord + "','" + profession + "','" + cs + "','" + enumber + "')"
        try:
            cursor.execute(sql)
            db.commit()
            print("学生信息录入成功")
        except:
            print("学生信息录已存在")
    db.close()

#学生成绩的获取
def cjLoading(kburl,headers_code2,data):
    db = pymysql.connect(host="localhost", user="root", passwd="123456", db="pystu", charset='utf8')
    cursor = db.cursor()
    global s
    response = s.post(kburl, headers=headers_code2, data=data)
    html = response.content.decode('gb2312')
    soup1 = bs4.BeautifulSoup(html, 'lxml')
    trList = soup1.findAll('td')
    list = {}
    temp = trList[25]
    a = str(temp).find(">")
    b = str(temp).find("</tb>")
    for index in range(25, len(trList)-10, 15):
        list[(str(trList[index])[a + 1:b - 4])] = str(trList[index + 5])[a + 1:b - 4]
    for key in list:
        #先通过名字和学号对数据库内进行检查，如果存在数据这算出两个分数的平均值，不存在则直接插入
        sql1 = "select garde from score where cname='"+key+"' and sid ='"+username+"'"
        cursor.execute(sql1)
        data = cursor.fetchone()
        if data == None:
            sql = "insert into score(sid,cname,garde) values('" + username + "','" + key + "','" + list[key] + "')"
            try:
                cursor.execute(sql)
                db.commit()
            except:
                print("成绩录入失败")
        else:
            list[key] = str(int((float(list[key]) + float(data[0])) / 2))
            sql = "update score set garde ='" + list[key] + "' where cname ='"+key+"'"
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
                print("成绩修改失败")
    db.close()


#学生课表的查询
def kbLoading(kburl,headers_code2,data):
    db = pymysql.connect(host="localhost", user="root", passwd="123456", db="pystu", charset='utf8')
    cursor = db.cursor()
    global s
    response = s.post(kburl, headers=headers_code2, data=data)
    html = response.content.decode('gb2312')
    list = set()
    soup = bs4.BeautifulSoup(html,'lxml')
    csname = soup.findAll('td',attrs={'align':'Center','rowspan':'2'})
    for i in range(len(csname)):
        temp = csname[i]
        a = str(temp).find("<br/>")
        b = str(temp).find(">")
        list.add(str(temp)[b+1:a])
    for s in list:
        #先根据名称对数据库内的课表进行检查，如果存在则跳过，不存在则插入
        sql1 = "select * from course where cname='"+s+"'"
        cursor.execute(sql1)
        data = cursor.fetchone()
        if data == None:
            sql = "insert into course(cname) values('"+s+"')"
            try:
                cursor.execute(sql)
                db.commit()
            except:
                print("课程已存在")
    print("课程录入成功")
    db.close()


def main():
    data = get_post_date(url,username,password)
    print("1:学生信息录入")
    print("2:学生课表录入")
    print("3:学生成绩录入")
    action = input("请输入要执行的操作：")
    login(url,data,action)
    
if __name__ == '__main__':
    main()
