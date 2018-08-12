#-*- coding:UTF-8 -*-
from time import time
import os
import sys
from datetime import datetime
import requests
from lxml import etree
import json
#from imp import reload
#reload(sys)
#sys.setdefaultencoding('utf8')

sys.path.append(sys.path[0]+'/../')
sys.path.append('/home/ubuntu/knownews/config/')

from config.models import *
from datetime import datetime,timedelta

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        }
post_url = 'https://www.huxiu.com/channel/ajaxGetMore'

root_url='https://www.huxiu.com'

class HuXiuCrawler(object):
    def __init__(self,url):
        self.url=url

    def __channels(self):
        html=requests.get(self.url,headers=headers).text
        selector=etree.HTML(html)
        
        zixun_infos=selector.xpath('//ul[@class="header-column header-column1 header-column-zx menu-box"]/li/a')
        items=[]
        for info in zixun_infos:
            item={}
            channel_name=info.xpath('text()')[0]
            catId=info.xpath('@href')[0].replace('/channel/','').replace('.html','')
            item['channel_name']=channel_name
            item['catId']=catId
            items.append(item)
        return items
    def __counts(self,channel):
        catId = channel['catId']
        post_data={
                    'huxiu_hash_code':'18f3ca29452154dfe46055ecb6304b4e',
                    'page':'1',
                    'catId':catId
                    }
        html=requests.post(post_url,data=post_data,headers=headers).text
        dict_data=json.loads(html)
        parse_data=dict_data['data']
        count=int(parse_data['total_page'])
        item={}
        item['channel_name']=channel['channel_name']
        item['count'] = count
        item['catId'] = channel['catId']
        return item
    def __url(self,channel_name,post_url,post_data):
        lit_article_url=[]
        html=requests.post(post_url,data=post_data,headers=headers).text
        dict_data=json.loads(html)
        parse_data=dict_data['data']
        total_page=parse_data['total_page']
        data=parse_data['data']
        selector=etree.HTML(data)
        article_urls=selector.xpath('//a/@href')
        for article_url in article_urls:
            if article_url.startswith('/article'):
                temp_url=root_url+article_url
        #        print(channel_name,article_url)
                lit_article_url.append(temp_url)
        lit_article_url=list(set(lit_article_url))
        return lit_article_url

    def __content(self,article_url):
        html=requests.get(article_url,headers=headers).text
        selector=etree.HTML(html)
        content='\n'.join(selector.xpath('//p/text()'))
        title =selector.xpath('//h1/text()')
        
        return ''.join(title),content
    def run(self):
        counts=[]
        for channel in self.__channels():
            counts.append(self.__counts(channel))
        for count_item in counts:
            catId=count_item['catId']
            count=count_item['count']
            for page in range(1,count+1):
                post_data = {
                        'huxiu_hash_code': '18f3ca29452154dfe46055ecb6304b4e',
                        'page': page,
                        'catId': catId
                        }
                channel_name=count_item['channel_name']
                article_urls=self.__url(channel_name,post_url,post_data)
                for article_url in article_urls:
                    i=i+1
                    title,content=self.__content(article_url)
                    #print ((title.strip()))
                    #print (type(content))
                    rawcontent=RawContents(title.strip(),content,'huxiu',datetime.now())
                    session=build_session('knownews')
                    session.add(rawcontent)
                    session.commit()
                    session.close()

if __name__=='__main__':
    c=HuXiuCrawler(root_url)
    c.run()

