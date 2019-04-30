import os
import json
import FlightInfo
import Const
import datetime
import hashlib


def myHash(text, size=Const.HASH_SIZE):
    home = 0
    bit = 1
    for i in text:
        home += ord(i) * bit
        bit += 1
    return int(home % size)


def newHashTable():
    hash_table = []
    for i in range(Const.HASH_SIZE):
        hash_table.append(Const.EMPTY)
    return hash_table


def saltPassword(password, salt="#%F&asuFU@Wax"):
    """
    加盐哈希函数
    :param password: str
    :param salt: str
    :return: str
    """
    salt_password = hashlib.sha256(password)
    salt_password = hashlib.sha256(salt_password+salt)
    return salt_password


def initFlightInfo():
    is_exist = os.path.exists(Const.PATH_FLIGHT_INFO)

    if is_exist:
        pass
    else:
        os.makedirs(Const.PATH_FLIGHT_INFO)


def queryFlightInfo(ticket):
    """
    返回匹配的查询结果，返回一个列表
    :param ticket: 航班信息
    :type ticket: FlightInfo.FlightInfo
    :return: 符合的所有航班信息列表
    :rtype: list
    """
    date = ticket.getDateStr()
    # 判断日期是否合法
    if isValidDate(date):
        start = ticket.getStart()
        end = ticket.getEnd()
        home = myHash(start + end, Const.HASH_SIZE)
        file = Const.PATH_FLIGHT_INFO + "\\" + date + ".json"

        if os.path.exists(file):
            f = open(file, "r")
            hash_table = json.load(f)
            f.close()
            index = home

            # 在哈希表中寻找起点终点相同的航班信息
            i = 1
            while True:
                # print("result:", hash_table[index])
                # 哈希查找失败条件
                if hash_table[index] == Const.EMPTY or hash_table[index] == []:
                    return Const.NO_SUIT_FLIGHT
                # 哈希查找的绝望阈值
                if i > Const.DES_VAL:
                    return Const.NO_SUIT_FLIGHT
                else:
                    suit = (ticket.getStart() == hash_table[index][0]['origin'] and
                            ticket.getEnd() == hash_table[index][0]['terminal'])
                    if suit:
                        Flight = hash_table[index]

                        # 航班按时间排序
                        def time(s):
                            hour, min = s['date']['startTime'].split(':')
                            hour = int(hour)
                            min = int(min)
                            return hour + (min / 60)

                        Flight = sorted(Flight, key=time)
                        return Flight
                    else:
                        index = (index + i * i) % Const.HASH_SIZE
                        i += 1
        else:
            return Const.FLIGHT_NOT_FOUND
    else:
        return Const.DATE_INVALID


def queryFlight(ticket):
    """
    返回具体航班信息
    :param ticket:
    :return:
    """
    pass


def addFlightInfo(ticket):
    """
    增加航班信息
    :param ticket:
    :type ticket:FlightInfo.FlightInfo
    :return: signal
    :rtype: int
    """
    date = ticket.getDateStr()
    start = ticket.getStart()
    end = ticket.getEnd()
    home = myHash(start + end, Const.HASH_SIZE)
    file = Const.PATH_FLIGHT_INFO + "\\" + date + ".json"

    if os.path.exists(file):
        f = open(file, "r")
        hash_table = json.load(f)
        f.close()
        index = home

        i = 1
        while True:
            if hash_table[index] == Const.EMPTY:
                hash_table[index] = []
                hash_table[index].append(ticket.__dict__)
                break
            elif hash_table[index] == []:
                hash_table[index].append(ticket.__dict__)
                break
            else:
                if hash_table[index][0]['origin'] + hash_table[index][0]['terminal'] == start + end:
                    hash_table[index].append(ticket.__dict__)
                    break
                elif i > Const.DES_VAL:
                    return Const.HASH_TABLE_FULL
                index = (index + i * i) % Const.HASH_SIZE
                i += 1

        f = open(file, "w")
        json.dump(hash_table, f)
        f.close()
        return Const.SUCCESS
    else:
        hash_table = newHashTable()
        hash_table[home] = ticket.__dict__
        f = open(file, "w+")
        json.dump(hash_table, f)
        f.close()
        return Const.SUCCESS


