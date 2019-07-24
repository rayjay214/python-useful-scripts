#!/usr/bin/env python
# coding=utf-8


'''
发现百度贴吧---某一个贴吧最近的发帖记录，并发邮件通知
爬虫线路： requests - bs4
Python版本： 3.6
OS： mac os 12.13.6
'''

import requests
from bs4 import BeautifulSoup

import arrow
import traceback
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
    分析贴吧的网页文件，整理信息，保存在列表变量中
    '''

    # 初始化一个列表来保存所有的帖子信息：
    comments = []
    # 首先，我们把需要爬取信息的网页下载到本地
    html = get_html(url)

    # 我们来做一锅汤
    soup = BeautifulSoup(html, 'lxml')

    # 按照之前的分析，我们找到所有具有‘ j_thread_list clearfix’属性的li标签。返回一个列表类型。
    liTags = soup.find_all('li', attrs={'class': 'j_thread_list clearfix'})

    #print(liTags)

    # 通过循环找到每个帖子里的我们需要的信息：
    for li in liTags:
        # 初始化一个字典来存储文章信息
        comment = {}
        # 这里使用一个try except 防止爬虫找不到信息从而停止运行
        try:
            # 开始筛选信息，并保存到字典中
            comment['title'] = li.find(
                'a', attrs={'class': 'j_th_tit'}).text.strip()
            comment['link'] = "http://tieba.baidu.com/" + \
                li.find('a', attrs={'class': 'j_th_tit'})['href']
            comment['name'] = li.find(
                'span', attrs={'class': 'tb_icon_author'}).text.strip()
            comment['time'] = li.find(
                'span', attrs={'class': 'pull-right is_show_create_time'}).text.strip()
            comment['replyNum'] = li.find(
                'span', attrs={'class': 'threadlist_rep_num center_text'}).text.strip()
            comment['lastReply'] = li.find(
                'span', attrs={'class': 'threadlist_reply_date pull_right j_reply_data'}).text.strip()

            if(':' in comment['lastReply'] and '2018' not in comment['time']):
                print(comment)
                comments.append(comment)
        except Exception as e:
            print('something wrong happened, error:{}'.format(e))

    return comments

g_str_mail_content = ''

def parse_each_post(list_content):
    global g_str_mail_content
    for item in list_content:
        url = item['link']
        #print(url)
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        #print(soup.prettify())
        #每一个回复的主体内容                          
        divMainPosts = soup.find_all('div', attrs={'class': 'd_post_content_main'})
        for post in divMainPosts:
            try:
                divMainContent = post.find('div', attrs={'class': 'd_post_content j_d_post_content'})
                spanMainContentTM = post.find_all('span', attrs={'class': 'tail-info'})
                content = divMainContent.text.strip()
                tm = spanMainContentTM[2].text.strip()
                arrow_tm = arrow.get(tm, 'YYYY-MM-DD HH:mm').to('local').to('utc')
                arrow_now = arrow.now()
                if(arrow_now.timestamp - (arrow_tm.timestamp - 28800) < 900):
                    #print('{},{},{}'.format(content, tm, item['link']))
                    g_str_mail_content += '{},{},{}\n'.format(content, tm, item['link'])

            except Exception as e:
                #print('{},{},{}'.format(divMainContent,e,traceback.print_exc()))
                pass

def Out2File(dict):
    with open('result.csv', 'w') as f:
        for comment in dict:
            f.write('{},{},{},{},{},{} \n'.format(
                comment['title'], comment['link'], comment['name'], comment['time'], comment['replyNum'], comment['lastReply']))

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

def main(base_url, deep):
    url_list = []
    for i in range(0, deep):
        url_list.append(base_url + '&pn=' + str(50 * i))

    for url in url_list:
        list_content = get_content(url)
        parse_each_post(list_content)

#base_url = 'https://tieba.baidu.com/f?kw=西部世界&ie=utf-8'
#base_url = 'http://tieba.baidu.com/f?ie=utf-8&kw=%E5%B8%86%E5%B8%83%E9%9E%8B&red_tag=b0939767394'
base_url1 = 'https://tieba.baidu.com/f?kw=xxxxxx&fr=index'
base_url2 = 'https://tieba.baidu.com/f?kw=xxxxxx&fr=index'
# 设置需要爬取的页码数量
deep = 1

if __name__ == '__main__':
    main(base_url1, deep)
    main(base_url2, deep)

    print(g_str_mail_content)
    if(g_str_mail_content):
        send_mail(g_str_mail_content)
