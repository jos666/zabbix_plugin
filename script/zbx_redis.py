#!/usr/bin/env python

import sys
import redis

redis_host = "127.0.0.1"
redis_port = 6379
redis_auth = 'crs-07i6tgia:jcWe2Plkds'


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: {0} [get|keys|ping]".format(sys.argv[0])
        exit(1)
    if sys.argv[1] == "get":
        try:
            r = redis.Redis(host=redis_host, port=redis_port, password=redis_auth)
            print r.info()[sys.argv[2]]
        except:
            print 0
    elif sys.argv[1] == 'keys':
        try:
            r = redis.Redis(host=redis_host, port=redis_port, password=redis_auth)
            print r.info().keys()
        except:
            print "error"
    elif sys.argv[1] == 'ping':
        try:
            r = redis.Redis(host=redis_host, port=redis_port, password=redis_auth)
            if r.ping():
                print 1
            else:
                print 0
        except:
            print 0
    else:
       print "Usage: {0} [get|keys|ping]".format(sys.argv[0])
        

