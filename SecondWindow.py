# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import json
import usrsHashTable
import cityDict
import datetime 
import FlightImplements
import FlightInfo 
import Const 
import myClass

class SecondWindow(QWidget):
    
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 设置标题
        self.setWindowTitle("航空客运订票系统")

        # 读取用户表
        self.table = usrsHashTable.usrsHashTable()

        # 导入QListWidget的qss样式
        with open("./QSS/QListWidgetQSS.qss", 'r') as f:   
            self.list_style = f.read()

        # 设置图标
        self.setWindowIcon(QIcon('icons/plane2.png'))
      
        # 创建列表窗口，添加条目
        self.leftlist = QListWidget()
        self.leftlist.setStyleSheet(self.list_style)
        self.leftlist.insertItem(0,"查看航班信息")
        self.leftlist.insertItem(1,"添加航班信息")
        self.leftlist.insertItem(2,"修改航班信息")
        self.leftlist.insertItem(3,"查看用户信息")
        self.leftlist.insertItem(4,"添加用户信息")
        self.leftlist.insertItem(5,"修改用户信息")
        self.leftlist.insertItem(6,"详细航班信息")

        # 隐藏滚动条
        self.leftlist.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  
        self.leftlist.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 去掉边框
        self.leftlist.setFrameShape(QListWidget.NoFrame)    

        # 创建六个小控件
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()
        self.stack5 = QWidget()
        self.stack6 = QWidget()
        self.stack7 = QWidget()
        
        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack4UI()
        self.stack5UI()
        self.stack6UI()
        self.stack7UI()

        # 在QStackedWidget对象中填充了六个子控件
        self.stack = QStackedWidget(self)

        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)
        self.stack.addWidget(self.stack4)
        self.stack.addWidget(self.stack5)
        self.stack.addWidget(self.stack6)
        self.stack.addWidget(self.stack7)

        # 水平布局，添加部件到布局中
        HBox = QHBoxLayout()
        HBox.addWidget(self.leftlist)
        HBox.addStretch()
        HBox.addWidget(self.stack)

        self.setLayout(HBox)

        # list和右侧窗口的index对应绑定
        self.leftlist.currentRowChanged.connect(self.display)

######################################################################

    def stack1UI(self):
    
        # 顶层之间放置起终点和日期
        self.place_1 = QHBoxLayout()
        self.date_1 = QHBoxLayout()
        
        self.origin_1 = QComboBox()
        self.terminal_1 = QComboBox()

        self.place_1.addWidget(self.origin_1)
        arrowLabel = QLabel("到")
        arrowLabel.setStyleSheet('margin: 10px')
        self.place_1.addWidget(arrowLabel, alignment=Qt.AlignCenter)
        self.place_1.addWidget(self.terminal_1)

        
        self.year_1 = QComboBox()
        self.month_1 = QComboBox()
        self.day_1 = QComboBox()
        
        self.date_1.addWidget(self.year_1)
        self.date_1.addWidget(QLabel('年'))
        self.date_1.addStretch()
        self.date_1.addWidget(self.month_1)
        self.date_1.addWidget(QLabel('月'))
        self.date_1.addStretch()
        self.date_1.addWidget(self.day_1)
        dayLabel = QLabel('日')
        dayLabel.setStyleSheet('margin: 0px')
        self.date_1.addWidget(dayLabel)
        

        # 城市
        city_opt = cityDict.allCity
        self.origin_1.addItems(city_opt)
        self.terminal_1.addItems(city_opt)
        
        # 年的范围 2000-2050
        year_opt = []
        for i in range(2019, 2051):
            year_opt.append(str(i))
        self.year_1.addItems(year_opt)

        # 月的范围 1-12
        month_opt = []
        for i in range(1, 13):
            month_opt.append(str(i))
        self.month_1.addItems(month_opt)

        # 日的范围 默认为31
        day_opt = []
        for i in range(1, 32):
            day_opt.append(str(i))
        self.day_1.addItems(day_opt)

         # 装饰条
        decorator = QLabel()
        decorator.setPixmap(QPixmap('./pictures/sky.jpg'))
        decorator.setObjectName('decorator')
        decorator.setStyleSheet('''
            min-height: 30px; 
            max-height: 30px;
            min-width: 500px; 
            max-width: 500px;
        ''')

        # 地点和日期
        self.topMid_1 = QVBoxLayout()
        self.topMid_1.addLayout(self.place_1)
        self.topMid_1.addLayout(self.date_1)
        
        # 顶层靠左放置前一天的按钮
        self.topLeft_1 = QPushButton()
        self.topLeft_1.setText("<<\n\n前一天")
        self.topLeft_1.clicked.connect(self.getLastDay)
        self.topLeft_1.setStyleSheet('border: 0px;')
        # 顶层靠右放置后一天的按钮
        self.topRight_1 = QPushButton()
        self.topRight_1.setText(">>\n\n后一天")
        self.topRight_1.setStyleSheet('border: 0px;')
        self.topRight_1.clicked.connect(self.getTomorrow)

        # 顶层
        self.top_1 = QHBoxLayout()
        self.top_1.addWidget(self.topLeft_1)
        self.top_1.addLayout(self.topMid_1)
        self.top_1.addWidget(self.topRight_1)
        
        # 中间放置显示列表
        self.flightInfoList_1 = QListWidget()
        self.flightInfoList_1.setObjectName('flightInfoList_1')
        '''self.flightInfoList_1.setStyleSheet("QListWidget{border: 0px; border-top: 1px solid gray; }"
                                            "QListWidget::Item{padding-top:20px; padding-bottom:4px; }"
                                            "QListWidget::Item:hover{background:skyblue; }"
                                            "QListWidget::item:selected{ color:red; }"
                                            "QListWidget::item:selected:!active{border-width:0px; padding:0; background:lightgray; }"
                                            )'''
        self.flightInfoList_1.itemDoubleClicked.connect(self.detailedFlightInfo)

        # 搜索按钮
        self.search_btn_1 = QPushButton('search_btn_1')
        self.search_btn_1.setIcon(QIcon("icons/search.ico"))
        self.search_btn_1.setText("搜索")
        self.search_btn_1.setObjectName('search_btn_1')
        self.search_btn_1.clicked.connect(self.searchFlightInfo)

        # 储存当前显示列表的航班信息
        self.flightArray_1 = []
        
        # 整体使用垂直布局
        layout = QVBoxLayout()
        layout.addWidget(decorator)
        layout.addLayout(self.top_1)
        layout.addWidget(self.search_btn_1)
        layout.addWidget(self.flightInfoList_1)

        self.stack1.setLayout(layout)
        
