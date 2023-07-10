from PyQt5 import QtWidgets, QtGui
import sys
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from PyQt5.QtWidgets import QTableWidget, QTableView, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import pandas as pd

class Main_Window(QWidget):
    
    def main_window(self, window):
        global search_list
        window.setWindowTitle("Hiking")
        window.resize(1950, 1100)
        
        search_list = []

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
        self.label_window.setText("Hiking : pesonal multiple selection")
        self.label_window.setGeometry(200,300,1000,50)
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
        self.box_region.currentIndexChanged.connect(self.region)
        self.label_region.setStyleSheet("font-size:20px;font-weight:bold;")
        
        self.label_county = QtWidgets.QLabel(window)
        self.label_county.setText("縣市:")
        self.label_county.setGeometry(200,500,200,30)
        self.box_county = QtWidgets.QComboBox(window)
        box_county_warning = ["請先選擇地區再選擇縣市"]
        self.box_county.addItems(box_county_warning)
        self.box_county.setGeometry(300,500,200,30)
        self.box_county.currentIndexChanged.connect(self.ui_search)
        self.box_county.currentIndexChanged.connect(self.county)
        self.label_county.setStyleSheet("font-size:20px;font-weight:bold;")
        
        global rb_1, rb_2, rb_3, rb_4, rb_5, group_difficulty
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
        group_difficulty.addButton(rb_1,1)
        group_difficulty.addButton(rb_2,2)
        group_difficulty.addButton(rb_3,3)
        group_difficulty.addButton(rb_4,4)
        group_difficulty.addButton(rb_5,5)
        group_difficulty.buttonToggled.connect(self.ui_search)
        group_difficulty.buttonToggled.connect(self.difficulty)
        self.label_difficulty.setStyleSheet("font-size:20px;font-weight:bold;")
        rb_1.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_2.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_3.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_4.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_5.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")

        global rb_less_5, rb_5_10, rb_10_15, rb_15_20, rb_20_25, rb_25_50, rb_50_75, rb_75_100, group_distance
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
        group_distance.buttonToggled.connect(self.ui_search)
        group_distance.buttonToggled.connect(self.distance)
        self.label_distance.setStyleSheet("font-size:20px;font-weight:bold;")
        rb_less_5.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_5_10.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_10_15.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_15_20.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_20_25.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_25_50.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_50_75.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
        rb_75_100.setStyleSheet("QRadioButton {color: #000;}QRadioButton:hover {color:#f00;}QRadioButton:focus {color:#00f;}")
    
        global rb_less_altitude_250, rb_altitude_250, rb_altitude_500, rb_altitude_750, rb_altitude_1000, rb_altitude_2000, rb_altitude_3000, group_altitude
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
        group_altitude.buttonToggled.connect(self.ui_search)
        group_altitude.buttonToggled.connect(self.altitude)
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
        group_height_difference.buttonToggled.connect(self.ui_search)
        group_height_difference.buttonToggled.connect(self.height_difference)
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
        self.listwidget.clicked.connect(self.popular)
        self.label_popular.setStyleSheet("font-size:20px;font-weight:bold;")
        self.listwidget.setStyleSheet("QListWidget::item{color:#000;}QListWidget::item:hover{color:#f00;}QListWidget::item:focus{color:#00f;}")
    
    def ui_search(self):
        self.btn = QtWidgets.QPushButton(Widget)
        self.btn.setText("Search")
        self.btn.setGeometry(350,740,80,50)
        self.btn.clicked.connect(self.search_result_window)
        self.btn.setStyleSheet("QPushButton::item{color:#000;}QPushButton:hover{color:#f00;font-size:20px;font-weight:bold;}QPushButton:focus{color:#00f;font-size:20px;font-weight:bold;}")   
        self.btn.show()   

    def region(self):
        global value_region, region
        db = client.hikin_gdb
        col = db.hiking_col
        result = list(col.find()) 

        df = pd.DataFrame(result)
        df.columns = (["id", "name", "url", "score", "county_1", "township_1", "county_2", "township_2", "county_3", "township_3", "county_4", "township_4", "county_5", "township_5", "county_6", "township_6", "county_7", "township_7", "county_8", "township_8", "difficulty", "distance", "time", "people_want", "people_gone", "people_view", "image_url", "altitude_low", "altitude_high", "height_difference", "basic_intro", "drive", "public_transportation", "route"])
                
        value_region = self.box_region.currentText()
        if value_region == "請選擇地區":
            pass
        elif value_region == "北部":
            self.box_county.clear()
            self.box_county.addItems(North)
            region = df["county_1"].isin(["台北市"])|df["county_2"].isin(["台北市"])|df["county_3"].isin(["台北市"])|df["county_4"].isin(["台北市"])|df["county_5"].isin(["台北市"])|df["county_6"].isin(["台北市"])|df["county_7"].isin(["台北市"])|df["county_8"].isin(["台北市"])|df["county_1"].isin(["新北市"])|df["county_2"].isin(["新北市"])|df["county_3"].isin(["新北市"])|df["county_4"].isin(["新北市"])|df["county_5"].isin(["新北市"])|df["county_6"].isin(["新北市"])|df["county_7"].isin(["新北市"])|df["county_8"].isin(["新北市"])|df["county_1"].isin(["基隆市"])|df["county_2"].isin(["基隆市"])|df["county_3"].isin(["基隆市"])|df["county_4"].isin(["基隆市"])|df["county_5"].isin(["基隆市"])|df["county_6"].isin(["基隆市"])|df["county_7"].isin(["基隆市"])|df["county_8"].isin(["基隆市"])|df["county_1"].isin(["桃園市"])|df["county_2"].isin(["桃園市"])|df["county_3"].isin(["桃園市"])|df["county_4"].isin(["桃園市"])|df["county_5"].isin(["桃園市"])|df["county_6"].isin(["桃園市"])|df["county_7"].isin(["桃園市"])|df["county_8"].isin(["桃園市"])|df["county_1"].isin(["新竹縣"])|df["county_2"].isin(["新竹縣"])|df["county_3"].isin(["新竹縣"])|df["county_4"].isin(["新竹縣"])|df["county_5"].isin(["新竹縣"])|df["county_6"].isin(["新竹縣"])|df["county_7"].isin(["新竹縣"])|df["county_8"].isin(["新竹縣"])|df["county_1"].isin(["新竹市"])|df["county_2"].isin(["新竹市"])|df["county_3"].isin(["新竹市"])|df["county_4"].isin(["新竹市"])|df["county_5"].isin(["新竹市"])|df["county_6"].isin(["新竹市"])|df["county_7"].isin(["新竹市"])|df["county_8"].isin(["新竹市"])|df["county_1"].isin(["宜蘭縣"])|df["county_2"].isin(["宜蘭縣"])|df["county_3"].isin(["宜蘭縣"])|df["county_4"].isin(["宜蘭縣"])|df["county_5"].isin(["宜蘭縣"])|df["county_6"].isin(["宜蘭縣"])|df["county_7"].isin(["宜蘭縣"])|df["county_8"].isin(["宜蘭縣"])
        elif value_region == "中部":
            self.box_county.clear()
            self.box_county.addItems(Center)
            region = df["county_1"].isin(["苗栗縣"])|df["county_2"].isin(["苗栗縣"])|df["county_3"].isin(["苗栗縣"])|df["county_4"].isin(["苗栗縣"])|df["county_5"].isin(["苗栗縣"])|df["county_6"].isin(["苗栗縣"])|df["county_7"].isin(["苗栗縣"])|df["county_8"].isin(["苗栗縣"])|df["county_1"].isin(["台中市"])|df["county_2"].isin(["台中市"])|df["county_3"].isin(["台中市"])|df["county_4"].isin(["台中市"])|df["county_5"].isin(["台中市"])|df["county_6"].isin(["台中市"])|df["county_7"].isin(["台中市"])|df["county_8"].isin(["台中市"])|df["county_1"].isin(["彰化縣"])|df["county_2"].isin(["彰化縣"])|df["county_3"].isin(["彰化縣"])|df["county_4"].isin(["彰化縣"])|df["county_5"].isin(["彰化縣"])|df["county_6"].isin(["彰化縣"])|df["county_7"].isin(["彰化縣"])|df["county_8"].isin(["彰化縣"])|df["county_1"].isin(["南投縣"])|df["county_2"].isin(["南投縣"])|df["county_3"].isin(["南投縣"])|df["county_4"].isin(["南投縣"])|df["county_5"].isin(["南投縣"])|df["county_6"].isin(["南投縣"])|df["county_7"].isin(["南投縣"])|df["county_8"].isin(["南投縣"])|df["county_1"].isin(["雲林縣"])|df["county_2"].isin(["雲林縣"])|df["county_3"].isin(["雲林縣"])|df["county_4"].isin(["雲林縣"])|df["county_5"].isin(["雲林縣"])|df["county_6"].isin(["雲林縣"])|df["county_7"].isin(["雲林縣"])|df["county_8"].isin(["雲林縣"])
        elif value_region == "南部":
            self.box_county.clear()
            self.box_county.addItems(South)    
            region = df["county_1"].isin(["嘉義市"])|df["county_2"].isin(["嘉義市"])|df["county_3"].isin(["嘉義市"])|df["county_4"].isin(["嘉義市"])|df["county_5"].isin(["嘉義市"])|df["county_6"].isin(["嘉義市"])|df["county_7"].isin(["嘉義市"])|df["county_8"].isin(["嘉義市"])|df["county_1"].isin(["嘉義縣"])|df["county_2"].isin(["嘉義縣"])|df["county_3"].isin(["嘉義縣"])|df["county_4"].isin(["嘉義縣"])|df["county_5"].isin(["嘉義縣"])|df["county_6"].isin(["嘉義縣"])|df["county_7"].isin(["嘉義縣"])|df["county_8"].isin(["嘉義縣"])|df["county_1"].isin(["台南市"])|df["county_2"].isin(["台南市"])|df["county_3"].isin(["台南市"])|df["county_4"].isin(["台南市"])|df["county_5"].isin(["台南市"])|df["county_6"].isin(["台南市"])|df["county_7"].isin(["台南市"])|df["county_8"].isin(["台南市"])|df["county_1"].isin(["高雄市"])|df["county_2"].isin(["高雄市"])|df["county_3"].isin(["高雄市"])|df["county_4"].isin(["高雄市"])|df["county_5"].isin(["高雄市"])|df["county_6"].isin(["高雄市"])|df["county_7"].isin(["高雄市"])|df["county_8"].isin(["高雄市"])|df["county_1"].isin(["屏東縣"])|df["county_2"].isin(["屏東縣"])|df["county_3"].isin(["屏東縣"])|df["county_4"].isin(["屏東縣"])|df["county_5"].isin(["屏東縣"])|df["county_6"].isin(["屏東縣"])|df["county_7"].isin(["屏東縣"])|df["county_8"].isin(["屏東縣"])|df["county_1"].isin(["澎湖縣"])|df["county_2"].isin(["澎湖縣"])|df["county_3"].isin(["澎湖縣"])|df["county_4"].isin(["澎湖縣"])|df["county_5"].isin(["澎湖縣"])|df["county_6"].isin(["澎湖縣"])|df["county_7"].isin(["澎湖縣"])|df["county_8"].isin(["澎湖縣"])
        elif value_region == "東部":
            self.box_county.clear()
            self.box_county.addItems(East)   
            region = df["county_1"].isin(["花蓮縣"])|df["county_2"].isin(["花蓮縣"])|df["county_3"].isin(["花蓮縣"])|df["county_4"].isin(["花蓮縣"])|df["county_5"].isin(["花蓮縣"])|df["county_6"].isin(["花蓮縣"])|df["county_7"].isin(["花蓮縣"])|df["county_8"].isin(["花蓮縣"])|df["county_1"].isin(["台東縣"])|df["county_2"].isin(["台東縣"])|df["county_3"].isin(["台東縣"])|df["county_4"].isin(["台東縣"])|df["county_5"].isin(["台東縣"])|df["county_6"].isin(["台東縣"])|df["county_7"].isin(["台東縣"])|df["county_8"].isin(["台東縣"])
        elif value_region == "離島":
            self.box_county.clear()
            self.box_county.addItems(Outlying_Island)
            region = df["county_1"].isin(["金門縣"])|df["county_2"].isin(["金門縣"])|df["county_3"].isin(["金門縣"])|df["county_4"].isin(["金門縣"])|df["county_5"].isin(["金門縣"])|df["county_6"].isin(["金門縣"])|df["county_7"].isin(["金門縣"])|df["county_8"].isin(["金門縣"])|df["county_1"].isin(["連江縣"])|df["county_2"].isin(["連江縣"])|df["county_3"].isin(["連江縣"])|df["county_4"].isin(["連江縣"])|df["county_5"].isin(["連江縣"])|df["county_6"].isin(["連江縣"])|df["county_7"].isin(["連江縣"])|df["county_8"].isin(["連江縣"])

    def county(self):
        global value_county, county
        db = client.hikin_gdb
        col = db.hiking_col
        result = list(col.find()) 

        df = pd.DataFrame(result)
        df.columns = (["id", "name", "url", "score", "county_1", "township_1", "county_2", "township_2", "county_3", "township_3", "county_4", "township_4", "county_5", "township_5", "county_6", "township_6", "county_7", "township_7", "county_8", "township_8", "difficulty", "distance", "time", "people_want", "people_gone", "people_view", "image_url", "altitude_low", "altitude_high", "height_difference", "basic_intro", "drive", "public_transportation", "route"])
        
        value_county = self.box_county.currentText()
        county = df["county_1"].isin([str(value_county)])|df["county_2"].isin([str(value_county)])|df["county_3"].isin([str(value_county)])|df["county_4"].isin([str(value_county)])|df["county_5"].isin([str(value_county)])|df["county_6"].isin([str(value_county)])|df["county_7"].isin([str(value_county)])|df["county_8"].isin([str(value_county)])

    def difficulty(self):
        global difficulty
        db = client.hikin_gdb
        col = db.hiking_col
        result = list(col.find()) 

        df = pd.DataFrame(result)
        df.columns = (["id", "name", "url", "score", "county_1", "township_1", "county_2", "township_2", "county_3", "township_3", "county_4", "township_4", "county_5", "township_5", "county_6", "township_6", "county_7", "township_7", "county_8", "township_8", "difficulty", "distance", "time", "people_want", "people_gone", "people_view", "image_url", "altitude_low", "altitude_high", "height_difference", "basic_intro", "drive", "public_transportation", "route"])

        if rb_1.isChecked():
            difficulty = df["difficulty"].isin([1])  
            search_list.append(difficulty)
        elif rb_2.isChecked():
            difficulty = df["difficulty"].isin([2])   
            search_list.append(difficulty)
        elif rb_3.isChecked():
            difficulty = df["difficulty"].isin([3]) 
            search_list.append(difficulty)
        elif rb_4.isChecked():
            difficulty = df["difficulty"].isin([4]) 
            search_list.append(difficulty)
        elif rb_5.isChecked():
            difficulty = df["difficulty"].isin([5])  
            search_list.append(difficulty)        
        
    def distance(self):
        global distance
        db = client.hikin_gdb
        col = db.hiking_col
        result = list(col.find()) 

        df = pd.DataFrame(result)
        df.columns = (["id", "name", "url", "score", "county_1", "township_1", "county_2", "township_2", "county_3", "township_3", "county_4", "township_4", "county_5", "township_5", "county_6", "township_6", "county_7", "township_7", "county_8", "township_8", "difficulty", "distance", "time", "people_want", "people_gone", "people_view", "image_url", "altitude_low", "altitude_high", "height_difference", "basic_intro", "drive", "public_transportation", "route"])
            
        if rb_less_5.isChecked():
            distance = df["distance"] < 5
            search_list.append(distance)
        elif rb_5_10.isChecked():
            distance = df["distance"].between(5,10)
            search_list.append(distance)
        elif rb_10_15.isChecked():
            distance = df["distance"].between(10,15)
            search_list.append(distance)
        elif rb_15_20.isChecked():
            distance = df["distance"].between(15,20)
            search_list.append(distance)
        elif rb_20_25.isChecked():
            distance = df["distance"].between(20,25)
            search_list.append(distance)
        elif rb_25_50.isChecked():
            distance = df["distance"].between(25,50)
            search_list.append(distance)
        elif rb_50_75.isChecked():
            distance = df["distance"].between(50,75)
            search_list.append(distance)
        elif rb_75_100.isChecked():
            distance = df["distance"].between(75,100)
            search_list.append(distance)

    def altitude(self):
        global altitude
        db = client.hikin_gdb
        col = db.hiking_col
        result = list(col.find()) 

        df = pd.DataFrame(result)
        df.columns = (["id", "name", "url", "score", "county_1", "township_1", "county_2", "township_2", "county_3", "township_3", "county_4", "township_4", "county_5", "township_5", "county_6", "township_6", "county_7", "township_7", "county_8", "township_8", "difficulty", "distance", "time", "people_want", "people_gone", "people_view", "image_url", "altitude_low", "altitude_high", "height_difference", "basic_intro", "drive", "public_transportation", "route"])
            
        if rb_less_altitude_250.isChecked():
            altitude = (df["altitude_low"] < 250)|(df["altitude_high"] < 250)
            search_list.append(altitude)
        elif rb_altitude_250.isChecked():
            altitude = df["altitude_low"].between(250,500)|df["altitude_high"].between(250,500)
            search_list.append(altitude)
        elif rb_altitude_500.isChecked():
            altitude = df["altitude_low"].between(500,750)|df["altitude_high"].between(500,750)
            search_list.append(altitude)
        elif rb_altitude_750.isChecked():
            altitude = df["altitude_low"].between(750,1000)|df["altitude_high"].between(750,1000)
            search_list.append(altitude)
        elif rb_altitude_1000.isChecked():
            altitude = df["altitude_low"].between(1000,2000)|df["altitude_high"].between(1000,2000)
            search_list.append(altitude)
        elif rb_altitude_2000.isChecked():
            altitude = df["altitude_low"].between(2000,3000)|df["altitude_high"].between(2000,3000)
            search_list.append(altitude)
        elif rb_altitude_3000.isChecked():
            altitude = (df["altitude_low"] > 3000)|(df["altitude_high"] > 3000)
            search_list.append(altitude)

    def height_difference(self):
        global height_difference
        db = client.hikin_gdb
        col = db.hiking_col
        result = list(col.find()) 

        df = pd.DataFrame(result)
        df.columns = (["id", "name", "url", "score", "county_1", "township_1", "county_2", "township_2", "county_3", "township_3", "county_4", "township_4", "county_5", "township_5", "county_6", "township_6", "county_7", "township_7", "county_8", "township_8", "difficulty", "distance", "time", "people_want", "people_gone", "people_view", "image_url", "altitude_low", "altitude_high", "height_difference", "basic_intro", "drive", "public_transportation", "route"])
        
        if rb_less_height_difference_50.isChecked():
            height_difference = df["height_difference"] < 50
            search_list.append(height_difference)
        elif rb_height_difference_50.isChecked():
            height_difference = df["height_difference"].between(50,100)
            search_list.append(height_difference)
        elif rb_height_difference_100.isChecked():
            height_difference = df["height_difference"].between(100,150)
            search_list.append(height_difference)
        elif rb_height_difference_150.isChecked():
            height_difference = df["height_difference"].between(150,200)
            search_list.append(height_difference)
        elif rb_height_difference_200.isChecked():
            height_difference = df["height_difference"].between(200,500)
            search_list.append(height_difference)
        elif rb_height_difference_500.isChecked():
            height_difference = df["height_difference"].between(500,750)
            search_list.append(height_difference)
        elif rb_height_difference_750.isChecked():
            height_difference = df["height_difference"].between(750,1000)
            search_list.append(height_difference)
        elif rb_height_difference_1000.isChecked():
            height_difference = df["height_difference"] > 1000
            search_list.append(height_difference)

    def popular(self):
        global popular
        db = client.hikin_gdb
        col = db.hiking_col
        result = list(col.find()) 

        df = pd.DataFrame(result)
        df.columns = (["id", "name", "url", "score", "county_1", "township_1", "county_2", "township_2", "county_3", "township_3", "county_4", "township_4", "county_5", "township_5", "county_6", "township_6", "county_7", "township_7", "county_8", "township_8", "difficulty", "distance", "time", "people_want", "people_gone", "people_view", "image_url", "altitude_low", "altitude_high", "height_difference", "basic_intro", "drive", "public_transportation", "route"])
            
        if self.listwidget.currentIndex().row()	 == 0:
            popular = df.sort_values(["people_gone"],ascending = 0)
        elif self.listwidget.currentIndex().row() == 1:
            popular = df.sort_values(["people_view"],ascending = 0)

    def search_result_window(self):
        global Final_df
        db = client.hikin_gdb
        col = db.hiking_col
        result = list(col.find()) 

        df = pd.DataFrame(result)
        df.columns = (["id", "name", "url", "score", "county_1", "township_1", "county_2", "township_2", "county_3", "township_3", "county_4", "township_4", "county_5", "township_5", "county_6", "township_6", "county_7", "township_7", "county_8", "township_8", "difficulty", "distance", "time", "people_want", "people_gone", "people_view", "image_url", "altitude_low", "altitude_high", "height_difference", "basic_intro", "drive", "public_transportation", "route"])
        self.setWindowTitle("Search Result")
        self.resize(2000, 2000)
        
        self.new_window_model = QStandardItemModel(1811,31)
        self.new_window_tableview = QTableView(self)
        self.new_window_tableview.setModel(self.new_window_model)
        self.new_window_tableview.move(100,50)
        self.new_window_tableview.resize(1700,950)
        self.new_window_model.setHorizontalHeaderLabels(["步道ID","步道名稱","步道相關資訊網站","步道評分","步道所在地區-1(縣市)","步道所在地區-1(鄉鎮市區)","步道所在地區-2(縣市)","步道所在地區-2(鄉鎮市區)","步道所在地區-3(縣市)","步道所在地區-3(鄉鎮市區)","步道所在地區-4(縣市)","步道所在地區-4(鄉鎮市區)","步道所在地區-5(縣市)","步道所在地區-5(鄉鎮市區)","步道所在地區-6(縣市)","步道所在地區-6(鄉鎮市區)","步道所在地區-7(縣市)","步道所在地區-7(鄉鎮市區)","步道所在地區-8(縣市)","步道所在地區-8(鄉鎮市區)","步道難易度","步道長度","步道攀登時間","步道欲前往人數","步道已前往人數","步道網站點閱人數","步道圖片網址","步道海拔起始高度(公尺)","步道海拔終點高度(公尺)","步道高度落差(公尺)","步道基本資料介紹","開車路線","大眾運輸路線","步道路線"])

        try:
            if value_county == "請選擇縣市":
                if len(search_list) == 4:
                    Final_df = df[region&search_list[0]&search_list[1]&search_list[2]&search_list[3]]
                    if Final_df.empty is True:
                        self.mbox = QtWidgets.QMessageBox(self)
                        self.mbox.setWindowTitle("對不起QQ")
                        self.mbox.setText("您的個人化步道篩選查無資料喔")
                        self.mbox.setIcon(QtWidgets.QMessageBox.Critical)          
                        self.mbox.exec()
                        print("Empty")
                elif len(search_list) == 3:
                    Final_df = df[region&search_list[0]&search_list[1]&search_list[2]]
                    if Final_df.empty is True:
                        self.mbox = QtWidgets.QMessageBox(self)
                        self.mbox.setWindowTitle("對不起QQ")
                        self.mbox.setText("您的個人化步道篩選查無資料喔")
                        self.mbox.setIcon(QtWidgets.QMessageBox.Critical)          
                        self.mbox.exec()
                        print("Empty")
                elif len(search_list) == 2:
                    Final_df = df[region&search_list[0]&search_list[1]]
                    if Final_df.empty is True:
                        self.mbox = QtWidgets.QMessageBox(self)
                        self.mbox.setWindowTitle("對不起QQ")
                        self.mbox.setText("您的個人化步道篩選查無資料喔")
                        self.mbox.setIcon(QtWidgets.QMessageBox.Critical)          
                        self.mbox.exec()
                        print("Empty")
                elif len(search_list) == 1:
                    Final_df = df[region&search_list[0]]
                    if Final_df.empty is True:
                        self.mbox = QtWidgets.QMessageBox(self)
                        self.mbox.setWindowTitle("對不起QQ")
                        self.mbox.setText("您的個人化步道篩選查無資料喔")
                        self.mbox.setIcon(QtWidgets.QMessageBox.Critical)          
                        self.mbox.exec()
                        print("Empty")
                elif len(search_list) == 0:
                    Final_df = df[region]
                    if Final_df.empty is True:
                        self.mbox = QtWidgets.QMessageBox(self)
                        self.mbox.setWindowTitle("對不起QQ")
                        self.mbox.setText("您的個人化步道篩選查無資料喔")
                        self.mbox.setIcon(QtWidgets.QMessageBox.Critical)          
                        self.mbox.exec()
                        print("Empty")
            elif value_county != "請選擇縣市":
                if len(search_list) == 4:
                    Final_df = df[county&search_list[0]&search_list[1]&search_list[2]&search_list[3]]
                    if Final_df.empty is True:
                        self.mbox = QtWidgets.QMessageBox(self)
                        self.mbox.setWindowTitle("對不起QQ")
                        self.mbox.setText("您的個人化步道篩選查無資料喔")
                        self.mbox.setIcon(QtWidgets.QMessageBox.Critical)          
                        self.mbox.exec()
                        print("Empty")
                elif len(search_list) == 3:
                    Final_df = df[county&search_list[0]&search_list[1]&search_list[2]]
                    if Final_df.empty is True:
                        self.mbox = QtWidgets.QMessageBox(self)
                        self.mbox.setWindowTitle("對不起QQ")
                        self.mbox.setText("您的個人化步道篩選查無資料喔")
                        self.mbox.setIcon(QtWidgets.QMessageBox.Critical)          
                        self.mbox.exec()
                        print("Empty")
                elif len(search_list) == 2:
                    Final_df = df[county&search_list[0]&search_list[1]]
                    if Final_df.empty is True:
                        self.mbox = QtWidgets.QMessageBox(self)
                        self.mbox.setWindowTitle("對不起QQ")
                        self.mbox.setText("您的個人化步道篩選查無資料喔")
                        self.mbox.setIcon(QtWidgets.QMessageBox.Critical)          
                        self.mbox.exec()
                        print("Empty")
                elif len(search_list) == 1:
                    Final_df = df[county&search_list[0]]
                    if Final_df.empty is True:
                        self.mbox = QtWidgets.QMessageBox(self)
                        self.mbox.setWindowTitle("對不起QQ")
                        self.mbox.setText("您的個人化步道篩選查無資料喔")
                        self.mbox.setIcon(QtWidgets.QMessageBox.Critical)          
                        self.mbox.exec()
                        print("Empty")
                elif len(search_list) == 0:
                    Final_df = df[county]
                    if Final_df.empty is True:
                        self.mbox = QtWidgets.QMessageBox(self)
                        self.mbox.setWindowTitle("對不起QQ")
                        self.mbox.setText("您的個人化步道篩選查無資料喔")
                        self.mbox.setIcon(QtWidgets.QMessageBox.Critical)          
                        self.mbox.exec()
                        print("Empty")
        except:
            if len(search_list) == 4:
                Final_df = df[search_list[0]&search_list[1]&search_list[2]&search_list[3]]
                if Final_df.empty is True:
                    self.mbox = QtWidgets.QMessageBox(self)
                    self.mbox.setWindowTitle("對不起QQ")
                    self.mbox.setText("您的個人化步道篩選查無資料喔")
                    self.mbox.setIcon(QtWidgets.QMessageBox.Critical)          
                    self.mbox.exec()
                    print("Empty")
            elif len(search_list) == 3:
                Final_df = df[search_list[0]&search_list[1]&search_list[2]]
                if Final_df.empty is True:
                    self.mbox = QtWidgets.QMessageBox(self)
                    self.mbox.setWindowTitle("對不起QQ")
                    self.mbox.setText("您的個人化步道篩選查無資料喔")
                    self.mbox.setIcon(QtWidgets.QMessageBox.Critical)          
                    self.mbox.exec()
                    print("Empty")
            elif len(search_list) == 2:
                Final_df = df[search_list[0]&search_list[1]]
                if Final_df.empty is True:
                    self.mbox = QtWidgets.QMessageBox(self)
                    self.mbox.setWindowTitle("對不起QQ")
                    self.mbox.setText("您的個人化步道篩選查無資料喔")
                    self.mbox.setIcon(QtWidgets.QMessageBox.Critical)          
                    self.mbox.exec()
                    print("Empty")
            elif len(search_list) == 1:
                Final_df = df[search_list[0]]
                if Final_df.empty is True:
                    self.mbox = QtWidgets.QMessageBox(self)
                    self.mbox.setWindowTitle("對不起QQ")
                    self.mbox.setText("您的個人化步道篩選查無資料喔")
                    self.mbox.setIcon(QtWidgets.QMessageBox.Critical)          
                    self.mbox.exec()
                    print("Empty")
            else:
                if self.listwidget.currentIndex().row()	 == 0:
                    Final_df = df.sort_values(["people_gone"],ascending = 0)
                elif self.listwidget.currentIndex().row() == 1:
                    Final_df = df.sort_values(["people_view"],ascending = 0)

        print(Final_df)
        print(len(search_list))
        # print(search_list[0])
        # print(search_list[1])
        if self.listwidget.currentIndex().row()	 == 0:
            sort_final_df = Final_df.sort_values(["people_gone"],ascending = 0)
            for i in range(34):         
                for j in range(len(Final_df)):      
                    self.new_window_model.setItem(j,i,QStandardItem(str(sort_final_df.iat[j,i])))
                i += 1
        elif self.listwidget.currentIndex().row() == 1:
            sort_final_df = Final_df.sort_values(["people_view"],ascending = 0)
            for i in range(34):         
                for j in range(len(Final_df)):      
                    self.new_window_model.setItem(j,i,QStandardItem(str(sort_final_df.iat[j,i])))
                i += 1
        else:
            for i in range(34):         
                for j in range(len(Final_df)):      
                    self.new_window_model.setItem(j,i,QStandardItem(str(Final_df.iat[j,i])))
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