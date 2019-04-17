class FlightInfo:
    # 类成员列表：[日期, 起点, 终点, 航班号, 飞机号, 航行时间, 乘员定额, 余票量]
    # __slots__ = ["date", "start", "end", "flight_number", "model", "duration", "quota", "surplus"]

    def __init__(self, date, start, end,
                 flight_number='', model='', quota=0, surplus=0, price=0, ordered=[], waiting=[], state=1, remark=''):
        self.date = date
        self.origin = start
        self.terminal = end
        self.flightNum = flight_number
        self.planeNum = model
        self.pasQuota = quota
        self.remTicketNum = surplus
        self.price = price
        self.orderedList = ordered
        self.waitingList = waiting
        self.State = state
        self.remark = remark

    def getDateStr(self):
        """
        返回年月日字符串
        :rtype: str
        """
        date = str(self.date["year"]) + str(self.date["month"]) + str(self.date["day"])
        return date

    def getStartTime(self):
        """
        返回起飞时间
        :rtype: str
        """
        return self.date["startTime"]

    def getStart(self):
        """
        返回起点
        :rtype: str
        """
        return self.origin

    def getEnd(self):
        """
        返回终点
        :rtype: str
        """
        return self.terminal

    def getEndTime(self):
        min = int(float(self.date["totalTime"])*60)
        orihour, orimin = self.date["startTime"].split(':')
        orihour = int(orihour)
        orimin = int(orimin)
        orihour += (orimin + min) / 60
        orimin = (orimin + min) % 60
        orihour %= 24
        hour = str(orihour).zfill(2)
        min = str(orimin).zfill(2)
        return hour+':'+min


        

