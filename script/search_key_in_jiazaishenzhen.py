#!/usr/bin/env python
# coding=utf-8


'''
抓取家在深圳---包含某一关键字的所有帖子
'''

import requests
from bs4 import BeautifulSoup

import smtplib
from email.mime.text import MIMEText
import xlwt
from xlutils.copy import copy
import xlrd
import os
import configparser

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

def parse_one_page(title, url, sheet):
    global g_cur_row
    global g_keyword
    global g_including_ref

    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    '''
    divReply = soup.find_all('div', attrs={'id':'ReplyDetail'})
    for reply in divReply:
        content = reply.get_text().strip()
        idx = content.find('引用')        
        if idx != -1 and not g_including_ref:
            content = content[:idx]

        if g_keyword in content:
            #print(content)
            sheet.write(g_cur_row, 0, title)
            sheet.write(g_cur_row, 1, content)
            sheet.write(g_cur_row, 2, url)
            g_cur_row += 1
    '''
    try:
        divPoster = soup.find_all('div', attrs={'class':'post-aside item-userinfo'})
        for poster in divPoster:
            divMainPost = poster.find_next_sibling('div', attrs={'class':'post-main-wrap item-body'})
            str_username = poster.find('a', attrs={'class':'username'}).text
            str_replytm = divMainPost.find('span', attrs={'class':'post-time spanWriteTime'}).text
            str_content = divMainPost.find('div', attrs={'id':'ReplyDetail'}).get_text().strip()
        
            idx = str_content.find('引用')
            if idx != -1 and not g_including_ref:
                str_content = str_content[:idx]

            if g_keyword in str_content:
                #print(content)
                sheet.write(g_cur_row, 0, title)
                sheet.write(g_cur_row, 1, str_username)
                sheet.write(g_cur_row, 2, str_replytm)
                sheet.write(g_cur_row, 3, url)
                sheet.write(g_cur_row, 4, str_content)
                g_cur_row += 1
    except Exception as e:
        print('{},{},{},{},{}'.format(title, url, str_username, str_replytm, e))
 

def parse_one_post(title, url, sheet):
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
    parse_one_page(title, url, sheet)
    index = url.find('.html')    
    if page_num >= 2:
        for i in range(2, page_num):
            url_with_page = url[:index] + '-0-0-{}'.format(i) + url[index:]
            parse_one_page(title, url_with_page, sheet) 

def parse_all_post(dict_posts):
    global g_excel_name
    workbook, sheet = get_workbook()
    for title in dict_posts:
        url = dict_posts[title]
        parse_one_post(title, url, sheet)
    
    workbook.save(g_excel_name)

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

#if file already exist, append or else create a new one
def get_workbook():
    global g_excel_name
    b_exist = False
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if g_excel_name == f:
            b_exist = True
            break

    if b_exist:
        workbook, worksheet = open_workbook()
    else:
        workbook, worksheet = create_workbook()

    return workbook, worksheet

def create_workbook():
    workbook = xlwt.Workbook(encoding = 'utf8')
    worksheet = workbook.add_sheet('sheet1')
    return workbook, worksheet

def open_workbook():
    global g_cur_row
    global g_excel_name

    rb = xlrd.open_workbook(g_excel_name)
    r_sheet = rb.sheet_by_index(0)
    g_cur_row = r_sheet.nrows
    wb = copy(rb)
    sheet = wb.get_sheet(0)
    return wb, sheet

def parse_config():
    global g_begin_page
    global g_end_page
    global g_base_url
    global g_keyword
    global g_excel_name
    global g_including_ref

    cfg = configparser.ConfigParser()
    cfg.read('search_key_in_jiazaishenzhen.cfg')
    g_begin_page = int(cfg['DEFAULT']['begin_page'])
    g_end_page = int(cfg['DEFAULT']['end_page'])
    g_base_url = cfg['DEFAULT']['base_url']
    g_keyword = cfg['DEFAULT']['keyword']
    g_excel_name = cfg['DEFAULT']['excel_name']
    g_including_ref = cfg['DEFAULT']['including_ref']

def main():
    global g_base_url
    global g_begin_page
    global g_end_page

    url_list = []
    for i in range(g_begin_page, g_end_page):
        print('current page is {}'.format(i))
        url_list.append(g_base_url.format(i))

    for idx, url in enumerate(url_list):
        dict_posts = get_content(url)
        parse_all_post(dict_posts)
        print('page {} finished'.format(idx))

def test_parse_one_page(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml') 
    
    divPoster = soup.find_all('div', attrs={'class':'post-aside item-userinfo'})
    for poster in divPoster:
        divMainPost = poster.find_next_sibling('div', attrs={'class':'post-main-wrap item-body'})    
        str_username = poster.find('a', attrs={'class':'username'}).text
        str_replytm = divMainPost.find('span', attrs={'class':'post-time spanWriteTime'}).text
        str_content = divMainPost.find('div', attrs={'id':'ReplyDetail'}).get_text().strip()
        print('{},{},{}--------------'.format(str_username, str_replytm, str_content))

# all global varibles
g_begin_page = 0
g_end_page = 0
g_base_url = ''
g_keyword = ''
g_excel_name = ''
g_including_ref = False
g_cur_row = 1

if __name__ == '__main__':
    parse_config()
    main()
    #parse_one_post('aaa', 'http://bbs.szhome.com/30-30017-detail-176827746.html')
    #test_parse_one_page('http://bbs.szhome.com/30-30017-detail-176827746-0-0-2.html')

