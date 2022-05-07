#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests, os, time
from lxml import etree
import configparser

current_time = int(time.time())

ck = 'session=e6be8183-1d58-48ec-8223-f1fff53f7b7e; Hm_lvt_0838dad5461d14f63bdf207a43a54c29={}; _ga=GA1.2.2077364455.{}; _gid=GA1.2.192621886.{}; _gat_gtag_UA_128397857_1=1; Hm_lpvt_0838dad5461d14f63bdf207a43a54c29={}'.format(current_time,current_time,current_time,current_time)

headers_login = {
    'authority': 'dashboard.cpolar.com',
    'method': 'POST',
    'path': '/login',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': ck,
    'dnt': '1',
    'origin': 'https://dashboard.cpolar.com',
    'referer': 'https://dashboard.cpolar.com/login',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}
headers_tcp = {
    'authority':'dashboard.cpolar.com',
    'method':'GET',
    'path':'/status',
    'scheme':'https',
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': ck,
    'dnt':'1',
    'referer':'https://dashboard.cpolar.com/get-started',
    'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile':'?0',
    'sec-ch-ua-platform':'"Windows"',
    'sec-fetch-dest':'document',
    'sec-fetch-mode':'navigate',
    'sec-fetch-site':'same-origin',
    'sec-fetch-user':'?1',
    'upgrade-insecure-requests':'1',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}
headers_login = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}


def get_tcp(usr, pwd):
    session = requests.session()
    session.headers = headers_login
    tcp_ = ''
    url = 'https://dashboard.cpolar.com/login'

    params = f'login={usr}&password={pwd}'  #&csrf_token='+csrf_token
    res = session.post(url, headers=headers_login, data=params)

    if res.status_code == 200:
        status_url = 'https://dashboard.cpolar.com/status'
        sources = requests.get(status_url, headers=headers_tcp)
        e = etree.HTML(sources.text)
        item_list = e.xpath("//tr/td/text()")
        item_num = len(item_list)//4
        ip_list = [item_list[1 + 4*x] for x in range(item_num)]
        tcp_list = e.xpath("//th/a/text()")
        # tcp_ = ''.join(e.xpath("//th/a/text()"))
    return tcp_list, ip_list

def get_cpolar_config(cf):
    usr = cf.get("config", "username")
    pwd = cf.get("config", "password")
    return usr, pwd

if __name__ == '__main__':
    cf = configparser.ConfigParser()
    cf.read("config.ini")
    usr, pwd = get_cpolar_config(cf)
    tcp, ip = get_tcp(usr, pwd)
    print(tcp)