######################################################################
        
    def stack2UI(self):

        # 实现各类标签和文本编辑框
        origin_label_2 = QLabel("起点站")
        self.origin_text_2 = QLineEdit()
        self.origin_text_2.setPlaceholderText("请输入起点站")

        terminal_label_2 = QLabel("终点站")
        self.terminal_text_2 = QLineEdit()
        self.terminal_text_2.setPlaceholderText("请输入终点站")

        flightNum_label_2 = QLabel("航班号")
        self.flightNum_text_2 = QLineEdit()
  
        planeNum_label_2 = QLabel("飞机号")
        self.planeNum_text_2 = QLineEdit()
        
        date_label_2 = QLabel("飞行日")
        date_text_2 = QHBoxLayout()

        # 年的范围 2000-2050
        self.year_2 = QComboBox()
        year_opt = []
        for i in range(2019, 2051):
            year_opt.append(str(i))
        self.year_2.addItems(year_opt)

        # 月的范围 1-12
        self.month_2 = QComboBox()
        month_opt = []
        for i in range(1, 13):
            month_opt.append(str(i))
        self.month_2.addItems(month_opt)

        # 日的范围 默认为31
        self.day_2 = QComboBox()
        day_opt = []
        for i in range(1, 32):
            day_opt.append(str(i))
        self.day_2.addItems(day_opt)

        date_text_2.addWidget(QLabel('年份'))
        date_text_2.addWidget(self.year_2)
        date_text_2.addStretch()
        date_text_2.addWidget(QLabel('月份'))
        date_text_2.addWidget(self.month_2)
        date_text_2.addStretch()
        date_text_2.addWidget(QLabel('日期'))
        date_text_2.addWidget(self.day_2)
        
        startTime_label_2 = QLabel("起飞时间")
        self.startTime_text_2 = QLineEdit()
        self.startTime_text_2.setPlaceholderText("起飞时间格式为 xx:xx")

        totalTime_label_2 = QLabel("航行时长")
        self.totalTime_text_2 = QLineEdit()
        self.totalTime_text_2.setPlaceholderText("航行时长以小时为单位")

        pasQuota_label_2 = QLabel("乘员定额")
        self.pasQuota_text_2 = QLineEdit()

        remTicketNum_label_2 = QLabel("余票量")
        self.remTicketNum_text_2 = QLineEdit()

        price_label_2 = QLabel("价格")
        self.price_text_2 = QLineEdit()
        
        # 保存和重置按钮按钮用水平布局
        okButton = QPushButton()
        okButton.setText("保存")
        okButton.clicked.connect(self.addFlightInfo)

        resetButton = QPushButton()
        resetButton.setText("重置")
        resetButton.clicked.connect(self.resetFlightInfo)

        choiceLayout = QHBoxLayout()
        choiceLayout.addStretch()
        choiceLayout.addWidget(okButton)
        choiceLayout.addStretch()
        choiceLayout.addWidget(resetButton)
        choiceLayout.addStretch()

        # 采用栅格布局添加标签文本和编辑框
        layout = QGridLayout()
        layout.setSpacing(10)

        layout.addWidget(origin_label_2, 0, 0)
        layout.addWidget(self.origin_text_2, 0, 1)

        layout.addWidget(terminal_label_2, 1, 0)
        layout.addWidget(self.terminal_text_2, 1, 1)
        
        layout.addWidget(flightNum_label_2, 2, 0)
        layout.addWidget(self.flightNum_text_2, 2, 1)
        
        layout.addWidget(planeNum_label_2, 3, 0)
        layout.addWidget(self.planeNum_text_2, 3, 1)
        
        layout.addWidget(date_label_2, 4, 0)
        layout.addLayout(date_text_2, 4, 1)
        
        layout.addWidget(startTime_label_2, 5, 0)
        layout.addWidget(self.startTime_text_2, 5, 1)
        
        layout.addWidget(totalTime_label_2, 6, 0)
        layout.addWidget(self.totalTime_text_2, 6, 1)
        
        layout.addWidget(pasQuota_label_2, 7, 0)
        layout.addWidget(self.pasQuota_text_2, 7, 1)
        
        layout.addWidget(remTicketNum_label_2, 8, 0)
        layout.addWidget(self.remTicketNum_text_2, 8, 1)

        layout.addWidget(price_label_2, 9, 0)
        layout.addWidget(self.price_text_2, 9, 1)
        
        layout.addLayout(choiceLayout, 10, 1)

        self.stack2.setLayout(layout)

