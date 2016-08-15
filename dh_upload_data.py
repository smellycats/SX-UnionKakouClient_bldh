# -*- coding: utf-8 -*-
import time
import arrow

from dh_kakou import DHKakou
from union_kakou import UnionKakou

from ini_conf import MyIni
from helper import *


class UploadData(object):
    def __init__(self):
        # 配置文件
        self.my_ini = MyIni()
        self.kk_ini = self.my_ini.get_kakou()
        self.uk_ini = self.my_ini.get_union()

        # request方法类
        self.kk = DHKakou(**self.kk_ini)
        self.uk = UnionKakou(**self.uk_ini)

        # ID上传标记
        self.id_flag = self.kk_ini['id_flag']
        self.step = 1000


    def set_id(self, _id):
        """设置ID"""
        self.id_flag = _id
        self.my_ini.set_id(_id)

    def post_info(self):
        """上传数据"""
        car_info = self.kk.get_picrecord(self.id_flag+1, self.id_flag+self.step)
        # 如果查询数据为0
        if len(car_info['data']['rows']) == 0:
            return
        data = []
        hphm_dict = {u'0': '-'}
        try:
            for i in car_info['data']['rows']:
                data.append({'jgsj': i['capDate'],          # 经过时间
                             'hphm': hphm_dict.get(i['carNum'], i['carNum']), # 号牌号码
                             'kkdd_id': create_kkddid(i['carImgUrl']),        # 卡口地点ID
                             'hpys_id': hpzl2hpys(i['carType']),              # 号牌颜色ID
                             'fxbh': fxbh2code(int(i['carDirect'])),          # 方向编号
                             'cdbh': i['carWayCode'],       # 车道
                             'clsd': i['carSpeed'],         # 车速
                             'hpzl': '00',
                             'img_path': i['carImgUrl']})   # 图片url地址
            r = self.uk.post_kakou(data)  #上传数据
            # 设置最新ID
            self.set_id(car_info['data']['rows'][-1]['id'])
            #print car_info['data']['rows'][-1]['id']
        except Exception as e:
            print e



    def main_loop(self):
        while 1:
            if self.kk.status and self.uk.status:
                try:
                    self.post_info()
                    time.sleep(1)
                except Exception as e:
                    time.sleep(1)
            else:
                try:
                    if not self.kk.status:
                        self.kk.get_picrecord(80128615, 80128617)
                        self.kk.status = True
                    if not self.uk.status:
                        self.uk.connect_test()
                        self.uk.status = True
                except Exception as e:
                    time.sleep(1)
        

if __name__ == '__main__':  # pragma nocover
    fd = UploadData()
    fd.main_loop()
