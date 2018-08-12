# conding=utf-8

import sys
from redis import Redis
sys.path.append(sys.path[0]+'/../')
sys.path.append('/home/ubuntu/knownews/config/')


class RedisUtil(Redis):
    def __init__(self):
        super(RedisUtil,self).__init__('127.0.0.1',6379)

if __name__=='__main__':
    ru=RedisUtil()
    ru.set('zx','hello')
    print (ru.get('zx'))
