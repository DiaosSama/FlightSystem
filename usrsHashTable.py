from myClass import *
from Const import *
import json


class usrsHashTable(object):

    def __init__(self):
        # 最大用户数
        self.n = 1000
        self.usrs = []
        with open("./info/UserInfo2.json", 'r') as load_f:
            self.usrs = json.load(load_f)

    def H1(self, x):
        length = len(x)
        home = 0
        for i in range(length):
            home = (home + ord(x[i])**2) % self.n
        return home

    def H2(self, x):
        return x

    # 添加用户
    def add(self, usr):
        if ("usrName" in usr.keys()) and (usr["usrName"]!=""):
            home = self.H1(usr["usrName"])
            index = home
            offset = 0
            while(self.usrs[index] != 0):
                if self.usrs[index]["usrName"] == usr["usrName"]:
                    return USER_EXISTED
                offset += 1
                index = home + self.H2(offset) % self.n
                # 绝望值
                desVal = 500
                if offset > desVal:   
                    return TOO_MANY_USERS
            self.usrs[index] = usr
            with open("./info/UserInfo2.json", 'w') as dump_f:
                json.dump(self.usrs, dump_f)
                print("写入 json 文件成功...")
            # 注册成功
            return 1
        else:
            return FORMAT_ERROR

    # 查询用户
    def get(self, name):
        home = self.H1(name)
        index = home
        offset = 0
        while True:
            if self.usrs[index] == 0:
                return SELECT_FAILED
            elif self.usrs[index]["usrName"] != name:
                offset += 1
                index = home + self.H2(offset) % self.n
                continue
            else:
                return index, self.usrs[index]

    # 删除用户
    def delete(self, name):
        result = self.get(name)
        if result == 0:
            return DELETE_FAILED
        else:
            self.usrs[result[0]] = 0
            with open("./info/UserInfo2.json", 'w') as dump_f:
                json.dump(self.usrs, dump_f)
                print("写入 json 文件成功...")
            # 删除成功
            return 1

    # 修改用户信息
    def revise(self, usr):
        result = self.get(usr["usrName"])
        print(result)
        if result == 0:
            return REVISE_FAILED
        else:
            # 更新除用户名和航班信息之外的信息
            result[1]["pwd"] = usr["pwd"]
            result[1]["realName"] = usr["realName"]
            result[1]["sex"] = usr["sex"]
            result[1]["age"] = usr["age"]
                
            # 更新哈希表
            self.usrs[result[0]] = result[1]
            with open("./info/UserInfo2.json", 'w') as dump_f:
                json.dump(self.usrs, dump_f)
                print("写入 json 文件成功...")
            # 修改成功
            return 1
        pass

    # 用户添加航班信息
    def addFlightInfo(self, usr, flightInfo):
        result = self.get(usr["usrName"])
        print(result)
        if result == 0:
            return ADD_FAILED
        else:
            # 添加航班信息
            result[1]["flightInfo"].append(flightInfo)
            # 更新哈希表
            self.usrs[result[0]] = result[1]
            with open("./info/UserInfo2.json", 'w') as dump_f:
                json.dump(self.usrs, dump_f)
                print("写入 json 文件成功...")
            # 添加成功
            return 1
        pass

    # 用户删除航班信息
    def deleteFlightInfo(self, usr, flightInfo):
        result = self.get(usr["usrName"])
        print(result)
        if result == 0:
            # 0 为删除失败代码
            return 0
        else:
            # 删除航班信息
            result[1]["flightInfo"].remove(flightInfo)
            # 更新哈希表
            self.usrs[result[0]] = result[1]
            with open("./info/UserInfo2.json", 'w') as dump_f:
                json.dump(self.usrs, dump_f)
                print("写入 json 文件成功...")
            # 1 为删除成功代码
            return 1

    # 用户修改航班信息
    def reviseFlightInfo(self, usr, oldFlightInfo, newFlightInfo):
        result = self.get(usr["usrName"])
        print(result)
        if result == 0:
            return DELETE_FAILED
        else:
            # 修改航班信息
            allFlightInfo = result[1]["flightInfo"]
            for i in range(len(allFlightInfo)):
                if allFlightInfo[i] == oldFlightInfo:
                    allFlightInfo[i] = newFlightInfo
                    break;
            # 更新哈希表
            self.usrs[result[0]] = result[1]
            with open("./info/UserInfo2.json", 'w') as dump_f:
                json.dump(self.usrs, dump_f)
                print("写入 json 文件成功...")
            # 修改成功
            return 1

    '''  
    订票只需在 flightInfo 追加一个航班信息
    至于等待购票、航班被迫取消、航班信息更新等机票状态可以在机票里的 state 设置
    退票可以直接在 flightInfo 删除航班信息
    
    '''

'''
if __name__ == "__main__":
    ht = HashTable()
    for i in ht.usrs:
        if i == 0:
            continue
        print(i)
'''
