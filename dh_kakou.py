# -*- coding: utf-8 -*-
import json

import requests


class DHKakou(object):

    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = kwargs['port']
        #self.city = kwargs['city']
        self.headers = {
            'authorization': 'HZSX',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.status = False
        
    def get_picrecord(self, _id, last_id):
        url = '''http://%s:%s/dahuaIS/rest/picrecord/search?q={"startId":%s,"endId":%s,"page":{"pageNo":1,"pageSize":100}}'''%(
            self.host, self.port, _id, last_id)
        try:
            r = requests.get(url, headers=self.headers)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise


if __name__ == '__main__':  # pragma nocover
    dhkk = DHKakou(**{'host': '10.44.245.247', 'port': 8082})
    for i in dhkk.get_picrecord(80128615, 80129615)['data']['rows']:
        if i['carType'] > 2:
            print i
        if i['carNum'][-1] == u'警':
            print i