######################################################################
        
    def stack3UI(self):

        self.flight_3 = []

        # 实现各类标签和文本编辑框
        origin_label_3 = QLabel("起点站")
        self.origin_text_3 = QLineEdit()
        self.origin_text_3.setReadOnly(True)
        self.origin_text_3.setPlaceholderText("起点站请从详细航班信息导入（不可修改）")

        terminal_label_3 = QLabel("终点站")
        self.terminal_text_3 = QLineEdit()
        self.terminal_text_3.setReadOnly(True)
        self.terminal_text_3.setPlaceholderText("终点站请从详细航班信息导入（不可修改）")

        flightNum_label_3 = QLabel("航班号")
        self.flightNum_text_3 = QLineEdit()
  
        planeNum_label_3 = QLabel("飞机号")
        self.planeNum_text_3 = QLineEdit()
        
        date_label_3 = QLabel("航班日期")
        self.date_text_3 = QLineEdit()
        self.date_text_3.setReadOnly(True)
        self.date_text_3.setPlaceholderText("航班日期无法修改")
        
        startTime_label_3 = QLabel("起飞时间")
        self.startTime_text_3 = QLineEdit()
        self.startTime_text_3.setPlaceholderText("起飞时间格式为 xx:xx")

        totalTime_label_3 = QLabel("航行时长")
        self.totalTime_text_3 = QLineEdit()
        self.totalTime_text_3.setPlaceholderText("航行时长以小时为单位")

        pasQuota_label_3 = QLabel("乘员定额")
        self.pasQuota_text_3 = QLineEdit()

        remTicketNum_label_3 = QLabel("余票量")
        self.remTicketNum_text_3 = QLineEdit()

        price_label_3 = QLabel("价格")
        self.price_text_3 = QLineEdit()

        state_label_3 = QLabel("状态")
        self.normalButton_3 = QRadioButton("正常")
        self.normalButton_3.setChecked(True)
        self.abnormalButton_3 = QRadioButton("异常")
        self.normalButton_3.toggled.connect(self.stateChanged)

        state_choice_3 = QHBoxLayout()
        state_choice_3.addStretch()
        state_choice_3.addWidget(self.normalButton_3)
        state_choice_3.addStretch()
        state_choice_3.addWidget(self.abnormalButton_3)
        state_choice_3.addStretch()

        remark_label_3 = QLabel("备注")
        self.remark_text_3 = QLineEdit()
        self.remark_text_3.setReadOnly(True)
        self.remark_text_3.setPlaceholderText("航班异常时请输入备注信息")

        # 保存和重置按钮按钮用水平布局
        okButton = QPushButton()
        okButton.setText("保存")
        okButton.clicked.connect(self.saveFlightInfo)

        recoverButton = QPushButton()
        recoverButton.setText("恢复")
        recoverButton.clicked.connect(self.recoverFlightInfo)

        choiceLayout = QHBoxLayout()
        choiceLayout.addStretch()
        choiceLayout.addWidget(okButton)
        choiceLayout.addStretch()
        choiceLayout.addWidget(recoverButton)
        choiceLayout.addStretch()

        # 采用栅格布局添加标签文本和编辑框
        layout = QGridLayout()
        layout.setSpacing(10)

        layout.addWidget(origin_label_3, 0, 0)
        layout.addWidget(self.origin_text_3, 0, 1)

        layout.addWidget(terminal_label_3, 1, 0)
        layout.addWidget(self.terminal_text_3, 1, 1)
        
        layout.addWidget(flightNum_label_3, 2, 0)
        layout.addWidget(self.flightNum_text_3, 2, 1)
        
        layout.addWidget(planeNum_label_3, 3, 0)
        layout.addWidget(self.planeNum_text_3, 3, 1)
        
        layout.addWidget(date_label_3, 4, 0)
        layout.addWidget(self.date_text_3, 4, 1)
        
        layout.addWidget(startTime_label_3, 5, 0)
        layout.addWidget(self.startTime_text_3, 5, 1)
        
        layout.addWidget(totalTime_label_3, 6, 0)
        layout.addWidget(self.totalTime_text_3, 6, 1)
        
        layout.addWidget(pasQuota_label_3, 7, 0)
        layout.addWidget(self.pasQuota_text_3, 7, 1)
        
        layout.addWidget(remTicketNum_label_3, 8, 0)
        layout.addWidget(self.remTicketNum_text_3, 8, 1)

        layout.addWidget(price_label_3, 9, 0)
        layout.addWidget(self.price_text_3, 9, 1)
        
        layout.addWidget(state_label_3, 10, 0)
        layout.addLayout(state_choice_3, 10, 1)

        layout.addWidget(remark_label_3, 11, 0)
        layout.addWidget(self.remark_text_3, 11, 1)
        
        layout.addLayout(choiceLayout, 12, 1)

        self.stack3.setLayout(layout)

######################################################################
    
    def stack4UI(self):

        #print(self.table.get('admin'))

        # 整体布局采用垂直布局 
        #layout = QVBoxLayout()
        layout = QGridLayout()

        # 搜索框
        self.search_text_4 = QLineEdit()
        self.search_text_4.setPlaceholderText("请输入用户名（直接空白搜索为默认查找全部用户）")
        # 连接回车信号槽
        self.search_text_4.returnPressed.connect(self.searchUser)

        # 搜索按钮
        search_btn_4 = QPushButton()
        #search_btn_4.setText("搜索")
        # 设置图标
        search_btn_4.setIcon(QIcon("icons/search.ico"))
        search_btn_4.setObjectName('search_btn_4')
        
        # 设置信号槽
        search_btn_4.clicked.connect(self.searchUser)

        # 搜索框和搜索按钮采用水平布局
        search_layout = QHBoxLayout()
        search_layout.addWidget(search_btn_4)
        search_layout.addWidget(self.search_text_4)

        # 分割线1
        devide1_label = QLabel("------------------- 搜索结果 --------------------")
        devide1_label.setAlignment(Qt.AlignCenter)
        
        # 显示列表
        self.result_list_4 = QListWidget()
        self.result_list_4.itemClicked.connect(self.displayDetails)

        # 分割线2
        devide2_label = QLabel("------------------- 详细信息 -------------------")
        devide2_label.setAlignment(Qt.AlignCenter)
        
        # 详细信息显示框
        detailedInfo_4 = QGridLayout()
        detailedInfo_4.setSpacing(10)

        usrName_label_4 = QLabel("用户名")
        self.usrName_text_4 = QLineEdit()
        self.usrName_text_4.setReadOnly(True)

        pwd_label_4 = QLabel("密码")
        self.pwd_text_4 = QLineEdit()
        self.pwd_text_4.setReadOnly(True)

        realName_label_4 = QLabel("真实姓名")
        self.realName_text_4 = QLineEdit()
        self.realName_text_4.setReadOnly(True)

        sex_label_4 = QLabel("性别")
        self.sex_text_4 = QLineEdit()
        self.sex_text_4.setReadOnly(True)

        age_label_4 = QLabel("年龄")
        self.age_text_4 = QLineEdit()
        self.age_text_4.setReadOnly(True)

        flightInfo_label_4 = QLabel("航班信息")
        self.flightInfo_text_4 = QTextBrowser()
        self.flightInfo_text_4.setReadOnly(True)
        
        # 修改和删除按钮按钮用水平布局
        reviseButton = QPushButton()
        reviseButton.setText("修改")
        reviseButton.clicked.connect(self.reviseUserInfo)

        deleteButton = QPushButton()
        deleteButton.setText("删除")
        deleteButton.clicked.connect(self.deleteUserInfo)

        choiceLayout = QHBoxLayout()
        choiceLayout.addStretch()
        choiceLayout.addWidget(reviseButton)
        choiceLayout.addStretch()
        choiceLayout.addWidget(deleteButton)
        choiceLayout.addStretch()

        layout.addWidget(search_btn_4, 0, 0)
        layout.addWidget(self.search_text_4, 0, 1)
        layout.addWidget(devide1_label, 1, 1)
        layout.addWidget(self.result_list_4, 2, 1)
        layout.addWidget(devide2_label, 3, 1)
        layout.addWidget(usrName_label_4, 4, 0)
        layout.addWidget(self.usrName_text_4, 4, 1)
        layout.addWidget(pwd_label_4, 5, 0)
        layout.addWidget(self.pwd_text_4, 5, 1)
        layout.addWidget(realName_label_4, 6, 0)
        layout.addWidget(self.realName_text_4, 6, 1)
        layout.addWidget(sex_label_4, 7, 0)
        layout.addWidget(self.sex_text_4, 7, 1)
        layout.addWidget(age_label_4, 8, 0)
        layout.addWidget(self.age_text_4, 8, 1)
        layout.addWidget(flightInfo_label_4, 9, 0)
        layout.addWidget(self.flightInfo_text_4, 9, 1)
        layout.addLayout(choiceLayout, 10, 1)
        
        layout.setSpacing(10)

        self.stack4.setLayout(layout)
        
