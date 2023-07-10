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

        self.canvas = FigureCanvas(self.hiking_distance())
        self.modified_canvas = FigureCanvas(self.hiking_modifed_distance())

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

    def hiking_distance(self):

        hiking_county_wb = op.load_workbook("excel_python_20230608_hiking.xlsx")
        hiking_county_ws = hiking_county_wb.active

        distance_less_25_list = []
        distance_25_list = []
        distance_50_list = []
        distance_75_list = []

        for i in list(hiking_county_ws.columns)[20]:
            #print(i.value)
            if "步道" in str(i.value):
                pass
            else:
                try:
                    if int(i.value) < 25:
                        distance_less_25_list.append(str(i.value))
                    elif 25 < int(i.value) < 50:
                        distance_25_list.append(str(i.value))
                    elif 50 < int(i.value) < 75:
                        distance_50_list.append(str(i.value))
                    elif 75 < int(i.value) < 100:
                        distance_75_list.append(str(i.value))    
                except:
                    pass

        color = ["b","g","r","c"]
        fig, ax = plt.subplots()
        plt.tick_params(labelsize = 8)
        ax.set_title("台灣步道長度統計",{"fontsize":20})
        plt.xlabel("數量",{"fontsize":10})   
        plt.ylabel("長度(單位:公里)",{"fontsize":10})  
        number = [len(distance_less_25_list),len(distance_25_list),len(distance_50_list),len(distance_75_list)]
        label = ["< 25","25 ~ 50","50 ~ 75","75 ~ 100"]
        plt.barh(label,number,color = color,tick_label = label,height = 0.5) 
        # plt.show()
        return fig
    
    def hiking_modifed_distance(self):
        
        hiking_county_wb = op.load_workbook("excel_python_20230608_hiking.xlsx")
        hiking_county_ws = hiking_county_wb.active

        distance_less_5_list = []
        distance_10_list = []
        distance_15_list = []
        distance_20_list = []
        distance_25_list = []

        for i in list(hiking_county_ws.columns)[20]:
            #print(i.value)
            if "步道" in str(i.value):
                pass
            else:
                try:
                    if int(i.value) < 5:
                        distance_less_5_list.append(str(i.value))
                    elif 5 < int(i.value) < 10:
                        distance_10_list.append(str(i.value))
                    elif 10 < int(i.value) < 15:
                        distance_15_list.append(str(i.value))
                    elif 15 < int(i.value) < 20:
                        distance_20_list.append(str(i.value))  
                    elif 20 < int(i.value) < 25:
                        distance_25_list.append(str(i.value))    
                except:
                    pass

        color = ["b","g","r","c","m"]
        fig, ax = plt.subplots()
        plt.tick_params(labelsize = 8)
        ax.set_title("台灣步道長度25公里以內統計",{"fontsize":20})
        plt.xlabel("數量",{"fontsize":10})   
        plt.ylabel("長度(單位:公里)",{"fontsize":10})  
        number = [len(distance_less_5_list),len(distance_10_list),len(distance_15_list),len(distance_20_list),len(distance_25_list)]
        label = ["< 5","5 ~ 10","10 ~ 15","15 ~ 20","20 ~ 25"]
        plt.barh(label,number,color = color,tick_label = label,height = 0.5) 
        # plt.show()
        return fig

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = MyWidget()
    Form.show()    
    sys.exit(app.exec_())
