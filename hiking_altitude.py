from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import openpyxl as op
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
matplotlib.rc("font", family = "Microsoft JhengHei")
matplotlib.use("Qt5Agg")

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hiking Distance")
        self.resize(1500, 1000)
        self.ui()
        # self.hiking_county()
        # self.hiking_new_taipei_city()

    def ui(self):

        self.canvas = FigureCanvas(self.hiking_altitude())
        self.modified_canvas = FigureCanvas(self.hiking_modifed_altitude())

        self.graphicview = QtWidgets.QGraphicsView(self)
        self.graphicview.setGeometry(50, 250, 600, 500)
        self.modified_graphicview = QtWidgets.QGraphicsView(self)
        self.modified_graphicview.setGeometry(750, 250, 600, 500)
        
        self.graphicscene = QtWidgets.QGraphicsScene()
        self.graphicscene.setSceneRect(0, 0, 580, 480)
        self.graphicscene.addWidget(self.canvas)
        self.modified_graphicscene = QtWidgets.QGraphicsScene()
        self.modified_graphicscene.setSceneRect(0, 0, 580, 480)
        self.modified_graphicscene.addWidget(self.modified_canvas)
        
        self.graphicview.setScene(self.graphicscene)
        self.modified_graphicview.setScene(self.modified_graphicscene)

    def hiking_altitude(self):

        hiking_county_wb = op.load_workbook("excel_python_20230608_hiking.xlsx")
        hiking_county_ws = hiking_county_wb.active

        altitude_less_1000_list = []
        altitude_1000_list = []
        altitude_2000_list = []
        altitude_3000_list = []

        for i in list(hiking_county_ws.columns)[25]:
            #print(i.value)
            #print(i.value.split("~"))
            #print(i.value.split("~")[0])
            #print(i.value.split("~")[1])
            if "步道" in i.value:
                pass
            else:
                try:
                    altitude = i.value.split("~")[1]
                except:
                    pass
                if int(altitude) < 1000:
                    altitude_less_1000_list.append(i.value)
                elif 1000 < int(altitude) < 2000:
                    altitude_1000_list.append(i.value)
                elif 2000 < int(altitude) < 3000:
                    altitude_2000_list.append(i.value)
                elif int(altitude) > 3000:
                    altitude_3000_list.append(i.value)
                    
        color = ["b","g","r","c"]
        fig, ax = plt.subplots()
        plt.tick_params(labelsize = 6)
        ax.set_title("台灣步道海拔統計",{"fontsize":20})
        plt.xlabel("數量",{"fontsize":10})   
        plt.ylabel("海拔(公尺)",{"fontsize":10})  
        number = [len(altitude_less_1000_list),len(altitude_1000_list),len(altitude_2000_list),len(altitude_3000_list)]
        label = ["< 1000","1000 ~ 2000","2000 ~ 3000","> 3000"]
        plt.barh(label,number,color = color,tick_label = label,height = 0.5) 
        # plt.show()        
        return fig
    
    def hiking_modifed_altitude(self):

        hiking_county_wb = op.load_workbook("excel_python_20230608_hiking.xlsx")
        hiking_county_ws = hiking_county_wb.active

        altitude_less_250_list = []
        altitude_250_list = []
        altitude_500_list = []
        altitude_750_list = []

        for i in list(hiking_county_ws.columns)[25]:
            #print(i.value)
            #print(i.value.split("~"))
            #print(i.value.split("~")[0])
            #print(i.value.split("~")[1])
            if "步道" in i.value:
                pass
            else:
                try:
                    altitude = i.value.split("~")[1]
                except:
                    pass
                if int(altitude) < 250:
                    altitude_less_250_list.append(i.value)
                elif 250 < int(altitude) < 500:
                    altitude_250_list.append(i.value)
                elif 500 < int(altitude) < 750:
                    altitude_500_list.append(i.value)
                elif 750 < int(altitude) < 1000:
                    altitude_750_list.append(i.value)
                    
        color = ["b","g","r","c"]
        fig, ax = plt.subplots()
        plt.tick_params(labelsize = 6)
        ax.set_title("台灣步道海拔低於1000公尺統計",{"fontsize":20})
        plt.xlabel("數量",{"fontsize":10})   
        plt.ylabel("海拔(公尺)",{"fontsize":10})  
        number = [len(altitude_less_250_list),len(altitude_250_list),len(altitude_500_list),len(altitude_750_list)]
        label = ["< 250","250 ~ 500","500 ~ 750","750 ~ 1000"]
        plt.barh(label,number,color = color,tick_label = label,height = 0.5) 
        # plt.show()      
        return fig

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = MyWidget()
    Form.show()    
    sys.exit(app.exec_())
