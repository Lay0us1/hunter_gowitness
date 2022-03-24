import requests
from datetime import datetime, date, timedelta
import re
import json
import time
import base64
import os

today = date.today()
# print(today)
hunter_api = "输入你的hunter key"
yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")  # 昨天日期
print(yesterday)


write_file_name = str(today)+".txt"

def readfile():
    page = 1  # 页面默认就是1
    a = open("hunter_keyword.txt", "r", encoding="utf8")
    aa = a.readlines()
    for i in range(len(aa)):
        b = aa[i].replace("\n", "")
        c = re.sub(r'after="(.*?)"', "after=\"" + yesterday + "\"", b)
        bytes_url = c.encode("utf-8")
        str_url = base64.b64encode(bytes_url)  # 被编码的参数必须是二进制数据
        d = str(str_url)
        e = d.replace("b\'", "").replace("\'", "").replace("/", "_").replace("+", "-")
        # print(e)
        url = "https://hunter.qianxin.com/openApi/search?api-key={}&search={}&page={}&page_size=100&is_web=1&status_code=200".format(
            hunter_api, e, page)
        r = requests.get(url)
        result = r.json()
        if result['code'] != 200:  # 如果状态码不等于200就退出
            exit("code={},message={}".format(result['code'], result['message']))
        else:
            ff = result['data']['total']
            # print(ff)
            time.sleep(3)
            try:
                for j in range(len(result['data']['arr'])):
                    url = result['data']['arr'][j]['url']
                    ip = result['data']['arr'][j]['ip']
                    port = result['data']['arr'][j]['port']
                    web_title = result['data']['arr'][j]['web_title']
                    print(url)
                    with open(write_file_name, 'a+') as oo:
                        oo.write(url+"\n")
                        oo.close()
            except:
                pass

def screen():
    os.system('gowitness.exe file -f {} -t 10 --timeout 5 -F -P screenshots --chrome-path "C:\Program Files\Google\Chrome\Application\chrome.exe"'.format(write_file_name))
    os.system("gowitness.exe report serve -A -a 127.0.0.1:10101")
readfile() # 读取hunter语句 并且将结果写入文件
screen() # 爬取写入后的文件并截图