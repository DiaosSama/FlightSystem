from urllib.request import urlopen
from urllib.parse import quote
from math import *
import numpy as np
import json


def geocode(address):
    url = 'http://api.map.baidu.com/geocoder/v2/?address='
    output = 'json'
    ak = '53GZ4wkclp83FAwNxYE7wyYFctjEKHwB'
    add = quote(address)  # 本文城市变量为中文，为防止乱码，先用quote进行编码
    url2 = url+add+'&output='+output+"&ak="+ak
    req = urlopen(url2)
    res  = req.read().decode()
    answer = json.loads(res)

    if answer['status']  == 'INVALID_PARAMETERS':
        return 0,0
    else:
        lon = float(answer['result']['location']['lng'])
        lat = float(answer['result']['location']['lat'])
        return lon ,lat
    
def distance(address1,address2):
    
    lon1, lat1 = geocode(address1) 
    lon2, lat2 = geocode(address2)  

    # 将十进制度数转化为弧度  
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])  

    # haversine公式  
    dlon = lon2 - lon1   
    dlat = lat2 - lat1   
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  
    c = 2 * asin(sqrt(a))   
    r = 6371 # 地球平均半径，单位为公里  
    return int(c * r)

def distance_list(city_array):
    distance_array = []
    for i in range(city_array.shape[0]):
        distance_array.append(distance(city_array[i][0],city_array[i][1]))
    return np.array(distance_array)

#print(distance_list(np.array([['广州','上海'],['广州','北京']])))















