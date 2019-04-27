from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QIcon
import sys
import cityDict

'''
	类型：窗口
	参数：shortest的返回值
'''

class flightPathWindow(QWidget):

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

        path = self.info

        title = QLabel("推荐航班路线")
        title.setStyleSheet("text-align: center;border: 1px solid black;")
        
        distence_label = QLabel("距离")
        price_label = QLabel("价钱")

        distence_sum = 0
        price_sum = 0

        for i in path:
            distence_sum += i[1]
            price_sum += i[2]

        layout = QGridLayout()
        layout.setSpacing(10)
        
        order = 2
        layout.addWidget(title, 0, 0, 1, 3)
        layout.addWidget(QLabel("地点"), 1, 0, 1, 1)
        layout.addWidget(QLabel("距离(公里)"), 1, 1, 1, 1)
        layout.addWidget(QLabel("价钱(元)"), 1, 2, 1, 1)
        for i in range(len(path)):
            layout.addWidget(QLabel(cityDict.reCityDict[path[i][0]]), i+2, 0, 1, 1)
            layout.addWidget(QLabel(str(path[i][1])), i+2, 1, 1, 1)
            layout.addWidget(QLabel(str(path[i][2])), i+2, 2, 1, 1)
            order += 1
        layout.addWidget(QLabel("总计"), order, 0, 1, 1)
        layout.addWidget(QLabel(str(distence_sum)), order, 1, 1, 1)
        layout.addWidget(QLabel(str(price_sum)), order, 2, 1, 1)

        self.setLayout(layout)

'''   
if __name__ == '__main__':
    
    info =  [['Aba', 0, 0], ['Jiuzhaigou', 223.0, 702], ['Changchun', 2411.0, 999]]
    App = QApplication(sys.argv)
    ex = flightPathWindow(info)
    ex.show()
    sys.exit(App.exec_())
'''
   