######################################################################
        
    def stack5UI(self):

        # 整体使用网格布局
        layout = QGridLayout()

        # 实现各类标签和文本编辑框
        usrName_label_5 = QLabel("用户名")
        self.usrName_text_5 = QLineEdit()
        self.usrName_text_5.setPlaceholderText("请输入用户名")
        

        pwd_label_5 = QLabel("密码")
        self.pwd_text_5 = QLineEdit()
        self.pwd_text_5.setPlaceholderText("请输入密码")

        realName_label_5 = QLabel("真实姓名")
        self.realName_text_5 = QLineEdit()

        sex_label_5 = QLabel("性别")
        self.sex_text_5 = QLineEdit()

        age_label_5 = QLabel("年龄")
        self.age_text_5 = QLineEdit()

        # 保存按钮
        saveButton = QPushButton()
        saveButton.setText("保存")
        saveButton.clicked.connect(self.addUserInfo)

        # 重置按钮
        resetButton = QPushButton()
        resetButton.setText("重置")
        resetButton.clicked.connect(self.resetUserInfo)

        # 采用水平布局放置保存和重置按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(saveButton)
        button_layout.addStretch()
        button_layout.addWidget(resetButton)
        button_layout.addStretch()

        layout.addWidget(usrName_label_5, 0, 0)
        layout.addWidget(self.usrName_text_5, 0, 1)
        layout.addWidget(pwd_label_5, 1, 0)
        layout.addWidget(self.pwd_text_5, 1, 1)
        layout.addWidget(realName_label_5, 2, 0)
        layout.addWidget(self.realName_text_5, 2, 1)
        layout.addWidget(sex_label_5, 3, 0)
        layout.addWidget(self.sex_text_5, 3, 1)
        layout.addWidget(age_label_5, 4, 0)
        layout.addWidget(self.age_text_5, 4, 1)
        layout.addLayout(button_layout, 5, 1)

        self.stack5.setLayout(layout)
    
######################################################################
    
    def stack6UI(self):
        
         # 整体使用网格布局
        layout = QGridLayout()

        # 实现各类标签和文本编辑框
        usrName_label_6 = QLabel("用户名")
        self.usrName_text_6 = QLineEdit()
        self.usrName_text_6.setPlaceholderText("请指定用户名")
        self.usrName_text_6.setReadOnly(True)

        pwd_label_6 = QLabel("密码")
        self.pwd_text_6 = QLineEdit()

        realName_label_6 = QLabel("真实姓名")
        self.realName_text_6 = QLineEdit()

        sex_label_6 = QLabel("性别")
        self.sex_text_6 = QLineEdit()

        age_label_6 = QLabel("年龄")
        self.age_text_6 = QLineEdit()

        # 确认按钮
        saveButton = QPushButton()
        saveButton.setText("确认")
        saveButton.clicked.connect(self.saveUserInfo)

        # 取消按钮
        cancelButton = QPushButton()
        cancelButton.setText("取消")
        cancelButton.clicked.connect(self.cancelSaveRevisedUserInfo)

        # 采用水平布局放置保存和取消按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(saveButton)
        button_layout.addStretch()
        button_layout.addWidget(cancelButton)
        button_layout.addStretch()

        layout.addWidget(usrName_label_6, 0, 0)
        layout.addWidget(self.usrName_text_6, 0, 1)
        layout.addWidget(pwd_label_6, 1, 0)
        layout.addWidget(self.pwd_text_6, 1, 1)
        layout.addWidget(realName_label_6, 2, 0)
        layout.addWidget(self.realName_text_6, 2, 1)
        layout.addWidget(sex_label_6, 3, 0)
        layout.addWidget(self.sex_text_6, 3, 1)
        layout.addWidget(age_label_6, 4, 0)
        layout.addWidget(self.age_text_6, 4, 1)
        layout.addLayout(button_layout, 6, 1)

        self.stack6.setLayout(layout)

