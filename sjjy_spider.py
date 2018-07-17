# 1. 伪装头部，带有cookies请求,用正则进行匹配
# 2. 单页内容怕取确认，昵称，ID，年龄，婚姻状况，来自1，来自2，学历，身高，月薪，体重，全部图片
# 3.在搜索页实现翻页，怕取当前页面的单个个人的链接，放入第二步中
# 4.进行多线程爬取，讲怕取的数据存入到Mongo中
#  http://www.jiayuan.com/152873139
# url iid 从100万开始，手测到1.79亿个，单个页面请求，1万个测试就好！

import requests
import re
import urllib
import time
from requests.exceptions import RequestException  #用于捕捉异常
from multiprocessing import Pool
import random


# proxies = {"http":"http://222.41.154.119"}

#解决JS渲染和翻页的问题,还要解决登录问题！
# from selenium import webdriver
# import time
# driver = webdriver.Chrome()
# driver.get('http://www.jiayuan.com/')
#录入账号和密码，点击操作
# driver.find_element_by_xpath('//*[@id="hder_login_form_new"]/input[3]').clear()
# driver.find_element_by_xpath('//*[@id="hder_login_form_new"]/input[3]').send_keys('')
# driver.find_element_by_xpath('//*[@id="hder_login_form_new"]/input[4]').clear()
# driver.find_element_by_xpath('//*[@id="hder_login_form_new"]/input[4]').send_keys('')
# driver.find_element_by_xpath('//*[@id="hder_login_form_new"]/button').click()
# 等待之后再到搜索的界面
#跳出的界面处理(自动刷新，把跳出的广告给刷掉)


# 下载进度条，可以放在urllib.request.urlretrieve 里面做参数，暂时不用了！
def Schedule(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
        print('完成！')
    print('%.2f%%' % per)



#头部和cookie最好都用字典的形式
def get_one_page(url):
    # headers= {
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #     'Accept-Encoding': 'gzip, deflate',
    #     'Accept-Language': 'zh-CN,zh;q=0.9',
    #     'Cache-Control': 'max-age=0',
    #     'Connection': 'keep-alive',
    #     'Cookie': 'photo_scyd_48914263=yes; PHPSESSID=26c2ce6c61a70502621f11ad80ebbec7; main_search:145823914=%7C%7C%7C00; jy_safe_tips_new=xingfu; SESSION_HASH=4fa7aa4f2f673016bf283102a080c0ec1fedcd85; main_search:48914263=%7C%7C%7C00; user_access=1; pop_time=1531836905035; REG_REF_URL=http://www.jiayuan.com/; save_jy_login_name=2742374471%40qq.com; stadate1=144823914; myloc=99%7C9905; myage=29; PROFILE=145823914%3A%25E5%25B7%25B4%25E4%25B8%2580%25E4%25B8%258B%3Am%3Aat3.jyimg.com%2Feb%2F38%2F83bdb3ac44ed4c5ffe6598484026%3A1%3A%3A1%3A83bdb3ac4_1_avatar_p.jpg%3A1%3A1%3A0%3A10; mysex=m; myuid=144823914; myincome=40; mylevel=1; COMMON_HASH=eb83bdb3ac44ed4c5ffe659848402638; sl_jumper=%26cou%3D17%26omsg%3D0%26dia%3D0%26lst%3D2018-07-17; last_login_time=1531836912; upt=7DCUDGOIb-ENecHARUZmcKAKhrDoslrXN6JRnYDOeeCP61lKmhar%2Ak586hWL9JgpDpDRyP1OP7Jkt9dJQpmHryjRixZsanY.; user_attr=000000; pclog=%7B%22145823914%22%3A%221531836919542%7C1%7C0%22%7D; IM_CS=1; IM_ID=1; RAW_HASH=d6k6ABLDEksIUcmxAgG8L6pOC%2AYa9d4z%2AZtyJgpWRXcQVfNvNxPlCKNRRz2kJ173ZYnHG%2AcOA9vpcgxv1JHJG8HnX8wbT5tJOl3Ay6lD5pAeAt0.; IM_S=%7B%22IM_CID%22%3A2511713%2C%22IM_SV%22%3A%22211.151.166.59%22%2C%22svc%22%3A%7B%22code%22%3A0%2C%22nps%22%3A0%2C%22unread_count%22%3A%220%22%2C%22ocu%22%3A0%2C%22ppc%22%3A0%2C%22jpc%22%3A0%2C%22regt%22%3A%221445782080%22%2C%22using%22%3A%22%22%2C%22user_type%22%3A%2210%22%2C%22uid%22%3A145823914%7D%2C%22m%22%3A0%2C%22f%22%3A0%2C%22omc%22%3A0%7D; IM_CON=%7B%22IM_TM%22%3A1531836922045%2C%22IM_SN%22%3A2%7D; IM_M=%5B%5D; IM_TK=1531836940280',
    #     'Host': 'usercp.jiayuan.com',
    #     'Referer': 'http://www.jiayuan.com/',
    #     'Upgrade-Insecure-Requests': '1',
    #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    #
    # }
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None

    except RequestException:
        return None
    return html

#
#爬取单页信息
def parse_one_info(html):

    pattern = re.compile('"member_info_r yh">.*?<h4>(.*?)<span>(.*?)</span>.*?<h6 class="member_name">(.*?)<a'
                         + '.*?target="_blank">(.*?)</a><a.*?<em>(.*?)</em>.*?身高：</div>.*?<em>(.*?)</em>'
                         +'.*?星座：</div>.*?<em>(.*?)</em>.*?属相：</div>.*?<em>(.*?)</em>'+
                         '.*?<div class="bg_white mt15">.*?<h4>(.*?)的择偶要求</h4>',re.S)
    items = re.findall(pattern,html)
    for i in items:
        print(i)


#爬取单页图片
def parse_one_pics(html):
    pattern = re.compile('_src="(.*?)"/></a></td>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        urllib.request.urlretrieve(item, '/home/karson/JJJY/%s.jpg' % item[-10:-1])

# 主程序  # 过亿次请求效率不是很高，所以还是要破掉广告，考虑从火狐浏览器入手！
def main(offset):
    url = "http://www.jiayuan.com/13461311"  + str(offset)
    html = get_one_page(url)
    parse_one_pics(html)
    parse_one_info(html)
    # time.sleep(2)



if __name__ =="__main__":
    pool = Pool(4)
    pool.map(main, [i for i in range(1,9999,2)])











# 设定好大的开始和结束匹配的范围！
# 图片匹配 compile匹配出单一格式，findall取出所有格式！
# 已经解决的问题：
# 1.selenium 模拟登录，点击
# 2.单个详情界面的信息解析，图片解析
# 3.单个详情界面的图片下载到本地
# 还未解决的问题：
# 1.最大的问题是selenium如何处理js的onclick方法，要用selenium包裹js语句？
# 2.selenium 翻页,搜索页面的链接解析(因为有广告挑出，暂时不作处理)
# 3.多进程部署
# 4.整个爬去逻辑的梳理，暂时整理一个思路：selenium,模拟登录，到搜索界面，解析当前页链接，然后
# 分两条路，一个是继续翻页，把解析到的链接存储在一个结合中（队列）；另一条就是从整个队里里面去解析
# 个人的所有信息（整合起来又要大费周章）
# 5.尝试把爬去的数据大规模的存储到数据库mysql，MongoDB中（这个部分可以先从其他项目实现中取测试！）
