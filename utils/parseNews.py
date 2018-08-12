#-*- coding:utf-8 -*-
import sys

from datetime import datetime

sys.path.append(sys.path[0]+'/../')
sys.path.append("/home/ubuntu/knownews/algo/")
sys.path.append('/home/ubuntu/knownews/config/')


from config.models import *
from algo.algo import *


def listToStr(keywords):
    result = ''
    for word in keywords:
        result += word
        result += ','
    return result[0:len(result)-1]

if __name__ == '__main__':

    session = build_session('knownews')
    results = session.query(RawContents).limit(10)


    for item in results:

        keywords_list = getKeywords(item.content)
        abstract = getAbstract(item.content)
        

        keywords = listToStr(keywords_list)
        print(keywords)
        news = WebNews(item.title, abstract, item.content, 2, datetime.now(), keywords)
        session.add(news)
        session.commit()



    session.close()
