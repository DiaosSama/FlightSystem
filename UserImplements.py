from UserInfo import *
from FlightInfo import *
import Const


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


def registerUser(usrName, pwd, realName, sex, age, flightInfo):
    pass