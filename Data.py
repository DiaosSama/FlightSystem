import copy
from FlightImplements import *
from FlightInfo import FlightInfo
import random
import Const
import json
import csv


def init_data(y, m, d):
    hash_table = newHashTable()
    State = 1
    remark = ""
    originList = ['Aba', 'Akesu', 'Bayannaoer', 'Baotou', 'Beihai', 'Beijing', 'Boao', 'Changchun', 'Changsha',
                  'Changzhi', 'Changzhou', 'Chaoyang', 'Chengdu', 'Chifeng', 'Dazhou', 'Dali', 'Dalian', 'Daqing',
                  'Datong', 'Dandong', 'Dacheng', 'Dunhuang', 'Erdos', 'Shiyan', 'Shihezi', 'Fuzhou', 'Fuyuan',
                  'Gaoyang', 'Ganzhou', 'Guangyuan', 'Guangzhou', 'Guiyang', 'Guilin', 'Harbin', 'Hami', 'Haikou',
                  'Hailar ', 'Hangzhou', 'Hefei', 'Hohhot', 'Huizhou', 'Huai', 'Hetian', 'Huangshan', 'Jieyang',
                  'Jinjiang quanzhou', 'Jinggangshan', 'Jingdezhen', 'Jiamusi', 'Jiuzhaigou', 'Jiansanjiang', 'Korla',
                  'Kelamayi', 'Kunming', 'Kashi', 'Lanzhou', 'Lijiang', 'Linzhi', 'Liuzhou', 'Six panshui', 'Zhangzhou',
                  'Linfen', 'Lhasa', 'Manzhouli', 'Maotai', 'Mudanjiang', 'Mianyang', 'Nanchang', 'Nanjing', 'Nanning',
                  'Nantong', 'Ningbo', 'Panzhihua', 'Qiqihar ', 'Qingdao', 'Sanya', 'Shijiazhuang', 'Songyuan',
                  'Shanghai', 'Shenzhen', 'Shenyang', 'Taizhou', 'Taiyuan', 'Tianjin', 'Tonghua', 'Tongliao', 'Tulufan',
                  'Wanzhou', 'Weihai', 'Wenzhou', 'Wulumuqi', 'Wuxi', 'Wuhai', 'Wuhan', 'Ulanhot', 'Ulanchabu', 'Xian',
                  'Xichang', 'Xining', 'Xilinhot', 'Xiamen', 'Xuzhou ', 'Yantai', 'Yanji', 'Yancheng', 'Yangzhou',
                  'Yining', 'Yibin', 'Yichang', 'Yiwu', 'Yinchuan', 'Yulin', 'Yuncheng', 'Zhanjiang', 'Zhangjiajie',
                  'Zhengzhou', 'Chongqing', 'Zhuhai', 'Zunyi']
    terminalList = ['Aba', 'Akesu', 'Bayannaoer', 'Baotou', 'Beihai', 'Beijing', 'Boao', 'Changchun', 'Changsha',
                    'Changzhi', 'Changzhou', 'Chaoyang', 'Chengdu', 'Chifeng', 'Dazhou', 'Dali', 'Dalian', 'Daqing',
                    'Datong', 'Dandong', 'Dacheng', 'Dunhuang', 'Erdos', 'Shiyan', 'Shihezi', 'Fuzhou', 'Fuyuan',
                    'Gaoyang', 'Ganzhou', 'Guangyuan', 'Guangzhou', 'Guiyang', 'Guilin', 'Harbin', 'Hami', 'Haikou',
                    'Hailar ', 'Hangzhou', 'Hefei', 'Hohhot', 'Huizhou', 'Huai', 'Hetian', 'Huangshan', 'Jieyang',
                    'Jinjiang quanzhou', 'Jinggangshan', 'Jingdezhen', 'Jiamusi', 'Jiuzhaigou', 'Jiansanjiang', 'Korla',
                    'Kelamayi', 'Kunming', 'Kashi', 'Lanzhou', 'Lijiang', 'Linzhi', 'Liuzhou', 'Six panshui', 'Zhangzhou',
                    'Linfen', 'Lhasa', 'Manzhouli', 'Maotai', 'Mudanjiang', 'Mianyang', 'Nanchang', 'Nanjing', 'Nanning',
                    'Nantong', 'Ningbo', 'Panzhihua', 'Qiqihar ', 'Qingdao', 'Sanya', 'Shijiazhuang', 'Songyuan',
                    'Shanghai', 'Shenzhen', 'Shenyang', 'Taizhou', 'Taiyuan', 'Tianjin', 'Tonghua', 'Tongliao', 'Tulufan',
                    'Wanzhou', 'Weihai', 'Wenzhou', 'Wulumuqi', 'Wuxi', 'Wuhai', 'Wuhan', 'Ulanhot', 'Ulanchabu', 'Xian',
                    'Xichang', 'Xining', 'Xilinhot', 'Xiamen', 'Xuzhou ', 'Yantai', 'Yanji', 'Yancheng', 'Yangzhou',
                    'Yining', 'Yibin', 'Yichang', 'Yiwu', 'Yinchuan', 'Yulin', 'Yuncheng', 'Zhanjiang', 'Zhangjiajie',
                    'Zhengzhou', 'Chongqing', 'Zhuhai', 'Zunyi']
    cityChinese = ['阿坝', '阿克苏', '巴彦淖尔', '包头', '北海', '北京', '博鳌', '长春', '长沙', '长治', '常州', '朝阳',
                   '成都', '赤峰', '达州', '大理', '大连', '大庆', '大同', '丹东', '稻城', '敦煌', '鄂尔多斯', '十堰',
                   '石河子', '福州', '抚远', '阜阳', '赣州', '广元', '广州', '贵阳', '桂林', '哈尔滨', '哈密', '海口',
                   '海拉尔', '杭州', '合肥', '呼和浩特', '惠州', '淮安', '和田', '黄山', '揭阳', '晋江', '井冈山', '景德镇',
                   '佳木斯', '九寨沟', '建三江', '库尔勒', '克拉玛依', '昆明', '喀什', '兰州', '丽江', '林芝', '柳州',
                   '六盘水', '泸州', '临汾', '拉萨', '满洲里', '茅台', '牡丹江', '绵阳', '南昌', '南京', '南宁', '南通',
                   '宁波', '攀枝花', '齐齐哈尔', '青岛', '三亚', '石家庄', '松原', '上海', '深圳', '沈阳', '台州', '太原',
                   '天津', '通化', '通辽', '吐鲁番', '万州', '威海', '温州', '乌鲁木齐', '无锡', '乌海', '武汉', '乌兰浩特',
                   '乌兰察布', '西安', '西昌', '西宁', '锡林浩特', '厦门', '徐州', '烟台', '延吉', '盐城', '扬州', '伊宁',
                   '宜宾', '宜昌', '义乌', '银川', '榆林', '运城', '湛江', '张家界', '郑州', '重庆', '珠海', '遵义']
    cityEntoCh = dict(zip(cityChinese, originList))
    infFlightNum = ['3U8', '8L9', '9C8', 'BK2', 'CA1', 'CA4', 'CA8', 'CA9', 'CN7', 'CZ2', 'CZ3', 'CZ4', 'CZ6', 'EU2',
                    'EU6', 'FM9', 'G52', 'GS6', 'GS7', 'HO1', 'HU7', 'JD5', 'JR1', 'KN2', 'KN5', 'KY8', 'MF8', 'MU2',
                    'MU5', 'MU7', 'MU9', 'NS3', 'OQ2', 'PN6', 'SC4', 'SC1', 'TV9', 'ZH9', 'ZH3']
    behFlightNum = []
    for i in range(1000):
        behFlightNum.append(str(i).zfill(3))
    planeNum = ['A320-300', 'A320-200', 'A320-600', 'A330-300', 'A330-200', 'A340-300', 'A340-200', 'A340-600',
                '737-600', '737-700', '737-800', '737-900', '747-400', '757-200', '757-300', '767-300', '767-400',
                '777-200', '777-300']
    pasQuota = [289, 158, 274, 210, 210, 295, 295, 380, 132, 149, 189, 189, 400, 200, 240, 260, 375, 380, 382]
    planeQuota = dict(zip(planeNum, pasQuota))
    orderedList = []
    waitingList = []
    Date = {"year": y, "month": m, "day": d}
    date = ""
    totalTime = 0
    price = 0

    # 每个起点终点对应生产航班
    for i in range(len(originList)):
        for j in range(len(terminalList)):
            if i == j:
                continue
            else:
                size = random.randint(1, 15)

                # 初始化价格
                with open("info/timeTable.csv", encoding='UTF-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        hi, he = cityEntoCh[row["ORIGIN"]], cityEntoCh[row["TERMINAL"]]
                        if (hi, he) == (originList[i], terminalList[j]):
                            price = row["PRICE"]
                            totalTime = row["TIME"]
                            break
                        else:
                            continue
                f.close()

                # 随机生成1-15班航班
                for k in range(size):
                    # 初始化航班号
                    num = random.randint(0, len(infFlightNum)-1)
                    IFN = infFlightNum[num]
                    num = random.randint(0, len(behFlightNum)-1)
                    FN = IFN + behFlightNum[num]

                    # 初始化飞机型号
                    num = random.randint(0, len(planeNum)-1)
                    PN = planeNum[num]

                    # 初始化飞机乘客量
                    PQ = planeQuota[PN]

                    # 初始化起飞时间
                    num = random.randint(0, 23)
                    hour = str(num).zfill(2)
                    orihour = num
                    num = random.randint(0, 59)
                    min = str(num).zfill(2)
                    newDate = copy.deepcopy(Date)
                    newDate["startTime"] = hour+':'+min
                    newDate["totalTime"] = totalTime

                    min = int(num)
                    orimin = int(float(totalTime) * 60)
                    orihour += int((min + orimin) / 60)
                    min = (orimin + min) % 60
                    orihour %= 24
                    hour = str(orihour).zfill(2)
                    min = str(min).zfill(2)
                    newDate["endTime"] = hour+':'+min
                    # print(Date["startTime"])

                    # 初始化飞行时间

                    info = FlightInfo(newDate, originList[i], terminalList[j], FN, PN, PQ, PQ, price, orderedList,
                                      waitingList, State, remark)
                    date = info.getDateStr()
                    info = info.__dict__
                    # print(hash_table)
                    index = myHash(originList[i]+terminalList[j], Const.HASH_SIZE)
                    # print(index)

                    time = 1
                    while True:
                        if hash_table[index] == Const.EMPTY:
                            hash_table[index] = []
                            hash_table[index].append(info)
                            print(info)
                            break
                        else:
                            if hash_table[index][0]['origin'] + hash_table[index][0]['terminal'] == originList[i] + terminalList[j]:
                                hash_table[index].append(info)
                                print(info)
                                break
                            elif time > Const.DES_VAL:
                                return Const.HASH_TABLE_FULL
                            index = (index + time * time) % Const.HASH_SIZE
                            time += 1
        # print(hash_table)

    file = Const.PATH_FLIGHT_INFO + "\\" + date + ".json"
    f = open(file, "w")
    json.dump(hash_table, f)
    f.close()


if __name__ == '__main__':
    init_data(2019, 4, 3)

