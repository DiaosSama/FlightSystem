from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import cityDict
import sys

'''
	类型：窗口
	参数：ticket
'''


class deFlightWindow(QWidget):

    def __init__(self, info):
        self.info = info
        super().__init__()
        self.initUI()
        
    
    def initUI(self):
        # 设置标题
        self.setWindowTitle("航空客运订票系统")

        # 导入QListWidget的qss样式
        '''with open("./QSS/QListWidgetQSS.qss", 'r') as f:   
            self.list_style = f.read()'''

        # 设置图标
        self.setWindowIcon(QIcon('icons/plane2.png'))

        self.setFixedSize(300, 350)

        self.setStyleSheet("background: #fff;")

        deFlightInfo = self.info
        date = deFlightInfo["date"]

        title = QLabel("航班信息详情")
        title.setStyleSheet("padding: 10px 80px;border: 1px solid black;")
        
        date_label = QLabel("航班日期")
        date_text = QLabel("{}年{}月{}日".format(date["year"], date["month"], date["day"]))

        startTime_label = QLabel("起飞时间")
        startTime_text = QLabel(date["startTime"])

        totalTime_label = QLabel("航班时间")
        totalTime_text = QLabel(date["totalTime"])

        origin_label = QLabel("起点")
        origin_text = QLabel(cityDict.reCityDict[deFlightInfo["origin"]])

        terminal_label = QLabel("终点")
        terminal_text = QLabel(cityDict.reCityDict[deFlightInfo["terminal"]])

        flightNum_label = QLabel("航班号")
        flightNum_text = QLabel(deFlightInfo["flightNum"])

        pasQuota_label = QLabel("乘员定额")
        pasQuota_text = QLabel(str(deFlightInfo["pasQuota"]))

        remTicketNum_label = QLabel("余票量")
        remTicketNum_text = QLabel(str(deFlightInfo["remTicketNum"]))

        price_label = QLabel("价格")
        price_text = QLabel(deFlightInfo["price"])

        state_label = QLabel("状态")
        state_text = QLabel(str(deFlightInfo["State"]))

        remark_label = QLabel("备注")
        remark_text = QLabel(deFlightInfo["remark"])

        layout = QGridLayout()
        layout.setSpacing(10)
        
        layout.addWidget(title, 0, 0, 1, 2, alignment=Qt.AlignCenter)
        layout.addWidget(date_label, 1, 0, 1, 1)
        layout.addWidget(date_text, 1, 1, 1, 1)
        layout.addWidget(startTime_label, 2, 0, 1, 1)
        layout.addWidget(startTime_text, 2, 1, 1, 1)
        layout.addWidget(totalTime_label, 3, 0, 1, 1)
        layout.addWidget(totalTime_text, 3, 1, 1, 1)
        layout.addWidget(origin_label, 4, 0, 1, 1)
        layout.addWidget(origin_text, 4, 1, 1, 1)
        layout.addWidget(terminal_label, 5, 0, 1, 1)
        layout.addWidget(terminal_text, 5, 1, 1, 1)
        layout.addWidget(flightNum_label, 6, 0, 1, 1)
        layout.addWidget(flightNum_text, 6, 1, 1, 1)
        layout.addWidget(pasQuota_label, 7, 0, 1, 1)
        layout.addWidget(pasQuota_text, 7, 1, 1, 1)
        layout.addWidget(remTicketNum_label, 8, 0, 1, 1)
        layout.addWidget(remTicketNum_text, 8, 1, 1, 1)
        layout.addWidget(price_label, 9, 0, 1, 1)
        layout.addWidget(price_text, 9, 1, 1, 1)
        layout.addWidget(state_label, 10, 0, 1, 1)
        layout.addWidget(state_text, 10, 1, 1, 1)
        layout.addWidget(remark_label, 11, 0, 1, 1)
        layout.addWidget(remark_text, 11, 1, 1, 1)

        self.setLayout(layout)


if __name__ == '__main__':
    
    info =  {'date': {'year': 2019, 'month': 4, 'day': 3, 'startTime': '00:02', 'totalTime': '3.65', 'endTime': '03:41'}, 'origin': 'Aba', 'terminal': 'Boao', 'flightNum': 'MU5545', 'planeNum': 'A340-600', 'pasQuota': 500, 'remTicketNum': 380, 'price': '962', 'orderedList': [], 'waitingList': [], 'State': 1, 'remark': ''}
    App = QApplication(sys.argv)
    ex = deFlightWindow(info)
    ex.show()
    sys.exit(App.exec_())
