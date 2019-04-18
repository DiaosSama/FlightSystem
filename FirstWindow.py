import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image
from usrsHashTable import *
from SecondWindow import *
from MainWindow import *

class FirstWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # 读取用户表
        self.table = usrsHashTable()
        self.usrs = self.table.usrs
        self.usrNames = []
        for i in self.usrs:
            if i != 0:
                self.usrNames.append(i["usrName"])
        #print(self.usrNames)

        # 导入qss样式
        file = QFile("./QSS/QSS.qss")
        # file = QFile("./QSS/flatwhite.qss")
        file.open(QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet = str(styleSheet, encoding='utf8')
        qApp.setStyleSheet(styleSheet)

        # 设置图标
        self.setWindowIcon(QIcon('icons/plane2.png'))
        # 登陆图片
        welcome_picture = QLabel(self)
        jpg = QPixmap('./pictures/welcome.jpg')
        welcome_picture.setPixmap(jpg)
        # 账号编辑文本框
        self.lineEdit_account = QLineEdit(self)
        self.lineEdit_account.setPlaceholderText("请输入账号")
        # 密码编辑文本框
        self.lineEdit_password = QLineEdit(self)
        self.lineEdit_password.setPlaceholderText("请输入密码")
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        # 回车连接登录事件
        self.lineEdit_account.returnPressed.connect(self.okButton_clicked)
        self.lineEdit_password.returnPressed.connect(self.okButton_clicked)
        # 登录按钮
        self.okButton = QPushButton("登录")
        # 退出按钮
        self.cancelButton = QPushButton("退出")

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.lineEdit_account)
        hbox1.addWidget(self.okButton)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.lineEdit_password)
        hbox2.addWidget(self.cancelButton)

        vbox = QVBoxLayout()
        vbox.addWidget(welcome_picture)
        vbox.addStretch()
        vbox.addLayout(hbox1)
        vbox.addStretch()
        vbox.addLayout(hbox2)
        vbox.addStretch()

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("登录界面")
        self.show()

        # 绑定事件
        self.okButton.clicked.connect(self.okButton_clicked)
        self.cancelButton.clicked.connect(QCoreApplication.instance().quit)


    def okButton_clicked(self):
        if self.lineEdit_account.text() == "" or self.lineEdit_password.text() == "":
            # 弹出信息框
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "用户名或密码不能为空！")
            msg_box.show()
            msg_box.exec_()
            return
        else:
            account = self.lineEdit_account.text()
            password = self.lineEdit_password.text()
            # 判断用户名是否存在
            if account in self.usrNames:
                rightPassword = self.table.get(account)[1]["pwd"]
                # 判断密码是否正确
                if password == rightPassword:
                    # 通过验证，进入系统
                    # 管理员窗口
                    if account == "admin":
                        self.newWindow = SecondWindow()
                        self.newWindow.show()
                    # 用户窗口
                    else:
                        self.newWindow = MainWindow(account)
                        # self.setFixedSize(960, 700)
                        # self.usrnameSignal = pyqtSignal(account)
                        # self.usrnameSignal.emit()
                        self.newWindow.show()
                    self.close()
                else:
                    # 弹出信息框
                    msg_box = QMessageBox(QMessageBox.Warning, "警告", "当前密码错误！")
                    msg_box.show()
                    msg_box.exec_()
                    return
                    
            else:
                # 弹出信息框
                msg_box = QMessageBox(QMessageBox.Warning, "警告", "当前用户不存在！")
                msg_box.show()
                msg_box.exec_()
                return
                

"""
class ThirdWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.newWindowUI()

    def newWindowUI(self):
        self.resize(300,300)
        self.move(200,200)
"""



        
if __name__ == '__main__':
    App = QApplication(sys.argv)
    ex = FirstWindow()
    ex.show()
    sys.exit(App.exec_())
