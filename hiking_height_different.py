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

        self.canvas = FigureCanvas(self.hiking_height_diff())
        self.modified_canvas = FigureCanvas(self.hiking_modifed_height_diff())

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

    def hiking_height_diff(self):

        hiking_county_wb = op.load_workbook("excel_python_20230608_hiking.xlsx")
        hiking_county_ws = hiking_county_wb.active

        height_diff_less_250_list = []
        height_diff_250_list = []
        height_diff_500_list = []
        height_diff_750_list = []
        height_diff_1000_list = []

        for i in list(hiking_county_ws.columns)[26]:
            #print(i.value)
            if "步道" in str(i.value):
                pass
            else:
                try:
                    if int(i.value) < 250:
                        height_diff_less_250_list.append(str(i.value))
                    elif 250 < int(i.value) < 500:
                        height_diff_250_list.append(str(i.value))
                    elif 500 < int(i.value) < 750:
                        height_diff_500_list.append(str(i.value))
                    elif 750 < int(i.value) < 1000:
                        height_diff_750_list.append(str(i.value))    
                    elif int(i.value) > 1000:
                        height_diff_1000_list.append(str(i.value))
                except:
                    pass
                
        color = ["b","g","r","c","m"]
        fig, ax = plt.subplots()
        plt.tick_params(labelsize = 6)
        ax.set_title("台灣步道高度落差統計",{"fontsize":20})
        plt.xlabel("數量",{"fontsize":10})   
        plt.ylabel("高度落差(公尺)",{"fontsize":10})  
        number = [len(height_diff_less_250_list),len(height_diff_250_list),len(height_diff_500_list),len(height_diff_750_list),len(height_diff_1000_list)]
        label = ["< 250","250 ~ 500","500 ~ 750","750 ~ 1000","> 1000"]
        plt.barh(label,number,color = color,tick_label = label,height = 0.5) 
        # plt.show()      
        return fig
    
    def hiking_modifed_height_diff(self):

        hiking_county_wb = op.load_workbook("excel_python_20230608_hiking.xlsx")
        hiking_county_ws = hiking_county_wb.active

        height_diff_less_50_list = []
        height_diff_50_list = []
        height_diff_100_list = []
        height_diff_150_list = []
        height_diff_200_list = []

        for i in list(hiking_county_ws.columns)[26]:
            #print(i.value)
            if "步道" in str(i.value):
                pass
            else:
                try:
                    if int(i.value) < 50:
                        height_diff_less_50_list.append(str(i.value))
                    elif 50 < int(i.value) < 100:
                        height_diff_50_list.append(str(i.value))
                    elif 100 < int(i.value) < 150:
                        height_diff_100_list.append(str(i.value))
                    elif 150 < int(i.value) < 200:
                        height_diff_150_list.append(str(i.value))   
                    elif 200 < int(i.value) < 250:
                        height_diff_200_list.append(str(i.value))    
                except:
                    pass
                
        color = ["b","g","r","c","m"]
        fig, ax = plt.subplots()
        plt.tick_params(labelsize = 6)
        ax.set_title("台灣步道高度落差250公尺以內統計",{"fontsize":20})
        plt.xlabel("數量",{"fontsize":10})   
        plt.ylabel("高度落差(公尺)",{"fontsize":10})  
        number = [len(height_diff_less_50_list),len(height_diff_50_list),len(height_diff_100_list),len(height_diff_150_list),len(height_diff_200_list)]
        label = ["< 50","50 ~ 100","100 ~ 150","150 ~ 200","200 ~ 250"]
        plt.barh(label,number,color = color,tick_label = label,height = 0.5) 
        # plt.show()
        return fig

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = MyWidget()
    Form.show()    
    sys.exit(app.exec_())
