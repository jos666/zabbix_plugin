# zabbix_plugin

## install
1. ln -s $(pwd)/script /opt
2. ln -s $(pwd)/conf/* /etc/zabbix/zabbix-agent.d/
3. zabbix web import template
4. host link template


## redis
1. install python redis lib 
```
easy_install redis
```
- china
```
easy_install -i http://pypi.douban.com/simple/ redis
```

### redis monitor items
1. cpu  user and sys 
2. mem  peak and rss 
3. clent  blocked_clients and connected_clients
4. db keys number
5. net input and output traffic



## lvs
** This script is mainly to monitor the number of connections LVS vip and enter the number of connections **
