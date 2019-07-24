#!/usr/bin/env python
# coding=utf-8


'''
抓取百度贴吧---西部世界吧的基本内容
爬虫线路： requests - bs4
Python版本： 3.6
OS： mac os 12.13.6
'''

import requests
from bs4 import BeautifulSoup

import arrow
import smtplib
from email.mime.text import MIMEText

def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return " ERROR "


def get_content(url):
    '''
    analyze main page
    '''
    # download to local
    html = get_html(url)

    soup = BeautifulSoup(html, 'lxml')

    #main post
    ddTags = soup.find_all('dd', attrs={'class': 'title f_yh'})

    dict_posts = {}  #key is title, value is url

    for dd in ddTags:
        try:
            list_a = dd.find_all('a')
            tagA = list_a[0]
            title = tagA.text.strip()
            post_url = "http://bbs.szhome.com{}".format(tagA['href'])
        
            dict_posts[title] = post_url
            #print('title:{}, url:{}'.format(title, post_url))

        except Exception as e:
            print('something wrong happened, error:{}'.format(e))
            exit()

    return dict_posts

g_str_mail_content = ''
g_count = 0

def parse_one_page(title, url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    divReply = soup.find_all('div', attrs={'id':'ReplyDetail'})
    for reply in divReply:
        content = reply.get_text().strip()
        if '名居' in content:
            print('{}|||{}|||{}'.format(title, content, url))

def parse_one_post(title, url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    #first, get page count
    divPage = soup.find('div', attrs={'class':'pagination pages'})
    list_a = divPage.find_all('a')
    page_num = 0
    for a in list_a:
        try:
            num = int(a.text.strip())
            if num > page_num:
                page_num = num
        except Exception as e:
            pass
    
    #parse each page
    parse_one_page(title, url)
    index = url.find('.html')    
    if page_num >= 2:
        for i in range(2, page_num):
            url_with_page = url[:index] + '-0-0-{}'.format(i) + url[index:]
            parse_one_page(title, url_with_page) 

def parse_all_post(dict_posts): 
    for title in dict_posts:
        url = dict_posts[title]
        parse_one_post(title, url)


def send_mail(content):
    HOST = 'smtp.qq.com'
    FROM = '526528945@qq.com'
    PWD = 'ujvthrkejqgobgci'
    SUBJECT = '通知'
    TO = ['526528945@qq.com']

    msg = MIMEText(content)
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = ','.join(TO)
    try:
        server = smtplib.SMTP_SSL(HOST, 465)
        server.login(FROM, PWD)
        server.sendmail(FROM, TO, msg.as_string())
        server.quit()
        print("Send email succeed!")
    except Exception as e:
        print("Send email error: %s" % e.args[0])

def main(base_url, g_begin_page, g_end_page):
    url_list = []
    for i in range(g_begin_page, g_end_page):
        url_list.append(base_url.format(i))

    for url in url_list:
        dict_posts = get_content(url)
        parse_all_post(dict_posts)

base_url = 'http://bbs.szhome.com/30017-0-0-0-{}.html'

# 设置需要爬取的页码数量
g_begin_page = 1
g_end_page = 5

if __name__ == '__main__':
    main(base_url, g_begin_page, g_end_page)
    #parse_one_post('aaa', 'http://bbs.szhome.com/30-30017-detail-176827746.html')

