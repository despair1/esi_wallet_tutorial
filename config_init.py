'''
Created on 01.10.2011

@author: mayor
'''

class _config_init:
    def __init__(self):
        self._conf={}
        f = open('config.txt', 'r')
        for line in f:
            line=line.strip(' \n')
            a=line.split('=',1)
            if len(a)>1 and a[1]:
                self._conf[a[0]]=a[1]
                #print a
                #print line
        f = open(self._conf.get("security_path"), 'r')
        for line in f:
            line = line.strip(' \n')
            a = line.split('=', 1)
            if len(a) > 1 and a[1]:
                self._conf[a[0]] = a[1]
    def get(self, name: object) -> object:
        return self._conf.get(name)


config_init = _config_init()
