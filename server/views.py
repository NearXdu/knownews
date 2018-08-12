import sys
import json

import requests
from aiohttp import web

sys.path.append(sys.path[0]+'/../')
sys.path.append('/home/ubuntu/knownews/config/')
sys.path.append('/home/ubuntu/knownews/utils/')

from config.models import *
from utils.RedisUtil import RedisUtil
from utils.util import *


# the index page request from wechat mini program
async def news_list_handle(request):
    session = build_session('knownews')
    results = session.query(WebNews).all()
    session.close()
    feeds = []
    for item in results:
        keywords = item.keywords.split(',')
        source = get_source_name_cn(item.source_id)
        news = {'news_id': item.id, 'news_title': item.title, 'abstract':item.abstract, 'source': source} 
        feeds.append(news)
    data = {'feeds': feeds}
    return web.json_response(data)

# the detail page request for a news
async def news_detail_handle(request):
    news_id = int(request.match_info.get('news_id', 0))
    
    session = build_session('knownews')
    result = session.query(WebNews).filter(WebNews.id == news_id).one()
    session.close()
    
    if not result:
        print("no such news\n")
        return web.Response(text="No Such News")
    keywords = strToList(result.keywords)
    news = {'news_id': news_id, 'news_title': result.title, 'abstract': result.title, 'keywords': keywords, 'content': result.content}
    #content = 'This is the detail page for news: %s\n%s\n' %(news_id, detail)
    return web.json_response(news)

# the keyword explaination request
async def keywords_explain_handle(request):
    keyword = request.match_info.get('keyword', 'NULL')
    explaination = get_keyword_explain(keyword)
    if not explaination:
        explaination = "None"
    data = {'keyword': keyword, 'explaination': explaination}
    return web.json_response(data)

# first find explaination in redis cache
# if no cache, get from mysql
# if still no record, query from BaiduBaike API or Wiki API
def get_keyword_explain(keyword):
    redis_client = RedisUtil()
    explain = redis_client.get(keyword)
    if explain:
        return explain
    try:
        session = build_session('knownews')
        results = session.query(KeywordsExplain).filter(KeywordsExplain.keyword == keyword).one()
        if results:
            return results.explaination

    except Exception as e:
        pass
    finally:
        session.close()
    return None
    
def get_explainlation_from_baidu_api(keyword):
    url = "http://baike.baidu.com/api/openapi/BaikeLemmaCardApi?scope=103&format=json&appid=379020&bk_key=%s&bk_length=600" % keyword
    #url = "http://baike.baidu.com/item/%s" % keyword
    user_agent = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
    headers = {'User-Agent': user_agent}
    #url = "http://shuyantech.com/api/cndbpedia/ment2ent?q=%s" % keyword
    res=requests.get(url, headers=headers)
    print(type(res.content))
    data=json.loads(res.content.decode('gb2312'))
    
    #data=json.loads(res.content.decode('utf-8'))
    for key,item in data.items():
        print(key)
        #for i in item:
        #    print(i.decode('utf-8'))
        print(key+':    '+str(item))

#get_explainlation_from_baidu_api("python")
def get_source_name_cn(source_id):
    session = build_session('knownews')
    result = session.query(NewsWebsites).filter(NewsWebsites.id == source_id).one()
    session.close()
    if result and not result.name_cn:
        return result.name_cn
    return "未知"

def parse_query(query_string):
    query_pairs = query_string.split('&')
    query_dict = {}
    for pair in query_pairs:
        key, value = pair.split('=')
        query_dict[key] = value
    return query_dict
