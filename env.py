# -*- coding:utf-8 -*-
'''
利用高德地图api实现经纬度与地址的批量转换
'''
import requests
import pandas as pd
import time
import importlib
import sys

importlib.reload(sys)

#文档读取
def parse():
    datas = []
    totalListData = pd.read_csv('locs.csv', encoding='gb2312')
    totalListDict = totalListData.to_dict('index')
    for i in range(0, len(totalListDict)):
        datas.append(str(totalListDict[i]['cityName']))
    return datas


def transform(cityName):
    ak = 'zijishenqing'
    base = "http://restapi.amap.com/v3/geocode/geo?key=%s&address=%s&city=%s" % (
        ak, cityName,cityName)
    response = requests.get(base)
    answer = response.json()
    if ((answer['geocodes']!= []) and (answer['geocodes'][0]['city'] != [])):
        return answer['geocodes'][0]['province'], cityName, answer['geocodes'][0]['location']
    else:
        return 0

if __name__ == '__main__':
    i = 0
    count = 0
    df = pd.DataFrame(columns=['province', 'city', 'location'])
    cityNames = parse()
    for cityName in cityNames:
        if(transform(cityName)!=0):
            province, city, location = transform(cityName)
            df.loc[i] = [province, city, location]
        i = i + 1
    df.to_csv('locdetail4.csv', index=False)