def delFlightInfo(ticket):
    """
    删除航班信息
    :type ticket: FlightInfo.FlightInfo
    :return: signal
    :rtype: int
    """
    date = ticket.getDateStr()
    start = ticket.getStart()
    end = ticket.getEnd()
    home = myHash(start + end, Const.HASH_SIZE)
    file = Const.PATH_FLIGHT_INFO + "\\" + date + ".json"

    if os.path.exists(file):
        f = open(file, "r")
        hash_table = json.load(f)
        f.close()
        index = home

        # 在哈希表中寻找起点终点相同的航班信息
        i = 1
        while True:
            # 哈希查找失败条件
            if hash_table[index] == Const.EMPTY:
                return Const.FLIGHT_NOT_FOUND
            # 哈希查找的绝望阈值
            if i > Const.DES_VAL:
                return Const.FLIGHT_NOT_FOUND

            suit = (ticket.getStart() == hash_table[index][0]['origin'] and
                    ticket.getEnd() == hash_table[index][0]['terminal'])
            # 进一步寻找起飞时间相同的航班
            if suit:
                for flight in hash_table[index]:
                    if flight == ticket.__dict__:
                        hash_table[index].remove(flight)
                        f = open(file, "w")
                        json.dump(hash_table, f)
                        f.close()
                        return Const.SUCCESS
                return Const.FLIGHT_NOT_FOUND
            else:
                index = (index + i * i) % Const.HASH_SIZE
                i += 1
    else:
        return Const.FLIGHT_NOT_FOUND


def revFlightInfo(oldTicket, newTicket):
    """
    修改航班信息
    :param oldTicket: 要修改的航班信息
    :param newTicket: 修改后的航班信息
    :type oldTicket: FlightInfo.FlightInfo
    :type newTicket: FlightInfo.FlightInfo
    :return: signal
    """
    date = oldTicket.getDateStr()
    start = oldTicket.getStart()
    end = oldTicket.getEnd()
    home = myHash(start + end, Const.HASH_SIZE)
    file = Const.PATH_FLIGHT_INFO + "\\" + date + ".json"

    # print("oldTicket",oldTicket.__dict__,'\n')
    # print("newTicket",newTicket.__dict__,'\n')

    if os.path.exists(file):
        f = open(file, "r")
        hash_table = json.load(f)
        f.close()
        index = home

        # 在哈希表中寻找起点终点相同的航班信息
        i = 1
        while True:
            print("before hash_table[index]", hash_table[index], '\n')
            # 哈希查找失败条件
            if hash_table[index] == Const.EMPTY:
                return Const.FLIGHT_NOT_FOUND

            # 哈希查找的绝望阈值
            if i > Const.DES_VAL:
                return Const.FLIGHT_NOT_FOUND

            suit = (oldTicket.getStart() == hash_table[index][0]['origin'] and
                    oldTicket.getEnd() == hash_table[index][0]['terminal'])
            # 进一步寻找起飞时间相同的航班
            if suit:
                for flight in hash_table[index]:

                    if flight["date"]["startTime"] == oldTicket.getStartTime():  # flight == oldTicket.__dict__:
                        hash_table[index].remove(flight)
                        hash_table[index].append(newTicket.__dict__)
                        print("after hash_table[index]", hash_table[index], '\n')
                        f = open(file, "w")
                        print("open ok")
                        json.dump(hash_table, f)
                        print("dump ok")
                        f.close()
                        print("close ok")
                        return Const.SUCCESS
                return Const.FLIGHT_NOT_FOUND
            else:
                index = (index + i * i) % Const.HASH_SIZE
                i += 1
    else:
        return Const.FLIGHT_NOT_FOUND


def isValidDate(date_str):
    # 判断日期是否合法
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def formatDate(year, month, day):
    # 日期格式化
    return str(year)+'-'+str(month)+'-'+str(day)
