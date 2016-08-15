# -*- coding: utf-8 -*-
import json

import requests


class Kakou(object):

    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = kwargs['port']
        self.city = kwargs['city']

        self.status = False
        
    def get_cltxs(self, _id, last_id):
        url = 'http://{0}:{1}/rest_hz_kakou/index.php/{2}/kakou/cltxs/{3}/{4}'.format(
            self.host, self.port, self.city, _id, last_id)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

    def get_maxid(self):
        """获取cltx表最大id值"""
        url = 'http://{0}:{1}/rest_hz_kakou/index.php/{2}/kakou/cltxmaxid'.format(
            self.host, self.port, self.city)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

