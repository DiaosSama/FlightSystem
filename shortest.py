#coding:utf-8
import cityDict
import numpy as np
import pandas as pd 

'''
    args：起点和终点的英文名
    return: 除直达线的最短路径
'''

def getShortest(beg, end):
    begIndex = cityDict.allCity2.index(beg)
    endIndex = cityDict.allCity2.index(end)
    # 读取距离信息和建立图
    data = pd.read_csv('info/timeTable.csv', sep=',', encoding='utf-8')
    dis = data['DISTENCE']
    length = len(cityDict.allCity)
    # 最短路径表
    minList = [-1] * length
    minList[begIndex] = 0
    # 访问列表
    vis = [1] * length
    vis[begIndex] = 0
    # 建图
    graph = np.zeros((length, length))
    index = 0
    for x in range(length):
        for y in range(length):
            if x == y:
                continue
            graph[x][y] = dis[index]
            index += 1
    # 终点和起点距离设为相对无限大
    graph[begIndex][endIndex] = graph[endIndex][begIndex] = 10**10
    # 路径记录表
    passCity = [] * length
    # 路径次序
    order = 0
    # 当前距离索引
    presentIndex = begIndex
    # 当前距离
    presentDis = 0
    # 更新路径表
    while(vis[endIndex]==1):
        for i in range(length):
            if vis[i]==1:
                if minList[i]==-1 or (presentDis+graph[presentIndex][i])<minList[i]:
                    minList[i] = presentDis + graph[presentIndex][i]
        
        # 路径表中最小距离
        newDis = -1
        # 路径表中最小距离索引
        newIndex = -1
        for i in range(length):
            if vis[i] == 1:
                if newDis==-1 or minList[i]<newDis:
                    newDis = minList[i]
                    newIndex = i
        # 找不到路径
        if newDis == -1:
            return None
        # 更新当前距离和距离索引
        presentDis = newDis
        presentIndex = newIndex
        vis[presentIndex] = 0
        # 添加到路径表 其中 minList[:] 为了复制列表
        passCity.append([minList[:], presentIndex])  
        
    # 查路径表得出最短路径
    passlen = len(passCity)
    parIndex = endIndex
    path = [[cityDict.allCity2[parIndex], passCity[passlen-1][0][parIndex]]]
    for i in range(passlen-1):
        if passCity[passlen-i-1][0][parIndex] == passCity[passlen-i-2][0][parIndex]:
            continue
        else:
            parIndex = passCity[passlen-i-2][1]
            path.append([cityDict.allCity2[parIndex], passCity[passlen-i-1][0][parIndex]])
    path.append([cityDict.allCity2[begIndex], 0])
    path.reverse()
    path[0].append(0)
    for i in range(1,len(path)):
        nowPlace = path[i][0]
        lastPlace = path[i-1][0]
        price = data.loc[(data['ORIGIN']==cityDict.reCityDict[lastPlace]) & (data['TERMINAL']==cityDict.reCityDict[nowPlace]), 'PRICE']
        path[i].append(int(price.values))
    
    return(path)
        
# print(getShortest('Aba' ,'Changchun'))
        



