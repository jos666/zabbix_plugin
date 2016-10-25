#!/usr/bin/env python
# author: Finy
# email: jos666@qq.com

import json
import sys


class utils(object):
    @staticmethod
    def hex2bin(s):
        # print hex2bin('C0A80249')
        num = int(s, 16)
        mid = []
        while True:
            if num == 0:
                break
            num, rem = divmod(num, 2)
            mid.append(str(rem))
        res = ''.join(mid)
        #print '11000000101010000000001001001001'
        return res[::-1]

    @staticmethod
    def hex2ip(s):
        'hex to ip address '
        bins = utils.hex2bin(s)
        ip = []
        digits = 8
        for i in range(4):
            start = 0 if i == 0 else i * digits
            stop = digits if i == 0 else digits * (i + 1)
            ip.append(str(int(bins[start:stop], 2)))
        return '.'.join(ip)

    @staticmethod
    def hex2str(s):
        ip, port = s.split(':')
        return utils.hex2ip(ip) + ':' + str(int(port, 16))


class ipvsadm(object):
    def __init__(self, kernel="/proc/net/ip_vs"):
        self.kernel = kernel
        with open(kernel) as f:
            self.ipvs = f.readlines()

    def verify_data(self):
        no_valid = ['LocalAddress:Port', 'RemoteAddress:Port',
                    'IP Virtual Server']
        delete_index = []
        for line in self.ipvs:
            if any(map(lambda x: x in line, no_valid)):
                delete_index.append(self.ipvs.index(line))
        delete_index.sort(reverse=True)
        for i in delete_index:
            del self.ipvs[i]

    def flush(self):
        vip = ['TCP', 'UDP', 'wrr', 'rr', 'persistent']
        data = {}
        for line in self.ipvs:
            if any(map(lambda x: x in line, vip)):
                if 'persistent' in line:
                    proto, viphex, alg, p, ptime, No = line.split()
                else:
                    proto, viphex, alg, No = line.split()
                viphex = utils.hex2str(viphex)
                data[viphex] = []
            if '->' in line:
                No, riphex, forward, Weight, ActiveConn, InActConn = \
                    line.split()
                riphex = utils.hex2str(riphex)
                data[viphex].append({'rip': riphex, 'forward': forward,
                                     'Weight': Weight, 'ActiveConn':
                                     ActiveConn, 'InActConn': InActConn})
        self.data = data

    def discovery(self):
        data = {'data': []}
        for k in self.data.keys():
            data['data'].append({'{#VIP}': k})
            #for i in self.data[k]:
                # data.append({'${#VNAME}': 'vip:' + k + '_' + 'real_server:' +
                #             i['rip'] + '_w:' + i['Weight']})
        return json.dumps(data, indent=4)

    def get(self, key, name):
        data = {}
        for k in self.data.keys():
            data[k] = {'ActiveConn': 0, 'InActConn': 0}

            for i in self.data[k]:
                data[k]['ActiveConn'] = data[k]['ActiveConn'] + \
                    int(i['ActiveConn'])
                data[k]['InActConn'] = data[k]['InActConn'] + \
                    int(i['InActConn'])
               # data['vip:' + k + '_' + 'real_server:' + i['rip'] + '_w:' +
               #      i['Weight']] = i
        try:
            return data[key][name]
        except:
            raise SystemExit

    def view(self):
        pass


if __name__ == '__main__':
    if len(sys.argv) == 1:
        Usage = "Usage: {0} [discovery|name key]\n" + \
            "\te.g: {0} discovery\n" + "\t     {0} 192.168.2.70" + \
            ":8080 ActiveConn"
        print Usage.format(sys.argv[0])
        raise SystemExit

    i = ipvsadm()
    i.verify_data()
    i.flush()
    if sys.argv[1] == 'discovery':
        print i.discovery()
    else:
        print i.get(*sys.argv[1:])