######################################################################

    def stack7UI(self):

        self.flight_7 = []
        

        # 实现各类标签和文本编辑框
        origin_label_7 = QLabel("起点站")
        self.origin_text_7 = QLineEdit()
        self.origin_text_7.setReadOnly(True)

        terminal_label_7 = QLabel("终点站")
        self.terminal_text_7 = QLineEdit()
        self.terminal_text_7.setReadOnly(True)

        flightNum_label_7 = QLabel("航班号")
        self.flightNum_text_7 = QLineEdit()
        self.flightNum_text_7.setReadOnly(True)
        
        planeNum_label_7 = QLabel("飞机号")
        self.planeNum_text_7 = QLineEdit()
        self.planeNum_text_7.setReadOnly(True)
        
        date_label_7 = QLabel("飞行日")
        self.date_text_7 = QLineEdit()
        self.date_text_7.setReadOnly(True)

        startTime_label_7 = QLabel("起飞时间")
        self.startTime_text_7 = QLineEdit()
        self.startTime_text_7.setReadOnly(True)

        totalTime_label_7 = QLabel("航行时长")
        self.totalTime_text_7 = QLineEdit()
        self.totalTime_text_7.setReadOnly(True)


        pasQuota_label_7 = QLabel("乘员定额")
        self.pasQuota_text_7 = QLineEdit()
        self.pasQuota_text_7.setReadOnly(True)
        
        remTicketNum_label_7 = QLabel("余票量")
        self.remTicketNum_text_7 = QLineEdit()
        self.remTicketNum_text_7.setReadOnly(True)

        state_label_7 = QLabel("状态")
        self.stateText_7 = QLineEdit()
        self.stateText_7.setReadOnly(True)

        remark_label_7 = QLabel("备注")
        self.remark_text_7 = QLineEdit()
        self.remark_text_7.setReadOnly(True)

        orderedList_label_7 = QLabel("乘客名单")
        self.orderedList_7 = QTextBrowser()
        self.orderedList_7.setReadOnly(True)

        waitingList_label_7 = QLabel("候补名单")
        self.waitingList_7 = QTextBrowser()
        self.waitingList_7.setReadOnly(True)

        # 修改和删除按钮按钮用水平布局
        reviseButton = QPushButton()
        reviseButton.setText("修改")
        reviseButton.clicked.connect(self.reviseFlightInfo)

        deleteButton = QPushButton()
        deleteButton.setText("删除")
        deleteButton.clicked.connect(self.deleteFlightInfo)

        reviseLayout = QHBoxLayout()
        reviseLayout.addStretch()
        reviseLayout.addWidget(reviseButton)
        reviseLayout.addStretch()
        
        deleteLayout = QHBoxLayout()
        deleteLayout.addStretch()
        deleteLayout.addWidget(deleteButton)
        deleteLayout.addStretch()
        

        # 采用栅格布局添加标签文本和编辑框
        layout = QGridLayout()
        layout.setSpacing(10)

        layout.addWidget(origin_label_7, 0, 0, 1, 1)
        layout.addWidget(self.origin_text_7, 0, 1, 1, 2)
        
        layout.addWidget(terminal_label_7, 0, 3, 1, 1)
        layout.addWidget(self.terminal_text_7, 0, 4, 1, 2)
        
        layout.addWidget(flightNum_label_7, 1, 0, 1, 1)
        layout.addWidget(self.flightNum_text_7, 1, 1, 1, 2)
        
        layout.addWidget(planeNum_label_7, 1, 3, 1, 1)
        layout.addWidget(self.planeNum_text_7, 1, 4, 1, 2)
        
        layout.addWidget(date_label_7, 2, 0, 1, 1)
        layout.addWidget(self.date_text_7, 2, 1, 1, 2)
        
        layout.addWidget(startTime_label_7, 2, 3, 1, 1)
        layout.addWidget(self.startTime_text_7, 2, 4, 1, 2)
        
        layout.addWidget(totalTime_label_7, 3, 0, 1, 1)
        layout.addWidget(self.totalTime_text_7, 3, 1, 1, 2)
        
        layout.addWidget(pasQuota_label_7, 3, 3, 1, 1)
        layout.addWidget(self.pasQuota_text_7, 3, 4, 1, 2)
        
        layout.addWidget(remTicketNum_label_7, 4, 0, 1, 1)
        layout.addWidget(self.remTicketNum_text_7, 4, 1, 1, 2)

        layout.addWidget(state_label_7, 4, 3, 1, 1)
        layout.addWidget(self.stateText_7, 4, 4, 1, 2)

        layout.addWidget(remark_label_7, 5, 0, 1, 1)
        layout.addWidget(self.remark_text_7, 5, 1, 1, 5)

        layout.addWidget(orderedList_label_7, 6, 0, 1, 1)
        layout.addWidget(self.orderedList_7, 6, 1, 1, 2)

        layout.addWidget(waitingList_label_7, 6, 3, 1, 1)
        layout.addWidget(self.waitingList_7, 6, 4, 1, 2)
        
        layout.addLayout(reviseLayout, 7, 1, 1, 1)
        layout.addLayout(deleteLayout, 7, 4, 1, 1)

        self.stack7.setLayout(layout)

