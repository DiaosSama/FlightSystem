from FlightInfo import *


class User:

    def __init__(self, usrName, pwd, realName, sex, age, flightInfo):
        self.usrName = usrName
        self.pwd = pwd
        self.realName = realName
        self.sex = sex
        self.age = age
        self.flightInfo = flightInfo

    def orderFlight(self, ticket):
        pass

    def unordFlight(self, ticket):
        pass

    