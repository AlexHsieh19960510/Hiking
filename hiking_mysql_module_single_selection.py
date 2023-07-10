from PyQt5 import QtWidgets, QtGui
import sys
import pymysql
from PyQt5.QtWidgets import QTableWidget, QTableView, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem

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
        self.box_region.currentIndexChanged.connect(self.ui_county)
        self.label_region.setStyleSheet("font-size:20px;font-weight:bold;")
        
        self.label_county = QtWidgets.QLabel(window)
        self.label_county.setText("縣市:")
        self.label_county.setGeometry(200,500,200,30)
        self.box_county = QtWidgets.QComboBox(window)
        box_county_warning = ["請先選擇地區再選擇縣市"]
        self.box_county.addItems(box_county_warning)
        self.box_county.setGeometry(300,500,200,30)
        self.box_county.currentIndexChanged.connect(self.search_county)
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

    def ui_county(self):
        global value_region, data_search, cursor_search
        cursor_search= db.cursor()
        value_region = self.box_region.currentText()
        if value_region == "請選擇地區":
            pass
        elif value_region == "北部":
            self.box_county.clear()
            self.box_county.addItems(North)
            cursor_search.execute('''select * from hiking_information where hiking_information.county_1 = '台北市' or hiking_information.county_1 = '新北市' or hiking_information.county_1 = '基隆市' or hiking_information.county_1 = '桃園市' or hiking_information.county_1 = '新竹縣' or hiking_information.county_1 = '新竹市' or hiking_information.county_1 = '宜蘭縣' or
                hiking_information.county_2 = '台北市' or hiking_information.county_2 = '新北市' or hiking_information.county_2 = '基隆市' or hiking_information.county_2 = '桃園市' or hiking_information.county_2 = '新竹縣' or hiking_information.county_2 = '新竹市' or hiking_information.county_2 = '宜蘭縣' or
                hiking_information.county_3 = '台北市' or hiking_information.county_3 = '新北市' or hiking_information.county_3 = '基隆市' or hiking_information.county_3 = '桃園市' or hiking_information.county_3 = '新竹縣' or hiking_information.county_3 = '新竹市' or hiking_information.county_3 = '宜蘭縣' or
                hiking_information.county_4 = '台北市' or hiking_information.county_4 = '新北市' or hiking_information.county_4 = '基隆市' or hiking_information.county_4 = '桃園市' or hiking_information.county_4 = '新竹縣' or hiking_information.county_4 = '新竹市' or hiking_information.county_4 = '宜蘭縣' or
                hiking_information.county_5 = '台北市' or hiking_information.county_5 = '新北市' or hiking_information.county_5 = '基隆市' or hiking_information.county_5 = '桃園市' or hiking_information.county_5 = '新竹縣' or hiking_information.county_5 = '新竹市' or hiking_information.county_5 = '宜蘭縣' or
                hiking_information.county_6 = '台北市' or hiking_information.county_6 = '新北市' or hiking_information.county_6 = '基隆市' or hiking_information.county_6 = '桃園市' or hiking_information.county_6 = '新竹縣' or hiking_information.county_6 = '新竹市' or hiking_information.county_6 = '宜蘭縣' or
                hiking_information.county_7 = '台北市' or hiking_information.county_7 = '新北市' or hiking_information.county_7 = '基隆市' or hiking_information.county_7 = '桃園市' or hiking_information.county_7 = '新竹縣' or hiking_information.county_7 = '新竹市' or hiking_information.county_7 = '宜蘭縣' or
                hiking_information.county_8 = '台北市' or hiking_information.county_8 = '新北市' or hiking_information.county_8 = '基隆市' or hiking_information.county_8 = '桃園市' or hiking_information.county_8 = '新竹縣' or hiking_information.county_8 = '新竹市' or hiking_information.county_8 = '宜蘭縣';''')
            data_search = cursor_search.fetchall()
            self.box_region.currentIndexChanged.connect(self.ui_search)
            print(data_search)
            return data_search  
        elif value_region == "中部":
            self.box_county.clear()
            self.box_county.addItems(Center)
            cursor_search.execute('''select * from hiking_information where hiking_information.county_1 = '苗栗縣' or hiking_information.county_1 = '台中市' or hiking_information.county_1 = '彰化縣' or hiking_information.county_1 = '南投縣' or hiking_information.county_1 = '雲林縣' or
                hiking_information.county_2 = '苗栗縣' or hiking_information.county_2 = '台中市' or hiking_information.county_2 = '彰化縣' or hiking_information.county_2 = '南投縣' or hiking_information.county_2 = '雲林縣' or
                hiking_information.county_3 = '苗栗縣' or hiking_information.county_3 = '台中市' or hiking_information.county_3 = '彰化縣' or hiking_information.county_3 = '南投縣' or hiking_information.county_3 = '雲林縣' or
                hiking_information.county_4 = '苗栗縣' or hiking_information.county_4 = '台中市' or hiking_information.county_4 = '彰化縣' or hiking_information.county_4 = '南投縣' or hiking_information.county_4 = '雲林縣' or
                hiking_information.county_5 = '苗栗縣' or hiking_information.county_5 = '台中市' or hiking_information.county_5 = '彰化縣' or hiking_information.county_5 = '南投縣' or hiking_information.county_5 = '雲林縣' or
                hiking_information.county_6 = '苗栗縣' or hiking_information.county_6 = '台中市' or hiking_information.county_6 = '彰化縣' or hiking_information.county_6 = '南投縣' or hiking_information.county_6 = '雲林縣' or
                hiking_information.county_7 = '苗栗縣' or hiking_information.county_7 = '台中市' or hiking_information.county_7 = '彰化縣' or hiking_information.county_7 = '南投縣' or hiking_information.county_7 = '雲林縣' or
                hiking_information.county_8 = '苗栗縣' or hiking_information.county_8 = '台中市' or hiking_information.county_8 = '彰化縣' or hiking_information.county_8 = '南投縣' or hiking_information.county_8 = '雲林縣';''')
            data_search = cursor_search.fetchall()
            self.box_region.currentIndexChanged.connect(self.ui_search)
            print(data_search)
            return data_search
        elif value_region == "南部":
            self.box_county.clear()
            self.box_county.addItems(South)    
            cursor_search.execute('''select * from hiking_information where hiking_information.county_1 = '嘉義市' or hiking_information.county_1 = '嘉義縣' or hiking_information.county_1 = '台南市' or hiking_information.county_1 = '高雄市' or hiking_information.county_1 = '屏東縣' or hiking_information.county_1 = '澎湖縣' or
                hiking_information.county_2 = '嘉義市' or hiking_information.county_2 = '嘉義縣' or hiking_information.county_2 = '台南市' or hiking_information.county_2 = '高雄市' or hiking_information.county_2 = '屏東縣' or hiking_information.county_2 = '澎湖縣' or
                hiking_information.county_3 = '嘉義市' or hiking_information.county_3 = '嘉義縣' or hiking_information.county_3 = '台南市' or hiking_information.county_3 = '高雄市' or hiking_information.county_3 = '屏東縣' or hiking_information.county_3 = '澎湖縣' or 
                hiking_information.county_4 = '嘉義市' or hiking_information.county_4 = '嘉義縣' or hiking_information.county_4 = '台南市' or hiking_information.county_4 = '高雄市' or hiking_information.county_4 = '屏東縣' or hiking_information.county_4 = '澎湖縣' or
                hiking_information.county_5 = '嘉義市' or hiking_information.county_5 = '嘉義縣' or hiking_information.county_5 = '台南市' or hiking_information.county_5 = '高雄市' or hiking_information.county_5 = '屏東縣' or hiking_information.county_5 = '澎湖縣' or
                hiking_information.county_6 = '嘉義市' or hiking_information.county_6 = '嘉義縣' or hiking_information.county_6 = '台南市' or hiking_information.county_6 = '高雄市' or hiking_information.county_6 = '屏東縣' or hiking_information.county_6 = '澎湖縣' or
                hiking_information.county_7 = '嘉義市' or hiking_information.county_7 = '嘉義縣' or hiking_information.county_7 = '台南市' or hiking_information.county_7 = '高雄市' or hiking_information.county_7 = '屏東縣' or hiking_information.county_7 = '澎湖縣' or 
                hiking_information.county_8 = '嘉義市' or hiking_information.county_8 = '嘉義縣' or hiking_information.county_8 = '台南市' or hiking_information.county_8 = '高雄市' or hiking_information.county_8 = '屏東縣' or hiking_information.county_8 = '澎湖縣';''')
            data_search = cursor_search.fetchall()
            self.box_region.currentIndexChanged.connect(self.ui_search)
            print(data_search)
            return data_search
        elif value_region == "東部":
            self.box_county.clear()
            self.box_county.addItems(East)    
            cursor_search.execute('''select * from hiking_information where hiking_information.county_1 = '花蓮縣' or hiking_information.county_1 = '台東縣' or
                hiking_information.county_2 = '花蓮縣' or hiking_information.county_2 = '台東縣' or
                hiking_information.county_3 = '花蓮縣' or hiking_information.county_3 = '台東縣' or
                hiking_information.county_4 = '花蓮縣' or hiking_information.county_4 = '台東縣' or
                hiking_information.county_5 = '花蓮縣' or hiking_information.county_5 = '台東縣' or
                hiking_information.county_6 = '花蓮縣' or hiking_information.county_6 = '台東縣' or
                hiking_information.county_7 = '花蓮縣' or hiking_information.county_7 = '台東縣' or
                hiking_information.county_8 = '花蓮縣' or hiking_information.county_8 = '台東縣';''')
            data_search = cursor_search.fetchall()
            self.box_region.currentIndexChanged.connect(self.ui_search)
            print(data_search)
            return data_search
        elif value_region == "離島":
            self.box_county.clear()
            self.box_county.addItems(Outlying_Island)
            cursor_search.execute('''select * from hiking_information where hiking_information.county_1 = '金門縣' or hiking_information.county_1 = '連江縣' or
                hiking_information.county_2 = '金門縣' or hiking_information.county_2 = '連江縣' or
                hiking_information.county_3 = '金門縣' or hiking_information.county_3 = '連江縣' or
                hiking_information.county_4 = '金門縣' or hiking_information.county_4 = '連江縣' or
                hiking_information.county_5 = '金門縣' or hiking_information.county_5 = '連江縣' or
                hiking_information.county_6 = '金門縣' or hiking_information.county_6 = '連江縣' or
                hiking_information.county_7 = '金門縣' or hiking_information.county_7 = '連江縣' or
                hiking_information.county_8 = '金門縣' or hiking_information.county_8 = '連江縣';''')
            data_search = cursor_search.fetchall()
            self.box_region.currentIndexChanged.connect(self.ui_search)
            print(data_search)    
            return data_search    

    def search_county(self):
        global value_county, data_search, cursor_search
        value_county = self.box_county.currentText()
        cursor_search = db.cursor()
        cursor_search.execute("select * from hiking_information where hiking_information.county_1 = '"+value_county+"' or hiking_information.county_2 = '"+value_county+"' or hiking_information.county_3 = '"+value_county+"' or hiking_information.county_4 = '"+value_county+"' or hiking_information.county_5 = '"+value_county+"' or hiking_information.county_6 = '"+value_county+"' or hiking_information.county_7 = '"+value_county+"' or hiking_information.county_8 = '"+value_county+"';")
        data_search = cursor_search.fetchall()
        print(data_search)
        self.box_county.currentIndexChanged.connect(self.ui_search)
        return data_search

    def search_difficulty(self):
        global data_search, cursor_search
        cursor_search = db.cursor()
        if rb_1.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.difficulty = 1;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_2.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.difficulty = 2;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_3.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.difficulty = 3;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_4.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.difficulty = 4;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_5.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.difficulty = 5;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        
    def search_distance(self):
        global data_search, cursor_search
        cursor_search = db.cursor()
        if rb_less_5.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.distance < 5;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_5_10.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.distance between 5 and 10;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_10_15.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.distance between 10 and 15;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_15_20.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.distance between 15 and 20;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_20_25.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.distance between 20 and 25;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_25_50.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.distance between 25 and 50;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_50_75.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.distance between 50 and 75;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_75_100.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.distance between 75 and 100;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search

    def search_altitude(self):
        global data_search, cursor_search
        cursor_search = db.cursor()
        if rb_less_altitude_250.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.altitude_low < 250 or hiking_information.altitude_high < 250;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_altitude_250.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.altitude_low between 250 and 500 or hiking_information.altitude_high between 250 and 500;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_altitude_500.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.altitude_low between 500 and 750 or hiking_information.altitude_high between 500 and 750;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_altitude_750.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.altitude_low between 750 and 1000 or hiking_information.altitude_high between 750 and 1000;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_altitude_1000.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.altitude_low between 1000 and 2000 or hiking_information.altitude_high between 1000 and 2000;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_altitude_2000.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.altitude_low between 2000 and 3000 or hiking_information.altitude_high between 2000 and 3000;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_altitude_3000.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.altitude_low > 3000 or hiking_information.altitude_high > 3000;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search

    def search_height_difference(self):
        global data_search, cursor_search
        cursor_search = db.cursor()
        if rb_less_height_difference_50.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.height_difference < 50;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_height_difference_50.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.height_difference between 50 and 100;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_height_difference_100.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.height_difference between 100 and 150;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_height_difference_150.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.height_difference between 150 and 200;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_height_difference_200.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.height_difference between 200 and 500;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_height_difference_500.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.height_difference between 500 and 750;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_height_difference_750.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.height_difference between 750 and 1000;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif rb_height_difference_1000.isChecked():
            cursor_search.execute("select * from hiking_information where hiking_information.height_difference > 1000;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search

    def search_popular(self):
        global data_search, cursor_search
        cursor_search = db.cursor()
        if self.listwidget.currentItem().text() == "已前往人數排名":
            cursor_search.execute("select * from hiking_information order by hiking_information.people_gone desc;")
            data_search = cursor_search.fetchall()
            print(data_search)
            return data_search
        elif self.listwidget.currentItem().text() == "網站點閱人數排名":
            cursor_search.execute("select * from hiking_information order by hiking_information.people_view desc;")
            data_search = cursor_search.fetchall()
            print(data_search)
            # print(data_search_popular[0])
            # print(data_search_popular[0][0])
            # print(data_search_popular[0][0][0])
            return data_search

    def search_result_window(self):
        self.setWindowTitle("Search Result")
        self.resize(2000, 2000)
        
        self.new_window_model = QStandardItemModel(1811,31)
        self.new_window_tableview = QTableView(self)
        self.new_window_tableview.setModel(self.new_window_model)
        self.new_window_tableview.move(100,50)
        self.new_window_tableview.resize(1700,950)
        self.new_window_model.setHorizontalHeaderLabels(["步道名稱","步道相關資訊網站","步道評分","步道所在地區-1(縣市)","步道所在地區-1(鄉鎮市區)","步道所在地區-2(縣市)","步道所在地區-2(鄉鎮市區)","步道所在地區-3(縣市)","步道所在地區-3(鄉鎮市區)","步道所在地區-4(縣市)","步道所在地區-4(鄉鎮市區)","步道所在地區-5(縣市)","步道所在地區-5(鄉鎮市區)","步道所在地區-6(縣市)","步道所在地區-6(鄉鎮市區)","步道所在地區-7(縣市)","步道所在地區-7(鄉鎮市區)","步道所在地區-8(縣市)","步道所在地區-8(鄉鎮市區)","步道難易度","步道長度","步道攀登時間","步道欲前往人數","步道已前往人數","步道網站點閱人數","步道圖片網址","步道海拔起始高度(公尺)","步道海拔終點高度(公尺)","步道高度落差(公尺)","步道基本資料介紹","開車路線","大眾運輸路線","步道路線"])

        for i in range(33):          #欄
            for j in range(len(data_search)):      #列
                self.new_window_model.setItem(j,i,QStandardItem(str(data_search[j][i])))
                j += 1
            i += 1
        self.show()

if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Main_Window()
    ui.main_window(Widget)
    ui.ui_county
    Widget.show()

    setting = {
    "host" : "localhost",
    "port" : 3306,
    "user" : "root",
    "password" : "sandia100alex",
    "db" : "hiking",
    "charset" : "utf8"
    }
            
    db = pymysql.connect(**setting)
    cursor = db.cursor()

    cursor.execute("show databases;")
    data_test = cursor.fetchall()
    print(data_test)   
    
    sys.exit(app.exec_())