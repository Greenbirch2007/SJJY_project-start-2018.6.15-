# 1. 伪装头部，带有cookies请求,用正则进行匹配
# 2. 单页内容怕取确认，昵称，ID，年龄，婚姻状况，来自1，来自2，学历，身高，月薪，体重，全部图片
# 3.在搜索页实现翻页，怕取当前页面的单个个人的链接，放入第二步中
# 4.进行多线程爬取，讲怕取的数据存入到Mongo中

import requests
import re
import urllib
from selenium import webdriver



#解决JS渲染和翻页的问题,还要解决登录问题！


from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get('http://www.jiayuan.com/')


#录入账号和密码，点击操作


driver.find_element_by_xpath('//*[@id="hder_login_form_new"]/input[3]').clear()
driver.find_element_by_xpath('//*[@id="hder_login_form_new"]/input[3]').send_keys('')
driver.find_element_by_xpath('//*[@id="hder_login_form_new"]/input[4]').clear()
driver.find_element_by_xpath('//*[@id="hder_login_form_new"]/input[4]').send_keys('')
driver.find_element_by_xpath('//*[@id="hder_login_form_new"]/button').click()
# 等待之后再到搜索的界面
time.sleep(6)
driver.find_element_by_xpath('//*[@id="usercp_dltc_div"]/a').click()



#跳出的界面处理(自动刷新，把跳出的广告给刷掉)



def Schedule(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
        print('完成！')
    print('%.2f%%' % per)



#头部和cookie最好都用字典的形式
def get_one_page(url):
    headers= {''}



    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None

    except RequestException:
        return None
    return html
url = 'http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=3:155.175,23:1&sn=default&sv=1&p=1&pt=9612&ft=off&f=select&mt=d'
print(get_one_page(url))
#

#爬取单页具体数据
def parse_one_page(html):
    pattern = re.compile('_src="(.*?)"/></a></td>', re.S)
    items = re.findall(pattern, html)
    x = 0
    for item in items:
        urllib.request.urlretrieve(item, '/home/karson/JJJY/%s.jpg' % x, Schedule)
        x += 1

urls =['http://www.jiayuan.com/178908195?tid=0&cache_key=',
       'http://www.jiayuan.com/178986916?fxly=search_v2',
       'http://www.jiayuan.com/113716450?fxly=tj-ymtj-xyggxqdr',
       ]
if __name__ == '__main__':
    for url in urls :
        html = get_one_page(url)
        print(parse_one_page(html))



def main():
    html = get_one_page(url)
    items = parse_one_page(html)
    print(items)

# 缺乏执行的主程序 main（）


if __name__ == '__main__':
    main()


print(html)
为0的部分不好取匹配
pattern = re.compile('"member_info_r yh">.*?<h4>(.*?)<span>(.*?)</span>.*?<h6 class="member_name">(.*?)<a'
                     + '.*?target="_blank">(.*?)</a><a.*?<em>(.*?)</em>.*?身高：</div>.*?<em>(.*?)</em>'
                     +'.*?星座：</div>.*?<em>(.*?)</em>.*?属相：</div>.*?<em>(.*?)</em>',re.S)

# 设定好大的开始和结束匹配的范围！


pattern = re.findall('<div class="big_pic fn-clear" id="bigImg">.*?_src=(.*?)/></a></td>'
                     +'.*?_src=(.*?)/></a></td>''.*?_src=(.*?)/></a></td>',re.S)

# 图片匹配 compile匹配出单一格式，findall取出所有格式！
#
#
# 已经解决的问题：
# 1.selenium 模拟登录，点击
# 2.单个详情界面的信息解析，图片解析
# 3.单个详情界面的图片下载到本地
#
#
# 还未解决的问题：
# 1.最大的问题是selenium如何处理js的onclick方法，要用selenium包裹js语句？
# 2.selenium 翻页,搜索页面的链接解析(因为有广告挑出，暂时不作处理)
# 3.多进程部署
# 4.整个爬去逻辑的梳理，暂时整理一个思路：selenium,模拟登录，到搜索界面，解析当前页链接，然后
# 分两条路，一个是继续翻页，把解析到的链接存储在一个结合中（队列）；另一条就是从整个队里里面去解析
# 个人的所有信息（整合起来又要大费周章）
# 5.尝试把爬去的数据大规模的存储到数据库mysql，MongoDB中（这个部分可以先从其他项目实现中取测试！）
