from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
import sys
import qtawesome
from FlightImplements import *
from FlightInfo import *
import usrsHashTable as uT


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, usrname):
        self.usrname = usrname
        super().__init__()
        self.init_ui()
        self.init_connect()

    def init_ui(self):
        self.setWindowTitle("航空客运订票系统")

        with open("./QSS/flatwhite.qss", 'r') as f:  # 加载样式表
            self.flatwhite_style = f.read()

        self.setFixedSize(960, 700)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.right_stack = QtWidgets.QStackedWidget()  # 创建右侧栈页面
        self.right_stack.setObjectName('right_stack')

        # 初始化搜索页面
        self.stackSearch = QtWidgets.QWidget()
        self.stackSearchUI()

        # 初始化用户信息界面
        self.stackUser = QtWidgets.QWidget()
        self.stackUserUI()

        # 向右侧栈页面中添加布局
        self.right_stack.addWidget(self.stackSearch)
        self.right_stack.addWidget(self.stackUser)

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_stack, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        # 实例化按钮
        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_visit = QtWidgets.QPushButton("")  # 空白按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮

        self.left_label_1 = QtWidgets.QPushButton("功能")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("联系与帮助")
        self.left_label_2.setObjectName('left_label')

        self.searchstack_button = QtWidgets.QPushButton(qtawesome.icon('fa.search', color='white'), "航班搜索")
        self.searchstack_button.setObjectName('left_button')
        self.user_button = QtWidgets.QPushButton(qtawesome.icon('fa.user-o', color='white'), "个人中心")
        self.user_button.setObjectName('left_button')

        # 添加左侧部件网格布局层

        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.searchstack_button, 2, 0, 1, 3)
        self.left_layout.addWidget(self.user_button, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 5, 0, 1, 3)

        # QSS美化界面
        self.QSSBeautify()

    def stackSearchUI(self):
        """(First Version)
        self.search_layout = QtWidgets.QGridLayout()
        self.stackSearch.setLayout(self.search_layout)
        # self.stackSearchIndex = self.right_stack.indexOf(self.stackSearch)

        # 搜索模块
        self.right_bar_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_widget.setLayout(self.right_bar_layout)
        self.search_icon = QtWidgets.QPushButton('搜索')
        # self.search_icon.setFont(qtawesome.font('fa', 16))
        self.search_icon.setStyleSheet(self.flatwhite_style)
        self.origin_box = QtWidgets.QComboBox()
        self.terminal_box = QtWidgets.QComboBox()
        city_opt = ['阿坝（红原）', '阿克苏', '巴彦淖尔', '包头', '北海', '北京', '博鳌', '长春', '长沙', '长治', '常州', '朝阳', '成都', '赤峰', '达州',
                    '大理', '大连', '大庆', '大同', '丹东', '稻城（亚丁）', '敦煌', '鄂尔多斯', '十堰（武当山）', '石河子', '福州', '抚远', '阜阳', '赣州',
                    '广元', '广州', '贵阳', '桂林', '哈尔滨', '哈密', '海口', '海拉尔', '杭州', '合肥', '呼和浩特', '惠州', '淮安', '和田', '黄山',
                    '揭阳（汕头）', '晋江泉州', '井冈山', '景德镇', '佳木斯', '九寨沟', '建三江', '库尔勒', '克拉玛依', '昆明', '喀什', '兰州', '丽江', '林芝',
                    '柳州', '六盘水', '泸州', '临汾', '拉萨', '满洲里', '茅台', '牡丹江', '绵阳', '南昌', '南京', '南宁', '南通', '宁波', '攀枝花',
                    '齐齐哈尔', '青岛', '三亚', '石家庄', '松原', '上海（虹桥）', '上海（浦东）', '深圳', '沈阳', '台州（黄岩）', '太原', '天津', '通化', '通辽',
                    '吐鲁番', '万州', '威海', '温州', '乌鲁木齐', '无锡', '乌海', '武汉', '乌兰浩特', '乌兰察布', '西安', '西昌', '西宁', '锡林浩特', '厦门',
                    '徐州', '烟台', '延吉', '盐城', '扬州', '伊宁', '宜宾', '宜昌', '义乌', '银川', '榆林', '运城', '湛江', '张家界', '郑州', '重庆',
                    '珠海', '遵义']
        self.origin_box.addItems(city_opt)
        self.terminal_box.addItems(city_opt)
        # self.right_bar_widget_search_input.setPlaceholderText("输入航班号，回车进行搜索")

        self.right_bar_layout.addWidget(self.search_icon, 0, 3)
        self.right_bar_layout.addWidget(self.origin_box, 0, 1)
        self.right_bar_layout.addWidget(self.terminal_box, 0, 2)

        self.search_layout.addWidget(self.right_bar_widget, 0, 0, 1, 9)
        """
        # 整体使用网格布局
        self.search_layout = QtWidgets.QGridLayout()

        # 初始化地名
        city_opt = ['阿坝（红原）', '阿克苏', '巴彦淖尔', '包头', '北海', '北京', '博鳌', '长春', '长沙', '长治', '常州', '朝阳', '成都', '赤峰', '达州',
                    '大理', '大连', '大庆', '大同', '丹东', '稻城（亚丁）', '敦煌', '鄂尔多斯', '十堰（武当山）', '石河子', '福州', '抚远', '阜阳', '赣州',
                    '广元', '广州', '贵阳', '桂林', '哈尔滨', '哈密', '海口', '海拉尔', '杭州', '合肥', '呼和浩特', '惠州', '淮安', '和田', '黄山',
                    '揭阳（汕头）', '晋江', '井冈山', '景德镇', '佳木斯', '九寨沟', '建三江', '库尔勒', '克拉玛依', '昆明', '喀什', '兰州', '丽江', '林芝',
                    '柳州', '六盘水', '泸州', '临汾', '拉萨', '满洲里', '茅台', '牡丹江', '绵阳', '南昌', '南京', '南宁', '南通', '宁波', '攀枝花',
                    '齐齐哈尔', '青岛', '三亚', '石家庄', '松原', '上海', '深圳', '沈阳', '台州（黄岩）', '太原', '天津', '通化', '通辽',
                    '吐鲁番', '万州', '威海', '温州', '乌鲁木齐', '无锡', '乌海', '武汉', '乌兰浩特', '乌兰察布', '西安', '西昌', '西宁', '锡林浩特', '厦门',
                    '徐州', '烟台', '延吉', '盐城', '扬州', '伊宁', '宜宾', '宜昌', '义乌', '银川', '榆林', '运城', '湛江', '张家界', '郑州', '重庆',
                    '珠海', '遵义']

        # 初始化地名与拼音对应字典
        city_pin = ['Aba', 'Akesu', 'Bayannaoer', 'Baotou', 'Beihai', 'Beijing', 'Boao', 'Changchun', 'Changsha',
                  'Changzhi', 'Changzhou', 'Chaoyang', 'Chengdu', 'Chifeng', 'Dazhou', 'Dali', 'Dalian', 'Daqing',
                  'Datong', 'Dandong', 'Dacheng', 'Dunhuang', 'Erdos', 'Shiyan', 'Shihezi', 'Fuzhou', 'Fuyuan',
                  'Gaoyang', 'Ganzhou', 'Guangyuan', 'Guangzhou', 'Guiyang', 'Guilin', 'Harbin', 'Hami', 'Haikou',
                  'Hailar ', 'Hangzhou', 'Hefei', 'Hohhot', 'Huizhou', 'Huai', 'Hetian', 'Huangshan', 'Jieyang',
                  'Jinjiang', 'Jinggangshan', 'Jingdezhen', 'Jiamusi', 'Jiuzhaigou', 'Jiansanjiang', 'Korla',
                  'Kelamayi', 'Kunming', 'Kashi', 'Lanzhou', 'Lijiang', 'Linzhi', 'Liuzhou', 'Six panshui', 'Zhangzhou',
                  'Linfen', 'Lhasa', 'Manzhouli', 'Maotai', 'Mudanjiang', 'Mianyang', 'Nanchang', 'Nanjing', 'Nanning',
                  'Nantong', 'Ningbo', 'Panzhihua', 'Qiqihar ', 'Qingdao', 'Sanya', 'Shijiazhuang', 'Songyuan',
                  'Shanghai', 'Shenzhen', 'Shenyang', 'Taizhou', 'Taiyuan', 'Tianjin', 'Tonghua', 'Tongliao', 'Tulufan',
                  'Wanzhou', 'Weihai', 'Wenzhou', 'Wulumuqi', 'Wuxi', 'Wuhai', 'Wuhan', 'Ulanhot', 'Ulanchabu', 'Xian',
                  'Xichang', 'Xining', 'Xilinhot', 'Xiamen', 'Xuzhou ', 'Yantai', 'Yanji', 'Yancheng', 'Yangzhou',
                  'Yining', 'Yibin', 'Yichang', 'Yiwu', 'Yinchuan', 'Yulin', 'Yuncheng', 'Zhanjiang', 'Zhangjiajie',
                  'Zhengzhou', 'Chongqing', 'Zhuhai', 'Zunyi']

        self.city_dict = dict(zip(city_opt, city_pin))

        # 出发地标签和下拉列表
        self.origin_label = QtWidgets.QLabel()
        self.origin_label.setText('出发地')
        self.origin_combobox = QtWidgets.QComboBox()
        self.origin_combobox.addItems(city_opt)

        # 目的地标签和下拉列表
        self.terminal_label = QtWidgets.QLabel()
        self.terminal_label.setText('目的地')
        self.terminal_combobox = QtWidgets.QComboBox()
        self.terminal_combobox.addItems(city_opt)

        # 初始化年份标签
        year = ['2019', '2020', '2021', '2022']
        month = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        day = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
               '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

        # 年份标签和下拉列表
        self.year_label = QtWidgets.QLabel()
        self.year_label.setText('年')
        self.year_combobox = QtWidgets.QComboBox()
        self.year_combobox.addItems(year)

        # 月份标签和下拉列表
        self.month_label = QtWidgets.QLabel()
        self.month_label.setText('月')
        self.month_combobox = QtWidgets.QComboBox()
        self.month_combobox.addItems(month)

        # 日期标签和下拉列表
        self.day_label = QtWidgets.QLabel()
        self.day_label.setText('日')
        self.day_combobox = QtWidgets.QComboBox()
        self.day_combobox.addItems(day)

        # 出发时间标签和水平布局
        self.date_label = QtWidgets.QLabel()
        self.date_label.setText('出发时间')
        self.date_layout = QtWidgets.QHBoxLayout()

        # 用水平布局摆放年月日
        self.date_layout.addWidget(self.year_label)
        self.date_layout.addWidget(self.year_combobox)
        self.date_layout.addStretch()
        self.date_layout.addWidget(self.month_label)
        self.date_layout.addWidget(self.month_combobox)
        self.date_layout.addStretch()
        self.date_layout.addWidget(self.day_label)
        self.date_layout.addWidget(self.day_combobox)

        # 搜索按钮
        self.search_button = QtWidgets.QPushButton()
        self.search_button.setText('搜索')

        # 前一天按钮
        self.last_day_button = QtWidgets.QPushButton()
        self.last_day_button.setText('前一天')

        # 后一天按钮
        self.next_day_button = QtWidgets.QPushButton()
        self.next_day_button.setText('后一天')

        # 航班信息标签
        self.flight_label = QtWidgets.QLabel()
        self.flight_label.setText('航班信息')

        # 第一条航班信息，采用网格布局
        self.flight_1 = QtWidgets.QGridLayout()
        self.start_time_1 = QtWidgets.QLabel()
        # 起飞时间
        self.start_time_1.setText('7:00')
        self.separator_1 = QtWidgets.QLabel()
        # 分隔符
        self.separator_1.setText('->')
        self.end_time_1 = QtWidgets.QLabel()
        # 到达时间
        self.end_time_1.setText('8:50')
        self.price_1 = QtWidgets.QLabel()
        # 航班价格
        self.price_1.setText('￥1000')
        self.order_1 = QtWidgets.QPushButton()
        # 购买按钮
        self.order_1.setText('购买')
        # 向第一条航班信息添加子控件
        self.flight_1.addWidget(self.start_time_1, 0, 0, 1, 1)
        self.flight_1.addWidget(self.separator_1, 0, 1, 1, 1)
        self.flight_1.addWidget(self.end_time_1, 0, 2, 1, 4)
        self.flight_1.addWidget(self.price_1, 0, 6, 1, 1)
        self.flight_1.addWidget(self.order_1, 0, 7, 1, 1)

        # 第二条航班信息，采用网格布局
        self.flight_2 = QtWidgets.QGridLayout()
        self.start_time_2 = QtWidgets.QLabel()
        # 起飞时间
        self.start_time_2.setText('9:00')
        self.separator_2 = QtWidgets.QLabel()
        # 分隔符
        self.separator_2.setText('->')
        self.end_time_2 = QtWidgets.QLabel()
        # 到达时间
        self.end_time_2.setText('10:50')
        self.price_2 = QtWidgets.QLabel()
        # 航班价格
        self.price_2.setText('￥1100')
        self.order_2 = QtWidgets.QPushButton()
        # 购买按钮
        self.order_2.setText('购买')
        # 向第二条航班信息添加子控件
        self.flight_2.addWidget(self.start_time_2, 0, 0, 1, 1)
        self.flight_2.addWidget(self.separator_2, 0, 1, 1, 1)
        self.flight_2.addWidget(self.end_time_2, 0, 2, 1, 4)
        self.flight_2.addWidget(self.price_2, 0, 6, 1, 1)
        self.flight_2.addWidget(self.order_2, 0, 7, 1, 1)

        # 第三条航班信息，采用网格布局
        self.flight_3 = QtWidgets.QGridLayout()
        self.start_time_3 = QtWidgets.QLabel()
        # 起飞时间
        self.start_time_3.setText('11:00')
        self.separator_3 = QtWidgets.QLabel()
        # 分隔符
        self.separator_3.setText('->')
        self.end_time_3 = QtWidgets.QLabel()
        # 到达时间
        self.end_time_3.setText('12:50')
        self.price_3 = QtWidgets.QLabel()
        # 航班价格
        self.price_3.setText('￥900')
        self.order_3 = QtWidgets.QPushButton()
        # 购买按钮
        self.order_3.setText('购买')
        # 向第三条航班信息添加子控件
        self.flight_3.addWidget(self.start_time_3, 0, 0, 1, 1)
        self.flight_3.addWidget(self.separator_3, 0, 1, 1, 1)
        self.flight_3.addWidget(self.end_time_3, 0, 2, 1, 4)
        self.flight_3.addWidget(self.price_3, 0, 6, 1, 1)
        self.flight_3.addWidget(self.order_3, 0, 7, 1, 1)

        # 第四条航班信息，采用网格布局
        self.flight_4 = QtWidgets.QGridLayout()
        self.start_time_4 = QtWidgets.QLabel()
        # 起飞时间
        self.start_time_4.setText('14:00')
        self.separator_4 = QtWidgets.QLabel()
        # 分隔符
        self.separator_4.setText('->')
        self.end_time_4 = QtWidgets.QLabel()
        # 到达时间
        self.end_time_4.setText('15:50')
        self.price_4 = QtWidgets.QLabel()
        # 航班价格
        self.price_4.setText('￥1000')
        self.order_4 = QtWidgets.QPushButton()
        # 购买按钮
        self.order_4.setText('购买')
        # 向第四条航班信息添加子控件
        self.flight_4.addWidget(self.start_time_4, 0, 0, 1, 1)
        self.flight_4.addWidget(self.separator_4, 0, 1, 1, 1)
        self.flight_4.addWidget(self.end_time_4, 0, 2, 1, 4)
        self.flight_4.addWidget(self.price_4, 0, 6, 1, 1)
        self.flight_4.addWidget(self.order_4, 0, 7, 1, 1)

        # 第五条航班信息，采用网格布局
        self.flight_5 = QtWidgets.QGridLayout()
        self.start_time_5 = QtWidgets.QLabel()
        # 起飞时间
        self.start_time_5.setText('16:00')
        self.separator_5 = QtWidgets.QLabel()
        # 分隔符
        self.separator_5.setText('->')
        self.end_time_5 = QtWidgets.QLabel()
        # 到达时间
        self.end_time_5.setText('17:50')
        self.price_5 = QtWidgets.QLabel()
        # 航班价格
        self.price_5.setText('￥1100')
        self.order_5 = QtWidgets.QPushButton()
        # 购买按钮
        self.order_5.setText('购买')
        # 向第五条航班信息添加子控件
        self.flight_5.addWidget(self.start_time_5, 0, 0, 1, 1)
        self.flight_5.addWidget(self.separator_5, 0, 1, 1, 1)
        self.flight_5.addWidget(self.end_time_5, 0, 2, 1, 4)
        self.flight_5.addWidget(self.price_5, 0, 6, 1, 1)
        self.flight_5.addWidget(self.order_5, 0, 7, 1, 1)

        # 前一页按钮
        self.last_page_button = QtWidgets.QPushButton()
        self.last_page_button.setText('前一页')
        self.last_page_button.setObjectName('search_last')
        self.last_page_button.setEnabled(False)  # 设置上一页不可用

        # 后一页按钮
        self.next_page_button = QtWidgets.QPushButton()
        self.next_page_button.setText('后一页')
        self.next_page_button.setObjectName('search_next')
        self.next_page_button.setEnabled(False)  # 设置下一页不可用

        # 向总布局添加子控件
        self.search_layout.addWidget(self.origin_label, 0, 0, 1, 1)
        self.search_layout.addWidget(self.origin_combobox, 0, 1, 1, 2)
        self.search_layout.addWidget(self.terminal_label, 1, 0, 1, 1)
        self.search_layout.addWidget(self.terminal_combobox, 1, 1, 1, 2)
        self.search_layout.addWidget(self.date_label, 2, 0, 1, 1)
        self.search_layout.addLayout(self.date_layout, 2, 1, 1, 2)
        self.search_layout.addWidget(self.last_day_button, 3, 0, 1, 1)
        self.search_layout.addWidget(self.search_button, 3, 1, 1, 1)
        self.search_layout.addWidget(self.next_day_button, 3, 2, 1, 1)
        self.search_layout.addWidget(self.flight_label, 4, 1, 1, 1)
        self.search_layout.addLayout(self.flight_1, 5, 0, 2, 3)
        self.search_layout.addLayout(self.flight_2, 7, 0, 2, 3)
        self.search_layout.addLayout(self.flight_3, 9, 0, 2, 3)
        self.search_layout.addLayout(self.flight_4, 11, 0, 2, 3)
        self.search_layout.addLayout(self.flight_5, 13, 0, 2, 3)
        self.search_layout.addWidget(self.last_page_button, 15, 0, 1, 1)
        self.search_layout.addWidget(self.next_page_button, 15, 2, 1, 1)

        self.stackSearch.setLayout(self.search_layout)
        self.stackSearch.setStyleSheet(self.flatwhite_style)

    def stackUserUI(self):
        # self.stackUserIndex = self.right_stack.indexOf(self.stackUser)
        # 设置窗口大小
        # self.setFixedSize(520, 440)

        # 整体使用网格布局
        self.personal_layout = QtWidgets.QGridLayout()

        # 获取用户信息
        self.User = uT.usrsHashTable().get(self.usrname)[1]

        # 头像
        self.head = QtWidgets.QLabel()
        self.head.setGeometry(0, 0, 30, 30)
        self.head.setPixmap(QtGui.QPixmap('./pictures/head0.jpg'))
        self.head.setStyleSheet(self.flatwhite_style)

        # 用户名
        self.user_name_babel = QtWidgets.QLabel()
        self.user_name_babel.setText('账户')
        self.user_name_babel.setStyleSheet(self.flatwhite_style)
        self.user_name_text = QtWidgets.QLineEdit()
        self.user_name_text.setText(self.User['usrName'])
        # self.user_name_text.setText('440*********5678')
        self.user_name_text.setStyleSheet(self.flatwhite_style)
        self.user_name_text.setReadOnly(True)

        # 姓名
        self.real_name_babel = QtWidgets.QLabel()
        self.real_name_babel.setText('姓名')
        self.real_name_babel.setStyleSheet(self.flatwhite_style)
        self.real_name_text = QtWidgets.QLineEdit()
        self.real_name_text.setText(self.User['realName'])
        # self.real_name_text.setText("王小明")
        self.real_name_text.setReadOnly(True)
        self.real_name_text.setStyleSheet(self.flatwhite_style)

        # 年龄
        self.age_babel = QtWidgets.QLabel()
        self.age_babel.setText('年龄')
        self.age_babel.setStyleSheet(self.flatwhite_style)
        self.age_text = QtWidgets.QLineEdit()
        self.age_text.setText(str(self.User['age']))
        # self.age_text.setText("20")
        self.age_text.setReadOnly(True)
        self.age_text.setStyleSheet(self.flatwhite_style)

        # 用网格布局放置用户名、姓名和年龄信息
        self.info_layout = QtWidgets.QGridLayout()
        self.info_layout.addWidget(self.user_name_babel, 0, 0, 1, 1)
        self.info_layout.addWidget(self.user_name_text, 0, 1, 1, 2)
        self.info_layout.addWidget(self.real_name_babel, 1, 0, 1, 1)
        self.info_layout.addWidget(self.real_name_text, 1, 1, 1, 2)
        self.info_layout.addWidget(self.age_babel, 2, 0, 1, 1)
        self.info_layout.addWidget(self.age_text, 2, 1, 1, 2)

        # 个人订单标签
        self.order_list_label = QtWidgets.QLabel()
        self.order_list_label.setText('个人订单')
        self.order_list_label.setStyleSheet(self.flatwhite_style)

        # 第一条航班信息，采用网格布局
        self.p_flight_1 = QtWidgets.QGridLayout()
        self.p_start_time_1 = QtWidgets.QLabel()
        self.p_start_time_1.setStyleSheet(self.flatwhite_style)
        # 起飞时间
        self.p_start_time_1.setText('7:00')
        self.p_separator_1 = QtWidgets.QLabel()
        self.p_separator_1.setStyleSheet(self.flatwhite_style)
        # 分隔符
        self.p_separator_1.setText('----->')
        self.p_end_time_1 = QtWidgets.QLabel()
        self.p_end_time_1.setStyleSheet(self.flatwhite_style)
        # 到达时间
        self.p_end_time_1.setText('8:50')
        self.p_price_1 = QtWidgets.QLabel()
        self.p_price_1.setStyleSheet(self.flatwhite_style)
        # 航班价格
        self.p_price_1.setText('￥1000')
        # 航班起点
        self.p_origin_1 = QtWidgets.QLabel()
        self.p_origin_1.setText('广州')
        self.p_origin_1.setStyleSheet(self.flatwhite_style)
        # 航班终点
        self.p_terminal_1 = QtWidgets.QLabel()
        self.p_terminal_1.setText('上海')
        self.p_terminal_1.setStyleSheet(self.flatwhite_style)
        self.p_refund_1 = QtWidgets.QPushButton()
        self.p_refund_1.setStyleSheet(self.flatwhite_style)
        # 取消按钮
        self.p_refund_1.setText('取消')
        """
        # 航班号
        self.p_flight_num_1 = QtWidgets.QLabel()
        self.p_flight_num_1.setText('SN5127')
        self.p_flight_num_1.setStyleSheet(self.flatwhite_style)
        """
        # 向第一条航班信息添加子控件
        self.p_flight_1.addWidget(self.p_start_time_1, 0, 0, 1, 1)
        self.p_flight_1.addWidget(self.p_separator_1, 0, 1, 1, 1)
        self.p_flight_1.addWidget(self.p_end_time_1, 0, 2, 1, 1)
        self.p_flight_1.addWidget(self.p_origin_1, 0, 3, 1, 1)
        self.p_flight_1.addWidget(self.p_terminal_1, 0, 4, 1, 1)
        self.p_flight_1.addWidget(self.p_price_1, 0, 5, 1, 1)
        self.p_flight_1.addWidget(self.p_refund_1, 0, 6, 1, 1)

        # 第二条航班信息，采用网格布局
        self.p_flight_2 = QtWidgets.QGridLayout()
        self.p_start_time_2 = QtWidgets.QLabel()
        self.p_start_time_2.setStyleSheet(self.flatwhite_style)
        # 起飞时间
        self.p_start_time_2.setText('9:00')
        self.p_separator_2 = QtWidgets.QLabel()
        self.p_separator_2.setStyleSheet(self.flatwhite_style)
        # 分隔符
        self.p_separator_2.setText('->')
        self.p_end_time_2 = QtWidgets.QLabel()
        self.p_end_time_2.setStyleSheet(self.flatwhite_style)
        # 到达时间
        self.p_end_time_2.setText('10:50')
        self.p_price_2 = QtWidgets.QLabel()
        self.p_price_2.setStyleSheet(self.flatwhite_style)
        # 航班价格
        self.p_price_2.setText('￥1100')
        self.p_origin_2 = QtWidgets.QLabel()
        self.p_origin_2.setText('广州')
        self.p_origin_2.setStyleSheet(self.flatwhite_style)
        # 航班起点
        self.p_terminal_2 = QtWidgets.QLabel()
        self.p_terminal_2.setText('上海')
        self.p_terminal_2.setStyleSheet(self.flatwhite_style)
        # 航班终点
        self.p_refund_2 = QtWidgets.QPushButton()
        self.p_refund_2.setStyleSheet(self.flatwhite_style)
        # 取消按钮
        self.p_refund_2.setText('取消')
        # 向第二条航班信息添加子控件
        self.p_flight_2.addWidget(self.p_start_time_2, 0, 0, 1, 1)
        self.p_flight_2.addWidget(self.p_separator_2, 0, 1, 1, 1)
        self.p_flight_2.addWidget(self.p_end_time_2, 0, 2, 1, 1)
        self.p_flight_2.addWidget(self.p_origin_2, 0, 3, 1, 1)
        self.p_flight_2.addWidget(self.p_terminal_2, 0, 4, 1, 1)
        self.p_flight_2.addWidget(self.p_price_2, 0, 5, 1, 1)
        self.p_flight_2.addWidget(self.p_refund_2, 0, 6, 1, 1)

        # 第三条航班信息，采用网格布局
        self.p_flight_3 = QtWidgets.QGridLayout()
        self.p_start_time_3 = QtWidgets.QLabel()
        self.p_start_time_3.setStyleSheet(self.flatwhite_style)
        # 起飞时间
        self.p_start_time_3.setText('11:00')
        self.p_separator_3 = QtWidgets.QLabel()
        self.p_separator_3.setStyleSheet(self.flatwhite_style)
        # 分隔符
        self.p_separator_3.setText('->')
        self.p_end_time_3 = QtWidgets.QLabel()
        self.p_end_time_3.setStyleSheet(self.flatwhite_style)
        # 到达时间
        self.p_end_time_3.setText('12:50')
        self.p_price_3 = QtWidgets.QLabel()
        self.p_price_3.setStyleSheet(self.flatwhite_style)
        # 航班价格
        self.p_price_3.setText('￥900')
        self.p_origin_3 = QtWidgets.QLabel()
        self.p_origin_3.setText('广州')
        self.p_origin_3.setStyleSheet(self.flatwhite_style)
        # 航班起点
        self.p_terminal_3 = QtWidgets.QLabel()
        self.p_terminal_3.setText('上海')
        self.p_terminal_3.setStyleSheet(self.flatwhite_style)
        # 航班终点
        self.p_refund_3 = QtWidgets.QPushButton()
        self.p_refund_3.setStyleSheet(self.flatwhite_style)
        # 取消按钮
        self.p_refund_3.setText('取消')
        # 向第三条航班信息添加子控件
        self.p_flight_3.addWidget(self.p_start_time_3, 0, 0, 1, 1)
        self.p_flight_3.addWidget(self.p_separator_3, 0, 1, 1, 1)
        self.p_flight_3.addWidget(self.p_end_time_3, 0, 2, 1, 1)
        self.p_flight_3.addWidget(self.p_origin_3, 0, 3, 1, 1)
        self.p_flight_3.addWidget(self.p_terminal_3, 0, 4, 1, 1)
        self.p_flight_3.addWidget(self.p_price_3, 0, 5, 1, 1)
        self.p_flight_3.addWidget(self.p_refund_3, 0, 6, 1, 1)

        # 第四条航班信息，采用网格布局
        self.p_flight_4 = QtWidgets.QGridLayout()
        self.p_start_time_4 = QtWidgets.QLabel()
        self.p_start_time_4.setStyleSheet(self.flatwhite_style)
        # 起飞时间
        self.p_start_time_4.setText('14:00')
        self.p_separator_4 = QtWidgets.QLabel()
        self.p_separator_4.setStyleSheet(self.flatwhite_style)
        # 分隔符
        self.p_separator_4.setText('->')
        self.p_end_time_4 = QtWidgets.QLabel()
        self.p_end_time_4.setStyleSheet(self.flatwhite_style)
        # 到达时间
        self.p_end_time_4.setText('15:50')
        self.p_price_4 = QtWidgets.QLabel()
        self.p_price_4.setStyleSheet(self.flatwhite_style)
        # 航班价格
        self.p_price_4.setText('￥1000')
        self.p_origin_4 = QtWidgets.QLabel()
        self.p_origin_4.setText('广州')
        self.p_origin_4.setStyleSheet(self.flatwhite_style)
        # 航班起点
        self.p_terminal_4 = QtWidgets.QLabel()
        self.p_terminal_4.setText('上海')
        self.p_terminal_4.setStyleSheet(self.flatwhite_style)
        # 航班终点
        self.p_refund_4 = QtWidgets.QPushButton()
        self.p_refund_4.setStyleSheet(self.flatwhite_style)
        # 取消按钮
        self.p_refund_4.setText('取消')
        # 向第四条航班信息添加子控件
        self.p_flight_4.addWidget(self.p_start_time_4, 0, 0, 1, 1)
        self.p_flight_4.addWidget(self.p_separator_4, 0, 1, 1, 1)
        self.p_flight_4.addWidget(self.p_end_time_4, 0, 2, 1, 1)
        self.p_flight_4.addWidget(self.p_origin_4, 0, 3, 1, 1)
        self.p_flight_4.addWidget(self.p_terminal_4, 0, 4, 1, 1)
        self.p_flight_4.addWidget(self.p_price_4, 0, 5, 1, 1)
        self.p_flight_4.addWidget(self.p_refund_4, 0, 6, 1, 1)

        # 第五条航班信息，采用网格布局
        self.p_flight_5 = QtWidgets.QGridLayout()
        self.p_start_time_5 = QtWidgets.QLabel()
        self.p_start_time_5.setStyleSheet(self.flatwhite_style)
        # 起飞时间
        self.p_start_time_5.setText('16:00')
        self.p_separator_5 = QtWidgets.QLabel()
        self.p_separator_5.setStyleSheet(self.flatwhite_style)
        # 分隔符
        self.p_separator_5.setText('->')
        self.p_end_time_5 = QtWidgets.QLabel()
        self.p_end_time_5.setStyleSheet(self.flatwhite_style)
        # 到达时间
        self.p_end_time_5.setText('17:50')
        self.p_price_5 = QtWidgets.QLabel()
        self.p_price_5.setStyleSheet(self.flatwhite_style)
        # 航班价格
        self.p_price_5.setText('￥1100')
        self.p_origin_5 = QtWidgets.QLabel()
        self.p_origin_5.setText('广州')
        self.p_origin_5.setStyleSheet(self.flatwhite_style)
        # 航班起点
        self.p_terminal_5 = QtWidgets.QLabel()
        self.p_terminal_5.setText('上海')
        self.p_terminal_5.setStyleSheet(self.flatwhite_style)
        # 航班终点
        self.p_refund_5 = QtWidgets.QPushButton()
        self.p_refund_5.setStyleSheet(self.flatwhite_style)
        # 取消按钮
        self.p_refund_5.setText('取消')
        # 向第五条航班信息添加子控件
        self.p_flight_5.addWidget(self.p_start_time_5, 0, 0, 1, 1)
        self.p_flight_5.addWidget(self.p_separator_5, 0, 1, 1, 1)
        self.p_flight_5.addWidget(self.p_end_time_5, 0, 2, 1, 1)
        self.p_flight_5.addWidget(self.p_origin_5, 0, 3, 1, 1)
        self.p_flight_5.addWidget(self.p_terminal_5, 0, 4, 1, 1)
        self.p_flight_5.addWidget(self.p_price_5, 0, 5, 1, 1)
        self.p_flight_5.addWidget(self.p_refund_5, 0, 6, 1, 1)

        # 上一页按钮
        self.p_last_pape_button = QtWidgets.QPushButton()
        self.p_last_pape_button.setText('上一页')
        self.p_last_pape_button.setStyleSheet(self.flatwhite_style)
        self.p_last_pape_button.setObjectName('user_last')

        # 下一页按钮
        self.p_next_pape_button = QtWidgets.QPushButton()
        self.p_next_pape_button.setText('下一页')
        self.p_next_pape_button.setStyleSheet(self.flatwhite_style)
        self.p_next_pape_button.setObjectName('user_next')

        # 向总布局添加子控件
        self.personal_layout.addWidget(self.head, 0, 0, 1, 1)
        self.personal_layout.addLayout(self.info_layout, 0, 2, 1, 1)
        self.personal_layout.addWidget(self.order_list_label, 1, 0, 1, 12)
        self.personal_layout.addLayout(self.p_flight_1, 2, 0, 2, 12)
        self.personal_layout.addLayout(self.p_flight_2, 4, 0, 2, 12)
        self.personal_layout.addLayout(self.p_flight_3, 6, 0, 2, 12)
        self.personal_layout.addLayout(self.p_flight_4, 8, 0, 2, 12)
        self.personal_layout.addLayout(self.p_flight_5, 10, 0, 2, 12)
        self.personal_layout.addWidget(self.p_last_pape_button, 12, 10, 1, 1)
        self.personal_layout.addWidget(self.p_next_pape_button, 12, 11, 1, 1)
        self.stackUser.setLayout(self.personal_layout)

    def init_connect(self):
        self.searchstack_button.clicked.connect(self.buttonclicked)
        self.user_button.clicked.connect(self.buttonclicked)
        self.left_close.clicked.connect(self.close)
        self.left_visit.clicked.connect(self.change_windows)
        self.left_mini.clicked.connect(self.showMinimized)
        self.search_button.clicked.connect(self.searchFlight)
        self.next_page_button.clicked.connect(self.nextPage)
        self.last_page_button.clicked.connect(self.prevPage)
        self.last_day_button.clicked.connect(self.test)

    def change_windows(self):
        """
        用于最大化和最小化窗口
        """
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def QSSBeautify(self):
        """
        美化界面
        """
        # 左侧小圆点
        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        # 左侧菜单
        self.left_widget.setStyleSheet('''
                    QPushButton{border:none;color:white;}
                    QPushButton#left_label{
                        border:none;
                        border-bottom:1px solid white;
                        font-size:18px;
                        font-weight:700;
                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                    }
                    QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
                    QWidget#left_widget{
                    background:gray;
                    border-top:1px solid white;
                    border-bottom:1px solid white;
                    border-left:1px solid white;
                    border-top-left-radius:10px;
                    border-bottom-left-radius:10px;
                    }
                    ''')

        # 搜索框
        # self.origin_box.setStyleSheet(self.flatwhite_style)
        # self.terminal_box.setStyleSheet(self.flatwhite_style)

        # 右侧总改
        self.right_stack.setStyleSheet('''
                    QWidget#right_stack{
                        color:#232C51;
                        background:white;
                        border-top:1px solid darkGray;
                        border-bottom:1px solid darkGray;
                        border-right:1px solid darkGray;
                        border-top-right-radius:10px;
                        border-bottom-right-radius:10px;
                    }
                    QLabel#right_lable{
                        border:none;
                        font-size:16px;
                        font-weight:700;
                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                    }
                ''')

        # 窗口背景透明
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # 去除窗口内缝隙
        self.main_layout.setSpacing(0)

        # 去除窗口边框
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

    def buttonclicked(self):
        sender = self.sender()
        if sender.text() == '航班搜索':
            self.right_stack.setCurrentIndex(0)
            # self.search_page = 1  # 页码

        if sender.text() == '个人中心':
            self.right_stack.setCurrentIndex(1)
            self.user_page = 1  # 页码

    def searchFlight(self):
        """
        查询并更新航班信息
        """
        origin = self.origin_combobox.currentText()
        origin = self.city_dict[origin]
        terminal = self.terminal_combobox.currentText()
        terminal = self.city_dict[terminal]
        date = dict()
        date["year"] = self.year_combobox.currentText()
        date["month"] = self.month_combobox.currentText()
        date["day"] = self.day_combobox.currentText()
        ticket = FlightInfo(date, origin, terminal)
        self.search_page = 1  # 页码

        self.Flight = queryFlightInfo(ticket)  # 查询航班

        # 航班按时间排序
        def time(s):
            hour, min = s['date']['startTime'].split(':')
            hour = int(hour)
            min = int(min)
            return hour+(min/60)

        self.Flight = sorted(self.Flight, key=time)

        # 更新航班信息
        self.freshSearchFlight()

    def freshSearchFlight(self):
        # 更新航班信息
        if (5 * self.search_page - 5) < len(self.Flight):
            self.start_time_1.setText(self.Flight[5 * self.search_page - 5]["date"]["startTime"])
            self.end_time_1.setText(self.Flight[5 * self.search_page - 5]["date"]["endTime"])
            self.price_1.setText('￥' + str(self.Flight[5 * self.search_page - 5]["price"]))
        else:
            self.start_time_1.setText("")
            self.end_time_1.setText("")
            self.price_1.setText('￥')

        if (5 * self.search_page - 4) < len(self.Flight):
            self.start_time_2.setText(self.Flight[5 * self.search_page - 4]["date"]["startTime"])
            self.end_time_2.setText(self.Flight[5 * self.search_page - 4]["date"]["endTime"])
            self.price_2.setText('￥' + str(self.Flight[5 * self.search_page - 4]["price"]))
        else:
            self.start_time_2.setText("")
            self.end_time_2.setText("")
            self.price_2.setText('￥')

        if (5 * self.search_page - 3) < len(self.Flight):
            self.start_time_3.setText(self.Flight[5 * self.search_page - 3]["date"]["startTime"])
            self.end_time_3.setText(self.Flight[5 * self.search_page - 3]["date"]["endTime"])
            self.price_3.setText('￥' + str(self.Flight[5 * self.search_page - 3]["price"]))
        else:
            self.start_time_3.setText("")
            self.end_time_3.setText("")
            self.price_3.setText('￥')

        if (5 * self.search_page - 2) < len(self.Flight):
            self.start_time_4.setText(self.Flight[5 * self.search_page - 2]["date"]["startTime"])
            self.end_time_4.setText(self.Flight[5 * self.search_page - 2]["date"]["endTime"])
            self.price_4.setText('￥' + str(self.Flight[5 * self.search_page - 2]["price"]))
        else:
            self.start_time_4.setText("")
            self.end_time_4.setText("")
            self.price_4.setText('￥')

        if (5 * self.search_page - 1) < len(self.Flight):
            self.start_time_5.setText(self.Flight[5 * self.search_page - 1]["date"]["startTime"])
            self.end_time_5.setText(self.Flight[5 * self.search_page - 1]["date"]["endTime"])
            self.price_5.setText('￥' + str(self.Flight[5 * self.search_page - 1]["price"]))
        else:
            self.start_time_5.setText("")
            self.end_time_5.setText("")
            self.price_5.setText('￥')

        # 设置按钮可用/不可用
        if self.search_page*5 >= len(self.Flight):
            self.next_page_button.setEnabled(False)
        else:
            self.next_page_button.setEnabled(True)
        if self.search_page == 1:
            self.last_page_button.setEnabled(False)
        else:
            self.last_page_button.setEnabled(True)

    def nextPage(self):
        sender = self.sender()
        if sender.objectName() == 'search_next':
            self.search_page += 1
            self.freshSearchFlight()
            print("next_page")

    def prevPage(self):
        self.search_page -= 1
        self.freshSearchFlight()
        print("prev_page")

    def test(self):
        self.setFixedSize(960, 700)
        print("test")


    """
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QtWidgets.QCursor(Qt.ArrowCursor))
    """


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainWindow("admin3")
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()