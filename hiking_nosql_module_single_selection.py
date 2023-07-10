from PyQt5 import QtWidgets, QtGui
import sys
from PyQt5.QtWidgets import QTableWidget, QTableView, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class Main_Window(QWidget):
    
    def main_window(self, window):
        window.setWindowTitle("Hiking")
        window.resize(1950, 1100)
        
        grview = QtWidgets.QGraphicsView(window)
        gw = 2000
        gh = 2000
        grview.setGeometry(0, 0, gw, gh)    
        scene = QtWidgets.QGraphicsScene()
        img = QtGui.QPixmap("Hiking_modified.jpg")
        img_w = 1870                        
        img_h = 1000                         
        img = img.scaled(img_w, img_h)
        x = 20                               
        y = 20                                
        dx = int((gw - img_w) / 2) - x        
        dy = int((gh - img_h) / 2) - y
        scene.setSceneRect(dx, dy, img_w, img_h)
        scene.addPixmap(img)
        grview.setScene(scene)
        
        self.table_widget = QTableWidget()

        self.label_window = QtWidgets.QLabel(window)
        self.label_window.setText("Hiking : personal single selection")
        self.label_window.setGeometry(200,300,500,50)
        self.label_window.setStyleSheet("font-size:40px;font-weight:bold;color: #000;")

        global North, Center, South, East, Outlying_Island, box_county_warning
        North = ["請選擇縣市","台北市","新北市","基隆市","桃園市","新竹縣","新竹市","宜蘭縣"]
        Center = ["請選擇縣市","苗栗縣","台中市","彰化縣","南投縣","雲林縣"]
        South = ["請選擇縣市","嘉義市","嘉義縣","台南市","高雄市","屏東縣","澎湖縣"]
        East = ["請選擇縣市","花蓮縣","台東縣"]
        Outlying_Island = ["請選擇縣市","金門縣","連江縣"] 
        
        self.label_region = QtWidgets.QLabel(window)
        self.label_region.setText("地區:")
        self.label_region.setGeometry(200,430,200,30)
        self.box_region = QtWidgets.QComboBox(window)
        self.box_region.addItems(["請選擇地區","北部","中部","南部","東部","離島"])
        self.box_region.setGeometry(300,430,200,30)
        self.box_region.currentIndexChanged.connect(self.ui_search)
        self.box_region.currentIndexChanged.connect(self.ui_region)
        self.label_region.setStyleSheet("font-size:20px;font-weight:bold;")

        self.label_county = QtWidgets.QLabel(window)
        self.label_county.setText("縣市:")
        self.label_county.setGeometry(200,500,200,30)
        self.box_county = QtWidgets.QComboBox(window)
        box_county_warning = ["請先選擇地區再選擇縣市"]
        self.box_county.addItems(box_county_warning)
        self.box_county.setGeometry(300,500,200,30)
        self.box_county.currentIndexChanged.connect(self.ui_county)
        self.label_county.setStyleSheet("font-size:20px;font-weight:bold;")
        
        global rb_1, rb_2, rb_3, rb_4, rb_5
        self.label_difficulty = QtWidgets.QLabel(window)
        self.label_difficulty.setText("難易度:")
        self.label_difficulty.setGeometry(200,570,200,30)
        rb_1 = QtWidgets.QRadioButton(window)
        rb_1.setGeometry(300,570,200,30)
        rb_1.setText("低")
        rb_2 = QtWidgets.QRadioButton(window)
        rb_2.setGeometry(340,570,200,30)
        rb_2.setText("低-中")
        rb_3 = QtWidgets.QRadioButton(window)
        rb_3.setGeometry(400,570,200,30)
        rb_3.setText("中")
        rb_4 = QtWidgets.QRadioButton(window)
        rb_4.setGeometry(440,570,200,30)
        rb_4.setText("中-高")
        rb_5 = QtWidgets.QRadioButton(window)
        rb_5.setGeometry(500,570,200,30)
        rb_5.setText("高")
        group_difficulty = QtWidgets.QButtonGroup(window)
        group_difficulty.addButton(rb_1)
        group_difficulty.addButton(rb_2)
        group_difficulty.addButton(rb_3)
        group_difficulty.addButton(rb_4)
        group_difficulty.addButton(rb_5)
        group_difficulty.buttonClicked.connect(self.ui_search)
        group_difficulty.buttonClicked.connect(self.search_difficulty)
        self.label_difficulty.setStyleSheet("font-size:20px;font-weight:bold;")
        rb_1.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_2.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_3.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_4.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_5.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")

        global rb_less_5, rb_5_10, rb_10_15, rb_15_20, rb_20_25, rb_25_50, rb_50_75, rb_75_100
        self.label_distance = QtWidgets.QLabel(window)
        self.label_distance.setText("長度:")
        self.label_distance.setGeometry(600,430,200,30)
        rb_less_5 = QtWidgets.QRadioButton(window)
        rb_less_5.setGeometry(700,430,200,30)
        rb_less_5.setText("距離小於5公里")
        rb_5_10 = QtWidgets.QRadioButton(window)
        rb_5_10.setGeometry(700,470,200,30)
        rb_5_10.setText("距離介於5至10公里")
        rb_10_15 = QtWidgets.QRadioButton(window)
        rb_10_15.setGeometry(700,510,200,30)
        rb_10_15.setText("距離介於10至15公里")
        rb_15_20 = QtWidgets.QRadioButton(window)
        rb_15_20.setGeometry(700,550,200,30)
        rb_15_20.setText("距離介於15至20公里")
        rb_20_25 = QtWidgets.QRadioButton(window)
        rb_20_25.setGeometry(700,590,200,30)
        rb_20_25.setText("距離介於20至25公里")
        rb_25_50 = QtWidgets.QRadioButton(window)
        rb_25_50.setGeometry(700,630,200,30)
        rb_25_50.setText("距離介於25至50公里")
        rb_50_75 = QtWidgets.QRadioButton(window)
        rb_50_75.setGeometry(700,670,200,30)
        rb_50_75.setText("距離介於50至75公里")
        rb_75_100 = QtWidgets.QRadioButton(window)
        rb_75_100.setGeometry(700,710,200,30)
        rb_75_100.setText("距離介於75至100公里")
        group_distance = QtWidgets.QButtonGroup(window)
        group_distance.addButton(rb_less_5)
        group_distance.addButton(rb_5_10)
        group_distance.addButton(rb_10_15)
        group_distance.addButton(rb_15_20)
        group_distance.addButton(rb_20_25)
        group_distance.addButton(rb_25_50)
        group_distance.addButton(rb_50_75)
        group_distance.addButton(rb_75_100)
        group_distance.buttonClicked.connect(self.ui_search)
        group_distance.buttonClicked.connect(self.search_distance)
        self.label_distance.setStyleSheet("font-size:20px;font-weight:bold;")
        rb_less_5.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_5_10.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_10_15.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_15_20.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_20_25.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_25_50.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_50_75.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_75_100.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
    
        global rb_less_altitude_250, rb_altitude_250, rb_altitude_500, rb_altitude_750, rb_altitude_1000, rb_altitude_2000, rb_altitude_3000
        self.label_altitude = QtWidgets.QLabel(window)
        self.label_altitude.setText("海拔高度:")
        self.label_altitude.setGeometry(1000,430,200,30)
        rb_less_altitude_250 = QtWidgets.QRadioButton(window)
        rb_less_altitude_250.setGeometry(1100,430,200,30)
        rb_less_altitude_250.setText("海拔低於250公尺")
        rb_altitude_250 = QtWidgets.QRadioButton(window)
        rb_altitude_250.setGeometry(1100,470,200,30)
        rb_altitude_250.setText("海拔介於250至500公尺")
        rb_altitude_500 = QtWidgets.QRadioButton(window)
        rb_altitude_500.setGeometry(1100,510,200,30)
        rb_altitude_500.setText("海拔介於500至750公尺")
        rb_altitude_750 = QtWidgets.QRadioButton(window)
        rb_altitude_750.setGeometry(1100,550,200,30)
        rb_altitude_750.setText("海拔介於750至1000公尺")
        rb_altitude_1000 = QtWidgets.QRadioButton(window)
        rb_altitude_1000.setGeometry(1100,590,200,30)
        rb_altitude_1000.setText("海拔介於1000至2000公尺")
        rb_altitude_2000 = QtWidgets.QRadioButton(window)
        rb_altitude_2000.setGeometry(1100,630,200,30)
        rb_altitude_2000.setText("海拔介於2000至3000公尺")
        rb_altitude_3000 = QtWidgets.QRadioButton(window)
        rb_altitude_3000.setGeometry(1100,670,200,30)
        rb_altitude_3000.setText("海拔高於3000公尺")
        group_altitude = QtWidgets.QButtonGroup(window)
        group_altitude.addButton(rb_less_altitude_250)
        group_altitude.addButton(rb_altitude_250)
        group_altitude.addButton(rb_altitude_500)
        group_altitude.addButton(rb_altitude_750)
        group_altitude.addButton(rb_altitude_1000)
        group_altitude.addButton(rb_altitude_2000)
        group_altitude.addButton(rb_altitude_3000)
        group_altitude.buttonClicked.connect(self.ui_search)
        group_altitude.buttonClicked.connect(self.search_altitude)
        self.label_altitude.setStyleSheet("font-size:20px;font-weight:bold;")
        rb_less_altitude_250.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_altitude_250.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_altitude_500.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_altitude_750.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_altitude_1000.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_altitude_2000.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_altitude_3000.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")

        global rb_less_height_difference_50, rb_height_difference_50, rb_height_difference_100, rb_height_difference_150, rb_height_difference_200, rb_height_difference_500, rb_height_difference_750, rb_height_difference_1000, group_height_difference
        self.label_height_difference = QtWidgets.QLabel(window)
        self.label_height_difference.setText("高度落差:")
        self.label_height_difference.setGeometry(1400,430,200,30)
        rb_less_height_difference_50 = QtWidgets.QRadioButton(window)
        rb_less_height_difference_50.setGeometry(1500,430,200,30)
        rb_less_height_difference_50.setText("高度落差小於50公尺")
        rb_height_difference_50 = QtWidgets.QRadioButton(window)
        rb_height_difference_50.setGeometry(1500,470,200,30)
        rb_height_difference_50.setText("高度落差介於50至100公尺")
        rb_height_difference_100 = QtWidgets.QRadioButton(window)
        rb_height_difference_100.setGeometry(1500,510,200,30)
        rb_height_difference_100.setText("高度落差介於100至150公尺")
        rb_height_difference_150 = QtWidgets.QRadioButton(window)
        rb_height_difference_150.setGeometry(1500,550,200,30)
        rb_height_difference_150.setText("高度落差介於150至200公尺")
        rb_height_difference_200 = QtWidgets.QRadioButton(window)
        rb_height_difference_200.setGeometry(1500,590,200,30)
        rb_height_difference_200.setText("高度落差介於200至250公尺")
        rb_height_difference_250 = QtWidgets.QRadioButton(window)
        rb_height_difference_250.setGeometry(1500,630,200,30)
        rb_height_difference_250.setText("高度落差介於250至500公尺")
        rb_height_difference_500 = QtWidgets.QRadioButton(window)
        rb_height_difference_500.setGeometry(1500,670,200,30)
        rb_height_difference_500.setText("高度落差介於500至750公尺")
        rb_height_difference_750 = QtWidgets.QRadioButton(window)
        rb_height_difference_750.setGeometry(1500,710,250,30)
        rb_height_difference_750.setText("高度落差介於750至1000公尺")
        rb_height_difference_1000 = QtWidgets.QRadioButton(window)
        rb_height_difference_1000.setGeometry(1500,750,200,30)
        rb_height_difference_1000.setText("高度落差大於1000公尺")
        group_height_difference = QtWidgets.QButtonGroup(window)
        group_height_difference.addButton(rb_less_height_difference_50)
        group_height_difference.addButton(rb_height_difference_50)
        group_height_difference.addButton(rb_height_difference_100)
        group_height_difference.addButton(rb_height_difference_150)
        group_height_difference.addButton(rb_height_difference_200)
        group_height_difference.addButton(rb_height_difference_250)
        group_height_difference.addButton(rb_height_difference_500)
        group_height_difference.addButton(rb_height_difference_750)  
        group_height_difference.addButton(rb_height_difference_1000) 
        group_height_difference.buttonClicked.connect(self.ui_search)
        group_height_difference.buttonClicked.connect(self.search_height_difference)
        self.label_height_difference.setStyleSheet("font-size:20px;font-weight:bold;")
        rb_less_height_difference_50.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_height_difference_50.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}") 
        rb_height_difference_100.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}") 
        rb_height_difference_150.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}") 
        rb_height_difference_200.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}") 
        rb_height_difference_250.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}") 
        rb_height_difference_500.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}") 
        rb_height_difference_750.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}") 
        rb_height_difference_1000.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")  

        self.label_popular = QtWidgets.QLabel(window)
        self.label_popular.setText("人氣推薦:")
        self.label_popular.setGeometry(200,640,200,30)
        self.listwidget = QtWidgets.QListWidget(window)
        self.listwidget.addItems(["已前往人數排名","網站點閱人數排名"])
        self.listwidget.setGeometry(300,640,200,50)
        self.listwidget.setFlow(QtWidgets.QListView.TopToBottom)
        self.listwidget.clicked.connect(self.ui_search)
        self.listwidget.clicked.connect(self.search_popular)
        self.label_popular.setStyleSheet("font-size:20px;font-weight:bold;")
        self.listwidget.setStyleSheet("QListWidget::item{color:#000;}QListWidget::item:hover{color:#f00;}QListWidget::item:focus{color:#00f;}")

    def ui_search(self):
        self.btn = QtWidgets.QPushButton(Widget)
        self.btn.setText("Search")
        self.btn.setGeometry(350,740,80,50)
        self.btn.clicked.connect(self.search_result_window)
        self.btn.setStyleSheet("QPushButton::item{color:#000;}QPushButton:hover{color:#f00;font-size:20px;font-weight:bold;}QPushButton:focus{color:#00f;font-size:20px;font-weight:bold;}")   
        self.btn.show()    

    def ui_region(self):
        global value_region, result
        db = client.hikin_gdb
        col = db.hiking_col
        value_region = self.box_region.currentText()
        if value_region == "請選擇地區":
            pass
        elif value_region == "北部":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"台北市"},{"步道所在地區-2(縣市)":"台北市"},{"步道所在地區-3(縣市)":"台北市"},{"步道所在地區-4(縣市)":"台北市"},{"步道所在地區-5(縣市)":"台北市"},{"步道所在地區-6(縣市)":"台北市"},{"步道所在地區-7(縣市)":"台北市"},{"步道所在地區-8(縣市)":"台北市"},{"步道所在地區-1(縣市)":"新北市"},{"步道所在地區-2(縣市)":"新北市"},{"步道所在地區-3(縣市)":"新北市"},{"步道所在地區-4(縣市)":"新北市"},{"步道所在地區-5(縣市)":"新北市"},{"步道所在地區-6(縣市)":"新北市"},{"步道所在地區-7(縣市)":"新北市"},{"步道所在地區-8(縣市)":"新北市"},{"步道所在地區-1(縣市)":"基隆市"},{"步道所在地區-2(縣市)":"基隆市"},{"步道所在地區-3(縣市)":"基隆市"},{"步道所在地區-4(縣市)":"基隆市"},{"步道所在地區-5(縣市)":"基隆市"},{"步道所在地區-6(縣市)":"基隆市"},{"步道所在地區-7(縣市)":"基隆市"},{"步道所在地區-8(縣市)":"基隆市"},{"步道所在地區-1(縣市)":"桃園市"},{"步道所在地區-2(縣市)":"桃園市"},{"步道所在地區-3(縣市)":"桃園市"},{"步道所在地區-4(縣市)":"桃園市"},{"步道所在地區-5(縣市)":"桃園市"},{"步道所在地區-6(縣市)":"桃園市"},{"步道所在地區-7(縣市)":"桃園市"},{"步道所在地區-8(縣市)":"桃園市"},{"步道所在地區-1(縣市)":"新竹縣"},{"步道所在地區-2(縣市)":"新竹縣"},{"步道所在地區-3(縣市)":"新竹縣"},{"步道所在地區-4(縣市)":"新竹縣"},{"步道所在地區-5(縣市)":"新竹縣"},{"步道所在地區-6(縣市)":"新竹縣"},{"步道所在地區-7(縣市)":"新竹縣"},{"步道所在地區-8(縣市)":"新竹縣"},{"步道所在地區-1(縣市)":"新竹市"},{"步道所在地區-2(縣市)":"新竹市"},{"步道所在地區-3(縣市)":"新竹市"},{"步道所在地區-4(縣市)":"新竹市"},{"步道所在地區-5(縣市)":"新竹市"},{"步道所在地區-6(縣市)":"新竹市"},{"步道所在地區-7(縣市)":"新竹市"},{"步道所在地區-8(縣市)":"新竹市"},{"步道所在地區-1(縣市)":"宜蘭縣"},{"步道所在地區-2(縣市)":"宜蘭縣"},{"步道所在地區-3(縣市)":"宜蘭縣"},{"步道所在地區-4(縣市)":"宜蘭縣"},{"步道所在地區-5(縣市)":"宜蘭縣"},{"步道所在地區-6(縣市)":"宜蘭縣"},{"步道所在地區-7(縣市)":"宜蘭縣"},{"步道所在地區-8(縣市)":"宜蘭縣"}]}))
            self.box_county.clear()
            self.box_county.addItems(North)
            print(result)
            return result  
        elif value_region == "中部":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"苗栗縣"},{"步道所在地區-2(縣市)":"苗栗縣"},{"步道所在地區-3(縣市)":"苗栗縣"},{"步道所在地區-4(縣市)":"苗栗縣"},{"步道所在地區-5(縣市)":"苗栗縣"},{"步道所在地區-6(縣市)":"苗栗縣"},{"步道所在地區-7(縣市)":"苗栗縣"},{"步道所在地區-8(縣市)":"苗栗縣"},{"步道所在地區-1(縣市)":"台中市"},{"步道所在地區-2(縣市)":"台中市"},{"步道所在地區-3(縣市)":"台中市"},{"步道所在地區-4(縣市)":"台中市"},{"步道所在地區-5(縣市)":"台中市"},{"步道所在地區-6(縣市)":"台中市"},{"步道所在地區-7(縣市)":"台中市"},{"步道所在地區-8(縣市)":"台中市"},{"步道所在地區-1(縣市)":"彰化縣"},{"步道所在地區-2(縣市)":"彰化縣"},{"步道所在地區-3(縣市)":"彰化縣"},{"步道所在地區-4(縣市)":"彰化縣"},{"步道所在地區-5(縣市)":"彰化縣"},{"步道所在地區-6(縣市)":"彰化縣"},{"步道所在地區-7(縣市)":"彰化縣"},{"步道所在地區-8(縣市)":"彰化縣"},{"步道所在地區-1(縣市)":"南投縣"},{"步道所在地區-2(縣市)":"南投縣"},{"步道所在地區-3(縣市)":"南投縣"},{"步道所在地區-4(縣市)":"南投縣"},{"步道所在地區-5(縣市)":"南投縣"},{"步道所在地區-6(縣市)":"南投縣"},{"步道所在地區-7(縣市)":"南投縣"},{"步道所在地區-8(縣市)":"南投縣"},{"步道所在地區-1(縣市)":"雲林縣"},{"步道所在地區-2(縣市)":"雲林縣"},{"步道所在地區-3(縣市)":"雲林縣"},{"步道所在地區-4(縣市)":"雲林縣"},{"步道所在地區-5(縣市)":"雲林縣"},{"步道所在地區-6(縣市)":"雲林縣"},{"步道所在地區-7(縣市)":"雲林縣"},{"步道所在地區-8(縣市)":"雲林縣"}]}))
            self.box_county.clear()
            self.box_county.addItems(Center)
            print(result)
            return result
        elif value_region == "南部":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"嘉義市"},{"步道所在地區-2(縣市)":"嘉義市"},{"步道所在地區-3(縣市)":"嘉義市"},{"步道所在地區-4(縣市)":"嘉義市"},{"步道所在地區-5(縣市)":"嘉義市"},{"步道所在地區-6(縣市)":"嘉義市"},{"步道所在地區-7(縣市)":"嘉義市"},{"步道所在地區-8(縣市)":"嘉義市"},{"步道所在地區-1(縣市)":"嘉義縣"},{"步道所在地區-2(縣市)":"嘉義縣"},{"步道所在地區-3(縣市)":"嘉義縣"},{"步道所在地區-4(縣市)":"嘉義縣"},{"步道所在地區-5(縣市)":"嘉義縣"},{"步道所在地區-6(縣市)":"嘉義縣"},{"步道所在地區-7(縣市)":"嘉義縣"},{"步道所在地區-8(縣市)":"嘉義縣"},{"步道所在地區-1(縣市)":"台南市"},{"步道所在地區-2(縣市)":"台南市"},{"步道所在地區-3(縣市)":"台南市"},{"步道所在地區-4(縣市)":"台南市"},{"步道所在地區-5(縣市)":"台南市"},{"步道所在地區-6(縣市)":"台南市"},{"步道所在地區-7(縣市)":"台南市"},{"步道所在地區-8(縣市)":"台南市"},{"步道所在地區-1(縣市)":"高雄市"},{"步道所在地區-2(縣市)":"高雄市"},{"步道所在地區-3(縣市)":"高雄市"},{"步道所在地區-4(縣市)":"高雄市"},{"步道所在地區-5(縣市)":"高雄市"},{"步道所在地區-6(縣市)":"高雄市"},{"步道所在地區-7(縣市)":"高雄市"},{"步道所在地區-8(縣市)":"高雄市"},{"步道所在地區-1(縣市)":"屏東縣"},{"步道所在地區-2(縣市)":"屏東縣"},{"步道所在地區-3(縣市)":"屏東縣"},{"步道所在地區-4(縣市)":"屏東縣"},{"步道所在地區-5(縣市)":"屏東縣"},{"步道所在地區-6(縣市)":"屏東縣"},{"步道所在地區-7(縣市)":"屏東縣"},{"步道所在地區-8(縣市)":"屏東縣"},{"步道所在地區-1(縣市)":"澎湖縣"},{"步道所在地區-2(縣市)":"澎湖縣"},{"步道所在地區-3(縣市)":"澎湖縣"},{"步道所在地區-4(縣市)":"澎湖縣"},{"步道所在地區-5(縣市)":"澎湖縣"},{"步道所在地區-6(縣市)":"澎湖縣"},{"步道所在地區-7(縣市)":"澎湖縣"},{"步道所在地區-8(縣市)":"澎湖縣"}]}))
            self.box_county.clear()
            self.box_county.addItems(South) 
            print(result)
            return result
        elif value_region == "東部":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"花蓮縣"},{"步道所在地區-2(縣市)":"花蓮縣"},{"步道所在地區-3(縣市)":"花蓮縣"},{"步道所在地區-4(縣市)":"花蓮縣"},{"步道所在地區-5(縣市)":"花蓮縣"},{"步道所在地區-6(縣市)":"花蓮縣"},{"步道所在地區-7(縣市)":"花蓮縣"},{"步道所在地區-8(縣市)":"花蓮縣"},{"步道所在地區-1(縣市)":"台東縣"},{"步道所在地區-2(縣市)":"台東縣"},{"步道所在地區-3(縣市)":"台東縣"},{"步道所在地區-4(縣市)":"台東縣"},{"步道所在地區-5(縣市)":"台東縣"},{"步道所在地區-6(縣市)":"台東縣"},{"步道所在地區-7(縣市)":"台東縣"},{"步道所在地區-8(縣市)":"台東縣"}]}))
            self.box_county.clear()
            self.box_county.addItems(East)  
            print(result)
            return result
        elif value_region == "離島":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"金門縣"},{"步道所在地區-2(縣市)":"金門縣"},{"步道所在地區-3(縣市)":"金門縣"},{"步道所在地區-4(縣市)":"金門縣"},{"步道所在地區-5(縣市)":"金門縣"},{"步道所在地區-6(縣市)":"金門縣"},{"步道所在地區-7(縣市)":"金門縣"},{"步道所在地區-8(縣市)":"金門縣"},{"步道所在地區-1(縣市)":"連江縣"},{"步道所在地區-2(縣市)":"連江縣"},{"步道所在地區-3(縣市)":"連江縣"},{"步道所在地區-4(縣市)":"連江縣"},{"步道所在地區-5(縣市)":"連江縣"},{"步道所在地區-6(縣市)":"連江縣"},{"步道所在地區-7(縣市)":"連江縣"},{"步道所在地區-8(縣市)":"連江縣"}]}))
            self.box_county.clear()
            self.box_county.addItems(Outlying_Island)
            print(result)    
            return result   

    def ui_county(self):
        global value_county, result
        db = client.hikin_gdb
        col = db.hiking_col
        value_county = self.box_county.currentText()
        if value_county == "請選擇縣市":
            pass
        elif self.box_county.currentText() == "台北市":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"台北市"},{"步道所在地區-2(縣市)":"台北市"},{"步道所在地區-3(縣市)":"台北市"},{"步道所在地區-4(縣市)":"台北市"},{"步道所在地區-5(縣市)":"台北市"},{"步道所在地區-6(縣市)":"台北市"},{"步道所在地區-7(縣市)":"台北市"},{"步道所在地區-8(縣市)":"台北市"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search)  
            return result
        elif self.box_county.currentText() == "新北市":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"新北市"},{"步道所在地區-2(縣市)":"新北市"},{"步道所在地區-3(縣市)":"新北市"},{"步道所在地區-4(縣市)":"新北市"},{"步道所在地區-5(縣市)":"新北市"},{"步道所在地區-6(縣市)":"新北市"},{"步道所在地區-7(縣市)":"新北市"},{"步道所在地區-8(縣市)":"新北市"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search)  
            return result
        elif self.box_county.currentText() == "基隆市":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"基隆市"},{"步道所在地區-2(縣市)":"基隆市"},{"步道所在地區-3(縣市)":"基隆市"},{"步道所在地區-4(縣市)":"基隆市"},{"步道所在地區-5(縣市)":"基隆市"},{"步道所在地區-6(縣市)":"基隆市"},{"步道所在地區-7(縣市)":"基隆市"},{"步道所在地區-8(縣市)":"基隆市"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "桃園市":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"桃園市"},{"步道所在地區-2(縣市)":"桃園市"},{"步道所在地區-3(縣市)":"桃園市"},{"步道所在地區-4(縣市)":"桃園市"},{"步道所在地區-5(縣市)":"桃園市"},{"步道所在地區-6(縣市)":"桃園市"},{"步道所在地區-7(縣市)":"桃園市"},{"步道所在地區-8(縣市)":"桃園市"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "新竹縣":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"新竹縣"},{"步道所在地區-2(縣市)":"新竹縣"},{"步道所在地區-3(縣市)":"新竹縣"},{"步道所在地區-4(縣市)":"新竹縣"},{"步道所在地區-5(縣市)":"新竹縣"},{"步道所在地區-6(縣市)":"新竹縣"},{"步道所在地區-7(縣市)":"新竹縣"},{"步道所在地區-8(縣市)":"新竹縣"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "新竹市":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"新竹市"},{"步道所在地區-2(縣市)":"新竹市"},{"步道所在地區-3(縣市)":"新竹市"},{"步道所在地區-4(縣市)":"新竹市"},{"步道所在地區-5(縣市)":"新竹市"},{"步道所在地區-6(縣市)":"新竹市"},{"步道所在地區-7(縣市)":"新竹市"},{"步道所在地區-8(縣市)":"新竹市"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "宜蘭縣":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"宜蘭縣"},{"步道所在地區-2(縣市)":"宜蘭縣"},{"步道所在地區-3(縣市)":"宜蘭縣"},{"步道所在地區-4(縣市)":"宜蘭縣"},{"步道所在地區-5(縣市)":"宜蘭縣"},{"步道所在地區-6(縣市)":"宜蘭縣"},{"步道所在地區-7(縣市)":"宜蘭縣"},{"步道所在地區-8(縣市)":"宜蘭縣"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "苗栗縣":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"苗栗縣"},{"步道所在地區-2(縣市)":"苗栗縣"},{"步道所在地區-3(縣市)":"苗栗縣"},{"步道所在地區-4(縣市)":"苗栗縣"},{"步道所在地區-5(縣市)":"苗栗縣"},{"步道所在地區-6(縣市)":"苗栗縣"},{"步道所在地區-7(縣市)":"苗栗縣"},{"步道所在地區-8(縣市)":"苗栗縣"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "台中市":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"台中市"},{"步道所在地區-2(縣市)":"台中市"},{"步道所在地區-3(縣市)":"台中市"},{"步道所在地區-4(縣市)":"台中市"},{"步道所在地區-5(縣市)":"台中市"},{"步道所在地區-6(縣市)":"台中市"},{"步道所在地區-7(縣市)":"台中市"},{"步道所在地區-8(縣市)":"台中市"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "彰化縣":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"彰化縣"},{"步道所在地區-2(縣市)":"彰化縣"},{"步道所在地區-3(縣市)":"彰化縣"},{"步道所在地區-4(縣市)":"彰化縣"},{"步道所在地區-5(縣市)":"彰化縣"},{"步道所在地區-6(縣市)":"彰化縣"},{"步道所在地區-7(縣市)":"彰化縣"},{"步道所在地區-8(縣市)":"彰化縣"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "南投縣":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"南投縣"},{"步道所在地區-2(縣市)":"南投縣"},{"步道所在地區-3(縣市)":"南投縣"},{"步道所在地區-4(縣市)":"南投縣"},{"步道所在地區-5(縣市)":"南投縣"},{"步道所在地區-6(縣市)":"南投縣"},{"步道所在地區-7(縣市)":"南投縣"},{"步道所在地區-8(縣市)":"南投縣"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "雲林縣":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"雲林縣"},{"步道所在地區-2(縣市)":"雲林縣"},{"步道所在地區-3(縣市)":"雲林縣"},{"步道所在地區-4(縣市)":"雲林縣"},{"步道所在地區-5(縣市)":"雲林縣"},{"步道所在地區-6(縣市)":"雲林縣"},{"步道所在地區-7(縣市)":"雲林縣"},{"步道所在地區-8(縣市)":"雲林縣"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "嘉義市":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"嘉義市"},{"步道所在地區-2(縣市)":"嘉義市"},{"步道所在地區-3(縣市)":"嘉義市"},{"步道所在地區-4(縣市)":"嘉義市"},{"步道所在地區-5(縣市)":"嘉義市"},{"步道所在地區-6(縣市)":"嘉義市"},{"步道所在地區-7(縣市)":"嘉義市"},{"步道所在地區-8(縣市)":"嘉義市"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "嘉義縣":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"嘉義縣"},{"步道所在地區-2(縣市)":"嘉義縣"},{"步道所在地區-3(縣市)":"嘉義縣"},{"步道所在地區-4(縣市)":"嘉義縣"},{"步道所在地區-5(縣市)":"嘉義縣"},{"步道所在地區-6(縣市)":"嘉義縣"},{"步道所在地區-7(縣市)":"嘉義縣"},{"步道所在地區-8(縣市)":"嘉義縣"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "台南市":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"台南市"},{"步道所在地區-2(縣市)":"台南市"},{"步道所在地區-3(縣市)":"台南市"},{"步道所在地區-4(縣市)":"台南市"},{"步道所在地區-5(縣市)":"台南市"},{"步道所在地區-6(縣市)":"台南市"},{"步道所在地區-7(縣市)":"台南市"},{"步道所在地區-8(縣市)":"台南市"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "高雄市":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"高雄市"},{"步道所在地區-2(縣市)":"高雄市"},{"步道所在地區-3(縣市)":"高雄市"},{"步道所在地區-4(縣市)":"高雄市"},{"步道所在地區-5(縣市)":"高雄市"},{"步道所在地區-6(縣市)":"高雄市"},{"步道所在地區-7(縣市)":"高雄市"},{"步道所在地區-8(縣市)":"高雄市"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "屏東縣":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"屏東縣"},{"步道所在地區-2(縣市)":"屏東縣"},{"步道所在地區-3(縣市)":"屏東縣"},{"步道所在地區-4(縣市)":"屏東縣"},{"步道所在地區-5(縣市)":"屏東縣"},{"步道所在地區-6(縣市)":"屏東縣"},{"步道所在地區-7(縣市)":"屏東縣"},{"步道所在地區-8(縣市)":"屏東縣"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "澎湖縣":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"澎湖縣"},{"步道所在地區-2(縣市)":"澎湖縣"},{"步道所在地區-3(縣市)":"澎湖縣"},{"步道所在地區-4(縣市)":"澎湖縣"},{"步道所在地區-5(縣市)":"澎湖縣"},{"步道所在地區-6(縣市)":"澎湖縣"},{"步道所在地區-7(縣市)":"澎湖縣"},{"步道所在地區-8(縣市)":"澎湖縣"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "花蓮縣":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"花蓮縣"},{"步道所在地區-2(縣市)":"花蓮縣"},{"步道所在地區-3(縣市)":"花蓮縣"},{"步道所在地區-4(縣市)":"花蓮縣"},{"步道所在地區-5(縣市)":"花蓮縣"},{"步道所在地區-6(縣市)":"花蓮縣"},{"步道所在地區-7(縣市)":"花蓮縣"},{"步道所在地區-8(縣市)":"花蓮縣"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "台東縣":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"台東縣"},{"步道所在地區-2(縣市)":"台東縣"},{"步道所在地區-3(縣市)":"台東縣"},{"步道所在地區-4(縣市)":"台東縣"},{"步道所在地區-5(縣市)":"台東縣"},{"步道所在地區-6(縣市)":"台東縣"},{"步道所在地區-7(縣市)":"台東縣"},{"步道所在地區-8(縣市)":"台東縣"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "金門縣":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"金門縣"},{"步道所在地區-2(縣市)":"金門縣"},{"步道所在地區-3(縣市)":"金門縣"},{"步道所在地區-4(縣市)":"金門縣"},{"步道所在地區-5(縣市)":"金門縣"},{"步道所在地區-6(縣市)":"金門縣"},{"步道所在地區-7(縣市)":"金門縣"},{"步道所在地區-8(縣市)":"金門縣"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result
        elif self.box_county.currentText() == "連江縣":
            result = list(col.find({"$or":[{"步道所在地區-1(縣市)":"連江縣"},{"步道所在地區-2(縣市)":"連江縣"},{"步道所在地區-3(縣市)":"連江縣"},{"步道所在地區-4(縣市)":"連江縣"},{"步道所在地區-5(縣市)":"連江縣"},{"步道所在地區-6(縣市)":"連江縣"},{"步道所在地區-7(縣市)":"連江縣"},{"步道所在地區-8(縣市)":"連江縣"}]}))        
            print(result)
            self.box_county.currentIndexChanged.connect(self.ui_search) 
            return result

    def search_difficulty(self):
        global result
        db = client.hikin_gdb
        col = db.hiking_col
        if rb_1.isChecked():
            result = list(col.find({"步道難易度":1}))        
            print(result)
            return result
        elif rb_2.isChecked():
            result = list(col.find({"步道難易度":2}))        
            print(result)
            return result
        elif rb_3.isChecked():
            result = list(col.find({"步道難易度":3}))        
            print(result)
            return result
        elif rb_4.isChecked():
            result = list(col.find({"步道難易度":4}))        
            print(result)
            return result
        elif rb_5.isChecked():
            result = list(col.find({"步道難易度":5}))        
            print(result)
            return result
        
    def search_distance(self):
        global result
        db = client.hikin_gdb
        col = db.hiking_col
        if rb_less_5.isChecked():
            result = list(col.find({"步道長度(公里)":{"$lt":5}}))        
            print(result)
            return result
        elif rb_5_10.isChecked():
            result = list(col.find({"步道長度(公里)":{"$gt":5,"$lt":10}}))        
            print(result)
            return result
        elif rb_10_15.isChecked():
            result = list(col.find({"步道長度(公里)":{"$gt":10,"$lt":15}}))        
            print(result)
            return result
        elif rb_15_20.isChecked():
            result = list(col.find({"步道長度(公里)":{"$gt":15,"$lt":20}}))        
            print(result)
            return result
        elif rb_20_25.isChecked():
            result = list(col.find({"步道長度(公里)":{"$gt":20,"$lt":25}}))        
            print(result)
            return result
        elif rb_25_50.isChecked():
            result = list(col.find({"步道長度(公里)":{"$gt":25,"$lt":50}}))        
            print(result)
            return result
        elif rb_50_75.isChecked():
            result = list(col.find({"步道長度(公里)":{"$gt":50,"$lt":75}}))        
            print(result)
            return result
        elif rb_75_100.isChecked():
            result = list(col.find({"步道長度(公里)":{"$gt":75,"$lt":100}}))        
            print(result)
            return result

    def search_altitude(self):
        global result
        db = client.hikin_gdb
        col = db.hiking_col
        if rb_less_altitude_250.isChecked():
            result = list(col.find({"$or":[{"步道海拔起始高度(公尺)":{"$lt":250}},{"步道海拔終點高度(公尺)":{"$lt":250}}]}))        
            print(result)
            return result
        elif rb_altitude_250.isChecked():
            result = list(col.find({"$or":[{"步道海拔起始高度(公尺)":{"$gt":250,"$lt":500}},{"步道海拔起始高度(公尺)":{"$gt":250,"$lt":500}}]}))        
            print(result)
            return result
        elif rb_altitude_500.isChecked():
            result = list(col.find({"$or":[{"步道海拔起始高度(公尺)":{"$gt":500,"$lt":750}},{"步道海拔起始高度(公尺)":{"$gt":500,"$lt":750}}]}))        
            print(result)
            return result
        elif rb_altitude_750.isChecked():
            result = list(col.find({"$or":[{"步道海拔起始高度(公尺)":{"$gt":750,"$lt":1000}},{"步道海拔起始高度(公尺)":{"$gt":750,"$lt":1000}}]}))        
            print(result)
            return result
        elif rb_altitude_1000.isChecked():
            result = list(col.find({"$or":[{"步道海拔起始高度(公尺)":{"$gt":1000,"$lt":2000}},{"步道海拔起始高度(公尺)":{"$gt":1000,"$lt":2000}}]}))        
            print(result)
            return result
        elif rb_altitude_2000.isChecked():
            result = list(col.find({"$or":[{"步道海拔起始高度(公尺)":{"$gt":2000,"$lt":3000}},{"步道海拔起始高度(公尺)":{"$gt":2000,"$lt":3000}}]}))        
            print(result)
            return result
        elif rb_altitude_3000.isChecked():
            result = list(col.find({"$or":[{"步道海拔起始高度(公尺)":{"gt":3000}},{"步道海拔起始高度(公尺)":{"gt":3000}}]}))        
            print(result)
            return result

    def search_height_difference(self):
        global result
        db = client.hikin_gdb
        col = db.hiking_col
        if rb_less_height_difference_50.isChecked():
            result = list(col.find({"步道高度落差(公尺)":{"$lt":50}}))        
            print(result)
            return result
        elif rb_height_difference_50.isChecked():
            result = list(col.find({"步道高度落差(公尺)":{"$gt":50,"$lt":100}}))        
            print(result)
            return result
        elif rb_height_difference_100.isChecked():
            result = list(col.find({"步道高度落差(公尺)":{"$gt":100,"$lt":150}}))        
            print(result)
            return result
        elif rb_height_difference_150.isChecked():
            result = list(col.find({"步道高度落差(公尺)":{"$gt":150,"$lt":200}}))        
            print(result)
            return result
        elif rb_height_difference_200.isChecked():
            result = list(col.find({"步道高度落差(公尺)":{"$gt":200,"$lt":500}}))        
            print(result)
            return result
        elif rb_height_difference_500.isChecked():
            result = list(col.find({"步道高度落差(公尺)":{"$gt":500,"$lt":750}}))        
            print(result)
            return result
        elif rb_height_difference_750.isChecked():
            result = list(col.find({"步道高度落差(公尺)":{"$gt":750,"$lt":1000}}))        
            print(result)
            return result
        elif rb_height_difference_1000.isChecked():
            result = list(col.find({"步道高度落差(公尺)":{"gt":1000}}))        
            print(result)
            return result

    def search_popular(self):
        global result
        db = client.hikin_gdb
        col = db.hiking_col
        if self.listwidget.currentItem().text() == "已前往人數排名":
            result = list(col.find().sort("步道已前往人數",-1))
            print(result)
            return result
        elif self.listwidget.currentItem().text() == "網站點閱人數排名":
            result = list(col.find().sort("步道網站點閱人數",-1))
            print(result)
            return result

    def search_result_window(self):
        self.setWindowTitle("Search Result")
        self.resize(2000, 2000)
        
        self.new_window_model = QStandardItemModel(1811,31)
        self.new_window_tableview = QTableView(self)
        self.new_window_tableview.setModel(self.new_window_model)
        self.new_window_tableview.move(100,50)
        self.new_window_tableview.resize(1700,950)
        self.new_window_model.setHorizontalHeaderLabels(["步道ID","步道名稱","步道相關資訊網站","步道評分","步道所在地區-1(縣市)","步道所在地區-1(鄉鎮市區)","步道所在地區-2(縣市)","步道所在地區-2(鄉鎮市區)","步道所在地區-3(縣市)","步道所在地區-3(鄉鎮市區)","步道所在地區-4(縣市)","步道所在地區-4(鄉鎮市區)","步道所在地區-5(縣市)","步道所在地區-5(鄉鎮市區)","步道所在地區-6(縣市)","步道所在地區-6(鄉鎮市區)","步道所在地區-7(縣市)","步道所在地區-7(鄉鎮市區)","步道所在地區-8(縣市)","步道所在地區-8(鄉鎮市區)","步道難易度","步道長度","步道攀登時間","步道欲前往人數","步道已前往人數","步道網站點閱人數","步道圖片網址","步道海拔起始高度(公尺)","步道海拔終點高度(公尺)","步道高度落差(公尺)","步道基本資料介紹","開車路線","大眾運輸路線","步道路線"])

              
        for i in range(len(result)):    
            for j in range(len(list(result[i].keys()))):
                self.new_window_model.setItem(i,j,QStandardItem(str(result[i][list(result[i].keys())[j]])))
            i += 1
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Main_Window()
    ui.main_window(Widget)
    
    Widget.show()

    uri = "mongodb+srv://alex111122221111:sandia100alex@hiking.46ndoin.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    sys.exit(app.exec_())