#-*- coding:utf8 -*-
from time import time
import os
import sys
#from imp import reload
#reload(sys)
#sys.setdefaultencoding('utf8')

sys.path.append(sys.path[0]+'/../')
sys.path.append('/home/ubuntu/knownews/config/')


from utils.RedisUtil import RedisUtil

ru=RedisUtil()

ru.set('haha','xixi')
print (ru.get('haha'))
