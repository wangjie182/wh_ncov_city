# -*- coding:utf-8 -*-
'''
利用高德地图api实现经纬度与地址的批量转换
'''
import requests
import pandas as pd
import time
import importlib
import sys
import json

import numpy as np
importlib.reload(sys)

# 文档读取


def parse():
    datas = []
    m = 0
    lists=[]
    totalListData = pd.read_csv('Updates_NC.csv', encoding='gb2312')
    totalListDict = totalListData.to_dict('index')
    for j in range(0, len(totalListDict)):
        datas.append(
            str(totalListDict[j]['省份']+'省'+str(totalListDict[j]['城市'])+'|'))
    lists = [datas[i:i + 10] for i in range(0, len(datas), 10)]
    return lists

def transform(k,cityName):
    ak = 'zijishenqing'
    base = "http://restapi.amap.com/v3/geocode/geo?key=%s&address=%s&batch=true" % (
        ak, cityName)
    response = requests.get(base)
    answer = response. json()
    j=0
    list=[]
    while  (j< int(answer['count'])):
        if ((answer['geocodes'] != []) and (answer['geocodes'][j]['district'] != [])):
            province=answer['geocodes'][j]['province']
            city=answer['geocodes'][j]['city']
            location=answer['geocodes'][j]['location']
            location=''.join(location).split(',',1)
            jingdu=location[0]
            weidu=location[1]
            district=answer['geocodes'][j]['district']
            df.loc[k] = [province,city,district,jingdu,weidu]
            k=k+1
        j=j+1

if __name__ == '__main__':
    df = pd.DataFrame(columns=['province','city', 'district','jingdu','weidu'])
    cityNames = parse()
    k=0
    for cityName in cityNames:
        transform(k,cityName)
        k=k+10
    df.to_csv('locdetail7.csv', index=False)
