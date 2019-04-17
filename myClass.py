# 日期类
Date = { "year": 2019,
         "month": 1,
         "day": 1,
         "week": 2,
         "startTime": "0:0",
         "totalTime": 0 }



# 已订票的客户名单
OrderedList = { "name": "",
                "ticketNum": 0,
                "seatRank": 0 }


# 等候替补的客户名单
WaitingList = { "name": "",
                "ticketNum": 0 }


# 航线信息
FlightInfo = { "State": 1,
               "remark": "",
               "origin":"",
               "terminal" : "",
               "flightNum" : "",
               "planeNum" : "",
               "date" : Date,
               "pasQuota" : 0,
               "remTicketNum": 0,
               "orderedList": OrderedList,
               "waitingList": WaitingList }


# 用户信息
UserInfo = { "usrName": "",
             "pwd": "",
             "realName": "",
             "sex": "",
             "age": 0,
             "flightInfo": [] }