######################################################################

    # 确定日期是否有效
    def confirmDay(self, year, month, day):
        # 日的范围 根据年和月判断
        date = str(year) + '-' + str(month) +'-' + str(day) 
        #print(date)
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            return True
        except:
            # 弹出信息框
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "当前日期不存在！")
            msg_box.show()
            msg_box.exec_()
            return False

    # 确定起终点是否有效
    def confirmPlace(self, origin, terminal):
        if origin in cityDict.allCity and terminal in cityDict.allCity:
            if origin == terminal:
                # 弹出信息框
                msg_box = QMessageBox(QMessageBox.Warning, "警告", "起点与终点不能相同！")
                msg_box.show()
                msg_box.exec_()
                return False
            return True
        else:
            # 弹出信息框
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "起点或终点不存在！")
            msg_box.show()
            msg_box.exec_()
            return False
      
    # 航班状态变化
    def stateChanged(self):
        print(self.normalButton_3.isChecked())
        print(self.abnormalButton_3.isChecked())
        
        if self.normalButton_3.isChecked():
            self.remark_text_3.setText("")
            self.remark_text_3.setReadOnly(True)
        else:
            self.remark_text_3.setReadOnly(False)

    # 查看详细的航班信息
    def detailedFlightInfo(self, item):
        if item.text() == '本时间段暂无航班信息':
            return
        startTime = item.text().split('\t')[0].replace('起飞时间：','')
        print(startTime)
        flight = []
        for i in self.flightArray_1:
            if startTime == i['date']['startTime']:
                self.flight_7 = i
                break

        data = self.flight_7
        print(data)
        origin = cityDict.reCityDict[data["origin"]]
        self.origin_text_7.setText(origin)
        terminal = cityDict.reCityDict[data["terminal"]]
        self.terminal_text_7.setText(terminal)
        self.flightNum_text_7.setText(data["flightNum"])     
        self.planeNum_text_7.setText(data["planeNum"])
        
        date = data["date"]
        y = str(date["year"])
        m = str(date["month"])
        d = str(date["day"])

        # 判断星期几
        week = datetime.datetime.strptime(y+'-'+m+'-'+d, "%Y-%m-%d").weekday()
        week_dict = {
            0: "一",
            1: "二",
            2: "三",
            3: "四",
            4: "五",
            5: "六",
            6: "天",
            }
        week = week_dict[week]
        
        date_sum = y + '年' + m + '月' + d + '日'     
        date_sum += ' (星期' + week + ')'
        self.date_text_7.setText(date_sum)
        
        self.startTime_text_7.setText(date["startTime"])
        date["totalTime"] = 0 if date["totalTime"]=='' else date["totalTime"]
        self.totalTime_text_7.setText(str(date["totalTime"]) + '小时')
		       
        self.pasQuota_text_7.setText(str(data["pasQuota"]))
		        
        self.remTicketNum_text_7.setText(str(data["remTicketNum"]))
        state = data["State"]
        if state == 1:
            self.stateText_7.setText("正常")       
        else:
            self.stateText_7.setText("异常")
            
        self.remark_text_7.setText(data["remark"])

        self.orderedList_7.clear()
        self.orderedList_7.append("姓名\t订票量")
        orderedList = data["orderedList"]
        for i in orderedList:
            self.orderedList_7.append(i["name"]+'\t'+str(i["ticketNum"]))

        self.waitingList_7.clear()
        self.waitingList_7.append("姓名\t订票量")
        waitingList = data["waitingList"]
        for i in waitingList:
            self.waitingList_7.append(i["name"]+'\t'+str(i["ticketNum"]))
        
        # 跳转到查看页面
        self.leftlist.setCurrentRow(6)
        self.stack.setCurrentIndex(6)
        
    # 搜索航班信息
    def searchFlightInfo(self, item):
        origin = self.origin_1.currentText()
        terminal = self.terminal_1.currentText()

        y = self.year_1.currentText()
        m = self.month_1.currentText()
        d = self.day_1.currentText()
        
        # 判断地点和日期是否有效
        if self.confirmPlace(origin, terminal) and self.confirmDay(y, m, d):
            print(origin, terminal, y, m, d)
            origin = cityDict.cityDict[self.origin_1.currentText()]
            terminal = cityDict.cityDict[self.terminal_1.currentText()]
            date = {
                'year' : y,
                'month' : m,
                'day' : d,
                'startTime' : 0,
                'totalTime' : 0
            }
            data = FlightInfo.FlightInfo(date, origin, terminal)
            self.flightArray_1 = FlightImplements.queryFlightInfo(data)
            if self.flightArray_1 != Const.FLIGHT_NOT_FOUND :
                self.flightInfoList_1.clear()
                for i in self.flightArray_1:
                    item_text = "起飞时间：" + i['date']['startTime'] + '\t' + \
                                "航班号：" + i['flightNum'] + '\t' + \
                                "余票量：" + str(i['remTicketNum'])
                    item = QListWidgetItem(item_text)
                    item.setTextAlignment(Qt.AlignHCenter)
                    self.flightInfoList_1.addItem(item)
            else:
                self.flightArray_1 = []
                self.flightInfoList_1.clear()
                item = QListWidgetItem("本时间段暂无航班信息")
                item.setTextAlignment(Qt.AlignHCenter)
                self.flightInfoList_1.addItem(item)

    # 恢复正在修改的航班信息
    def recoverFlightInfo(self):

        # 获取航班信息
        origin = self.flight_3["origin"]
        terminal = self.flight_3["terminal"]
        flightNum = self.flight_3["flightNum"]
        planeNum = self.flight_3["planeNum"]
        date = self.flight_3["date"]
        startTime = self.flight_3["date"]["startTime"]
        totalTime = self.flight_3["date"]["totalTime"]
        pasQuota = self.flight_3["pasQuota"]
        remTicketNum = self.flight_3["remTicketNum"]
        price = self.flight_3["price"]

        # 将信息更新到修改页面
        origin = cityDict.reCityDict[origin]
        terminal = cityDict.reCityDict[terminal]

        self.origin_text_3.setText(origin)
        self.terminal_text_3.setText(terminal)
        self.flightNum_text_3.setText(flightNum)
        self.planeNum_text_3.setText(planeNum)
        self.date_text_3.setText(str(date["year"]) + '-' + str(date["month"]) + '-' + str(date["day"]))
        self.startTime_text_3.setText(startTime)
        self.totalTime_text_3.setText(str(totalTime)+"小时")
        self.pasQuota_text_3.setText(str(pasQuota))
        self.remTicketNum_text_3.setText(str(remTicketNum))
        self.price_text_3.setText(str(price))
        
    # 修改航班信息
    def reviseFlightInfo(self):
        if self.flight_7 != []:
            self.flight_3 = self.flight_7    
            self.recoverFlightInfo()
            # 跳转到修改页面
            self.leftlist.setCurrentRow(2)
            self.stack.setCurrentIndex(2)
        else:
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "当前未指定航班！")
            msg_box.show()
            msg_box.exec_()

    # 删除航班信息
    def deleteFlightInfo(self):
        if self.flight_7 != []:
            flight = FlightInfo.FlightInfo(self.flight_7)
            if(FlightImplements.delFlightInfo(flight)):
                # 删除成功
                bothList = flight['orderedList'] + flight['waitingList']
                # 删除已购票的用户中的航班信息
                if not bothList == []:
                    self.table.deleteFlightInfo(self, bothList, flight)
                msg_box = QMessageBox(QMessageBox.Information, "信息", "已删除当前航班！")
                msg_box.show()
                msg_box.exec_()
                print("删除成功", flight.__dict__)
                self.flight_7 = []
        else:
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "当前未指定航班！")
            msg_box.show()
            msg_box.exec_()
          
    # 添加航班信息
    def addFlightInfo(self):
        origin = self.origin_text_2.text().strip()
        terminal = self.terminal_text_2.text().strip()
        flightNum = self.flightNum_text_2.text().strip()
        planeNum = self.planeNum_text_2.text().strip()
        year = self.year_2.currentText()
        month = self.month_2.currentText()
        day = self.day_2.currentText()
        startTime = self.startTime_text_2.text().strip()
        totalTime = self.totalTime_text_2.text().strip()
        pasQuota = self.pasQuota_text_2.text().strip()
        remTicketNum = self.remTicketNum_text_2.text().strip()
        price = self.price_text_2.text().strip()

        totalTime = 0 if totalTime=='' else int(totalTime)
        price = 0 if price=='' else int(price)

        # 起点和终点不能为空
        if origin == '' or terminal == '':
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "出发城市或目的地不能为空！")
            msg_box.show()
            msg_box.exec_()
        else:
            # 判断起终点是否有效
            if self.confirmPlace(origin, terminal):
                # 判断日期是否有效
                if self.confirmDay(year, month, day):
                    # 判断是否填写起飞时间
                    if startTime=='' or flightNum=='' or planeNum=='' or totalTime=='' or pasQuota=='' or remTicketNum=='' or price=='':
                        msg_box = QMessageBox(QMessageBox.Warning, "警告", "文本框不能为空！")
                        msg_box.show()
                        msg_box.exec_()
                        return
                    else:
                        origin = cityDict.cityDict[origin]
                        terminal = cityDict.cityDict[terminal]
                        y, m, d = int(year), int(month), int(day)
                        print(origin, terminal, y, m, d)
                        date = {
                            'year' : y,
                            'month' : m,
                            'day' : d,
                            'startTime' : 0,
                            'totalTime' : 0
                        }
                        flight = FlightInfo.FlightInfo(date, origin, terminal, startTime, totalTime,
                                            flightNum, planeNum, pasQuota, remTicketNum, price)
                        if(FlightImplements.addFlightInfo(flight)):
                            # 添加成功
                            msg_box = QMessageBox(QMessageBox.Information, "信息", "已添加当前航班！")
                            msg_box.show()
                            msg_box.exec_()
                            print("添加成功", flight.__dict__)

    # 保存修改的航班信息
    def saveFlightInfo(self):
        origin = self.origin_text_3.text().strip()
        terminal = self.terminal_text_3.text().strip()
        flightNum = self.flightNum_text_3.text().strip()
        planeNum = self.planeNum_text_3.text().strip()
        date = self.date_text_3.text()
        startTime = self.startTime_text_3.text().strip()
        totalTime = self.totalTime_text_3.text().replace('小时','')
        pasQuota = self.pasQuota_text_3.text().strip()
        remTicketNum = self.remTicketNum_text_3.text().strip()
        price = self.price_text_3.text().strip()
        state = 1
        remark = self.remark_text_3.text().strip()
        if self.abnormalButton_3.isChecked():
            state = 2
        if origin=='' or terminal=='' or date=='' or flightNum=='' or planeNum=='' or startTime=='' or \
                totalTime=='' or pasQuota=='' or remTicketNum=='' or price=='':
                # 修改成功
                msg_box = QMessageBox(QMessageBox.Warning, "警告", "文本框不能为空！")
                msg_box.show()
                msg_box.exec_()
                return
        date = date.split('-')
        y = date[0]
        m = date[1]
        d = date[2]
        if self.confirmDay(y, m, d):
            oldTicket = FlightInfo.FlightInfo(self.flight_3)
            origin = cityDict.cityDict[origin]
            terminal = cityDict.cityDict[terminal]
            date = {
                'year' : y,
                'month' : m,
                'day' : d,
                'startTime' : startTime,
                'totalTime' : totalTime
            }
            newTicket = FlightInfo.FlightInfo(date, origin, terminal, flightNum, planeNum, pasQuota, remTicketNum, price,
                                self.flight_3["orderedList"], self.flight_3["waitingList"],
                                state, remark)
            if(FlightImplements.revFlightInfo(oldTicket, newTicket)):
                # 修改成功
                msg_box = QMessageBox(QMessageBox.Information, "信息", "已修改当前航班！")
                msg_box.show()
                msg_box.exec_()
                print('修改成功')
            else:
                # 修改失败
                msg_box = QMessageBox(QMessageBox.Information, "信息", "修改当前航班失败！")
                msg_box.show()
                msg_box.exec_()
                print('修改失败')
                               
    # 重置航班信息
    def resetFlightInfo(self):
        self.origin_text_2.setText('')
        self.terminal_text_2.setText('')
        self.flightNum_text_2.setText('')
        self.planeNum_text_2.setText('')
        self.year_2.setCurrentIndex(0)
        self.month_2.setCurrentIndex(0)
        self.day_2.setCurrentIndex(0)
        self.startTime_text_2.setText('')
        self.totalTime_text_2.setText('')
        self.pasQuota_text_2.setText('')
        self.remTicketNum_text_2.setText('')

    # 搜索用户信息
    def searchUser(self):
        search_name = self.search_text_4.text().strip()
        name_list = []
        if search_name == '':
            for i in self.table.usrs:
                if i !=0 :
                    name_list.append(i["usrName"])
        else:
            print("【*】 指定搜索结果")
            print(self.table.get(search_name))
            if self.table.get(search_name) == 0:
                name_list = ["搜索不到当前用户名"]
            else:
                name_list.append(self.table.get(search_name)[1]["usrName"])
        print("【*】 最终搜索结果")
        # 列表排序
        name_list.sort()
        print(name_list)
        self.result_list_4.clear()
        self.result_list_4.addItems(name_list)

    # 显示用户详细信息
    def displayDetails(self, item):
        user = self.table.get(item.text())[1]
        print("【*】 当前用户信息")
        print(user)
        self.usrName_text_4.setText(user["usrName"])
        self.pwd_text_4.setText(user["pwd"])
        self.realName_text_4.setText(user["realName"])
        self.sex_text_4.setText(user["sex"])
        self.age_text_4.setText(str(user["age"]))

        self.flightInfo_text_4.clear()
        flightInfo = user["flightInfo"]
        for i in flightInfo:
            date = i["date"]
            #print(date)
            if i["State"] == 1:
                self.flightInfo_text_4.append("状态：正常\t"
                    + str(date["year"])+"年"+str(date["month"])+"月"+str(date["day"])+"日\t"
                    + date["startTime"]+'\t'
                    + i["origin"]+"->"+i["terminal"])    

    # 添加用户信息
    def addUserInfo(self):
        # 获取文本编辑框信息
        usrName = self.usrName_text_5.text().strip()
        pwd = self.pwd_text_5.text().strip()
        realName = self.realName_text_5.text()
        sex = self.sex_text_5.text()
        age = self.age_text_5.text()

        if age == '':
            age = '0'

        # 创建一个新的用户类
        newUserInfo = myClass.UserInfo.copy()
        newUserInfo["usrName"] = usrName
        newUserInfo["pwd"] = pwd
        newUserInfo["realName"] = realName
        newUserInfo["sex"] = sex
        newUserInfo["age"] = int(age)

        # 用户名或密码不能为空
        if usrName == '' or pwd == '':
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "用户名或密码不能为空！")
            msg_box.show()
            msg_box.exec_()
        # 写入用户表
        else:
            # 弹出信息框
            msg_box = QMessageBox(QMessageBox.Information, "信息", "已添加当前用户！")
            msg_box.show()
            msg_box.exec_()
            
            self.table.add(newUserInfo)
            print("【*】 添加用户成功")
              
    # 重置用户信息
    def resetUserInfo(self):
        self.usrName_text_5.setText('')
        self.pwd_text_5.setText('')
        self.realName_text_5.setText('')
        self.sex_text_5.setText('')
        self.age_text_5.setText('')

    # 修改用户信息
    def reviseUserInfo(self):
        self.usrName_text_6.setText(self.usrName_text_4.text())
        self.pwd_text_6.setText(self.pwd_text_4.text())
        self.realName_text_6.setText(self.realName_text_4.text())
        self.sex_text_6.setText(self.sex_text_4.text())
        self.age_text_6.setText(self.age_text_4.text())
        
        # 跳转到修改页面
        self.leftlist.setCurrentRow(5)
        self.stack.setCurrentIndex(5)

    # 删除用户信息
    def deleteUserInfo(self):
        deleteUsrName = self.usrName_text_4.text()
        if deleteUsrName == "":
            # 弹出信息框
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "当前未指定用户！")
            msg_box.show()
            msg_box.exec_()
        else:
            self.table.delete(deleteUsrName)
            print("【*】 删除用户成功")

            # 弹出信息框
            msg_box = QMessageBox(QMessageBox.Information, "信息", "已删除当前用户！")
            msg_box.show()
            msg_box.exec_()

            # 更新显示列表
            self.searchUser()

    # 保存修改的用户信息
    def saveUserInfo(self):
        if self.usrName_text_6.text() == '':
            # 弹出信息框
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "当前未指定用户！")
            msg_box.show()
            msg_box.exec_()
        else:
            # 更新用户信息
            usrName = self.usrName_text_6.text()
            pwd = self.pwd_text_6.text()
            realName = self.realName_text_6.text()
            sex = self.sex_text_6.text()
            age = self.age_text_6.text()

            if pwd=='':
                # 弹出信息框
                msg_box = QMessageBox(QMessageBox.Warning, "警告", "密码不能为空")
                msg_box.show()
                msg_box.exec_()
                return 

            newUserInfo = myClass.UserInfo.copy()
            newUserInfo["usrName"] = usrName
            newUserInfo["pwd"] = pwd
            newUserInfo["realName"] = realName
            newUserInfo["sex"] = sex
            newUserInfo["age"] = int(age)

            self.table.revise(newUserInfo)
            print("【*】 修改用户成功")

            # 弹出信息框
            msg_box = QMessageBox(QMessageBox.Information, "信息", "已修改当前用户！")
            msg_box.show()
            msg_box.exec_()
            
    # 取消修改用户信息
    def cancelSaveRevisedUserInfo(self):
        if self.usrName_text_6.text() == '':
            # 弹出信息框
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "当前未指定用户！")
            msg_box.show()
            msg_box.exec_()
        else:
            self.usrName_text_6.setText('')
            self.pwd_text_6.setText('')
            self.realName_text_6.setText('')
            self.sex_text_6.setText('')
            self.age_text_6.setText('')
   
    # 显示左侧导航条对应的栈空间
    def display(self, i):
        #设置当前可见的选项卡的索引
        self.stack.setCurrentIndex(i)

    # 更新到前一天的航班数据
    def getLastDay(self):
        origin = self.origin_1.currentText()
        terminal = self.terminal_1.currentText()

        y = self.year_1.currentText()
        m = self.month_1.currentText()
        d = self.day_1.currentText()
        # 判断日期是否合理
        if self.confirmDay(y, m, d) == False:
            return
        # 获取前一天的日期
        currentDay = datetime.datetime.strptime(y+'-'+m+'-'+d, "%Y-%m-%d")
        yesterday = currentDay + datetime.timedelta(days = -1)
        y, m, d= yesterday.year, yesterday.month, yesterday.day
        # 超出最早日期
        if y == 2018:
            # 弹出信息框
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "超出系统指定时间！")
            msg_box.show()
            msg_box.exec_()
            return
        # 判断地点和日期是否有效
        if self.confirmPlace(origin, terminal):
            # 更新年月日选项
            self.year_1.setCurrentIndex(self.year_1.findText(str(y)))
            self.month_1.setCurrentIndex(self.month_1.findText(str(m)))
            self.day_1.setCurrentIndex(self.day_1.findText(str(d)))
            print(origin, terminal, y, m, d)
            origin = cityDict.cityDict[self.origin_1.currentText()]
            terminal = cityDict.cityDict[self.terminal_1.currentText()]
            date = {
                'year' : y,
                'month' : m,
                'day' : d,
                'startTime' : 0,
                'totalTime' : 0
            }
            data = FlightInfo.FlightInfo(date, origin, terminal)
            self.flightArray_1 = FlightImplements.queryFlightInfo(data)
            if self.flightArray_1 != Const.FLIGHT_NOT_FOUND :
                self.flightInfoList_1.clear()
                for i in self.flightArray_1:
                    item_text = "起飞时间：" + i['date']['startTime'] + '\t' + \
                                "航班号：" + i['flightNum'] + '\t' + \
                                "余票量：" + str(i['remTicketNum'])
                    item = QListWidgetItem(item_text)
                    item.setTextAlignment(Qt.AlignHCenter)
                    self.flightInfoList_1.addItem(item)
            else:
                self.flightArray_1 = []
                self.flightInfoList_1.clear()
                item = QListWidgetItem("本时间段暂无航班信息")
                item.setTextAlignment(Qt.AlignHCenter)
                self.flightInfoList_1.addItem(item)
    # 更新到后一天的航班数据
    def getTomorrow(self):
        origin = self.origin_1.currentText()
        terminal = self.terminal_1.currentText()

        y = self.year_1.currentText()
        m = self.month_1.currentText()
        d = self.day_1.currentText()
        # 判断日期是否合理
        if self.confirmDay(y, m, d) == False:
            # 弹出信息框
            return
        # 获取后一天的日期
        currentDay = datetime.datetime.strptime(y+'-'+m+'-'+d, "%Y-%m-%d")
        tomorrow = currentDay + datetime.timedelta(days = 1)
        y, m, d= tomorrow.year, tomorrow.month, tomorrow.day
        # 超出最远日期
        if y == 2051:
            # 弹出信息框
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "超出系统指定时间！")
            msg_box.show()
            msg_box.exec_()
            return
        
        # 判断地点和日期是否有效
        if self.confirmPlace(origin, terminal):
            # 更新年月日选项
            self.year_1.setCurrentIndex(self.year_1.findText(str(y)))
            self.month_1.setCurrentIndex(self.month_1.findText(str(m)))
            self.day_1.setCurrentIndex(self.day_1.findText(str(d)))
            print(y,m,d)
            print(origin, terminal, y, m, d)
            origin = cityDict.cityDict[self.origin_1.currentText()]
            terminal = cityDict.cityDict[self.terminal_1.currentText()]
            date = {
                'year' : y,
                'month' : m,
                'day' : d,
                'startTime' : 0,
                'totalTime' : 0
            }
            data = FlightInfo.FlightInfo(date, origin, terminal)
            self.flightArray_1 = FlightImplements.queryFlightInfo(data)
            if self.flightArray_1 != Const.FLIGHT_NOT_FOUND :
                self.flightInfoList_1.clear()
                for i in self.flightArray_1:
                    item_text = "起飞时间：" + i['date']['startTime'] + '\t' + \
                                "航班号：" + i['flightNum'] + '\t' + \
                                "余票量：" + str(i['remTicketNum'])
                    item = QListWidgetItem(item_text)
                    item.setTextAlignment(Qt.AlignHCenter)
                    self.flightInfoList_1.addItem(item)
            else:
                self.flightArray_1 = []
                self.flightInfoList_1.clear()
                item = QListWidgetItem("本时间段暂无航班信息")
                item.setTextAlignment(Qt.AlignHCenter)
                self.flightInfoList_1.addItem(item)

    # 重写关闭函数
    def closeEvent(self, a0):
        self.hide()
        self.table.updateJson()
        print("secondWindow closed...")
        return super().closeEvent(a0)
######################################################################

        
if __name__ == '__main__':
    
    App = QApplication(sys.argv)
    ex = SecondWindow()
    ex.show()
    sys.exit(App.exec_())
