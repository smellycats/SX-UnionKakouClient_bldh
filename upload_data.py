# -*- coding: utf-8 -*-
import arrow

from kakou import Kakou
from union_kakou import UnionKakou

from ini_conf import MyIni


class UploadData(object):
    def __init__(self):
        # 配置文件
        self.my_ini = MyIni()
        self.kk_ini = self.my_ini.get_kakou()
        self.uk_ini = self.my_ini.get_union()

        # request方法类
        self.kk = Kakou(**self.kk_ini)
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
        maxid = self.kk.get_maxid()['maxid']
        # 没有新数据则返回
        if maxid <= self.id_flag: 
            return

        if maxid < (self.id_flag + self.step):
            last_id = self.id_flag + self.step
        else:
            last_id = maxid

        car_info = self.kk.get_cltxs(self.id_flag, last_id)
        # 如果查询数据为0
        if car_info['total_count'] == 0:
            # 设置最新ID
            self.set_id(last_id)
            return

        # 过滤卡口地点ID为None的数据
        effect_car_info = filter(lambda x: x['kkdd_id'] is not None,
                                 car_info['items'])
        data = []
        for i in effect_car_info:
            data.append({'jgsj': i.jgsj,          # 经过时间
                         'hphm': i.hphm,          # 号牌号码
                         'kkdd_id': i.kkdd_id,    # 卡口地点ID
                         'hpys_id': '',           # 号牌颜色ID
                         'fxbh': i.fxbh_code,     # 方向编号
                         'cdbh': i.cdbh,          # 车道
                         'img_path': i.img_path}) # 图片url地址
        r = self.uk.post_kakou(data)  #上传数据
        # 设置最新ID
        self.set_id(last_id)


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
                        self.kk.get_maxid()
                        self.kk.status = True
                    if not self.uk.status:
                        self.uk.get_test()
                        self.uk.status = True
                except Exception as e:
                    time.sleep(1)
        
