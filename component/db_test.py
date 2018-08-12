#-*- coding:utf8 -*-
from time import time
import os
import sys
#from imp import reload
#reload(sys)
#sys.setdefaultencoding('utf8')

sys.path.append(sys.path[0]+'/../')
sys.path.append('/home/ubuntu/knownews/config/')

from config.models import *
from config.settings import *
from datetime import datetime,timedelta

class NewsGenerator(object):
    def get_news(self):
        news=[]
        session=build_session('knownews')
        result=session.query(WebNews.keywords).all()
        session.close()
        for row in result:
                news.append(row.keywords)
        return (news)

def CreateAllTable():
    db_name = 'knownews'
    engine = create_engine( URL(**settings.DATABASE[db_name]),connect_args={'charset':'utf8'})
    create_knownews_table(engine)



if __name__=='__main__':
    CreateAllTable()
    #ng=NewsGenerator()
    #keys=ng.get_news()[0].split(',')
    #for item in keys:
    #    print (item)


