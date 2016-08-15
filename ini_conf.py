#-*- encoding: utf-8 -*-
import ConfigParser

class MyIni:

    def __init__(self, conf_path = '/home/my_ini.conf'):
        self.conf_path = conf_path
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(conf_path)

    def get_kakou(self):
        """获取卡口配置文件"""
        conf = {}
        section = 'KAKOU'
        conf['host']    = self.cf.get(section, 'host')
        conf['port']    = self.cf.getint(section, 'port')
        conf['id_flag'] = self.cf.getint(section, 'id_flag')
        conf['city']    = self.cf.get(section, 'city')
        return conf

    def get_union(self):
        """获取联网卡口配置文件信息"""
        conf = {}
        section = 'UNION'
        conf['host'] = self.cf.get(section, 'host')
        conf['port'] = self.cf.getint(section, 'port')
        return conf

    def set_id(self, id_flag):
        """设置id标记"""
        self.cf.set('KAKOU', 'id_flag', id_flag)
        self.cf.write(open(self.conf_path, 'w'))

    
