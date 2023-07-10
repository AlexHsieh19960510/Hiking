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
        self.setWindowTitle("Hiking Distribution")
        self.resize(1500, 1000)
        self.ui()
        # self.hiking_county()
        # self.hiking_new_taipei_city()

    def ui(self):

        self.county_canvas = FigureCanvas(self.hiking_county())
        self.new_taipei_city_canvas = FigureCanvas(self.hiking_new_taipei_city())

        self.county_graphicview = QtWidgets.QGraphicsView(self)
        self.county_graphicview.setGeometry(50, 250, 600, 500)
        self.new_taipei_city_graphicview = QtWidgets.QGraphicsView(self)
        self.new_taipei_city_graphicview.setGeometry(750, 250, 600, 500)
        
        self.county_graphicscene = QtWidgets.QGraphicsScene()
        self.county_graphicscene.setSceneRect(0, 0, 580, 480)
        self.county_graphicscene.addWidget(self.county_canvas)
        self.new_taipei_city_graphicscene = QtWidgets.QGraphicsScene()
        self.new_taipei_city_graphicscene.setSceneRect(0, 0, 580, 480)
        self.new_taipei_city_graphicscene.addWidget(self.new_taipei_city_canvas)
        
        self.county_graphicview.setScene(self.county_graphicscene)
        self.new_taipei_city_graphicview.setScene(self.new_taipei_city_graphicscene)

    def hiking_county(self):

        hiking_county_wb = op.load_workbook("excel_python_20230608_hiking.xlsx")
        hiking_county_ws = hiking_county_wb.active

        county_list = []
        county_dict = {}
        n = 3
        while n < 19:
            for i in list(hiking_county_ws.columns)[n]:
                if "步道" in i.value:
                    pass
                else:
                    county_list.append(i.value)
                    if i.value in county_dict:
                        county_dict[i.value] = county_dict.get(i.value, 0) + 1
                        #county_dict[i.value] += 1
                    else:
                        county_dict[i.value] = 1
            n += 2
            
        del county_dict["香港"]
        del county_dict["西班牙"]
        del county_dict[" "]
        print(county_dict)

        county = []
        number = []
        for i in county_dict:
            county.append(i)
            number.append(county_dict[i])

        color = ["b","g","r","c","m","y","k","tab:blue","tab:orange","tab:green","tab:red","tab:purple","tab:brown","tab:pink","tab:gray","tab:olive","tab:cyan","yellow","lime","tan","dodgerblue","magenta"]
        fig, ax = plt.subplots()
        ax.set_title("台灣各縣市步道數",{"fontsize":20})
        plt.xlabel("數量",{"fontsize":15})   
        plt.ylabel("縣市",{"fontsize":15})  
        plt.barh(county,number,color = color,tick_label = county,height = 0.5) 
        # plt.show()
        return fig
    
    def hiking_new_taipei_city(self):

        hiking_county_wb = op.load_workbook("excel_python_20230608_hiking.xlsx")
        hiking_county_ws = hiking_county_wb.active

        new_taipei_township_list = []
        new_taipei_township_dict = {}
        m = 3
        while m < 19:
            for i in list(hiking_county_ws.columns)[m]:
                if "步道" in i.value:
                    pass
                elif "新北市" in i.value:
                    column = list(hiking_county_ws.columns)[m].index(i) 
                    #print(i.value,column)
                    township = list(hiking_county_ws.columns)[m+1][column]
                    #print(township.value)
                    new_taipei_township_list.append(township.value)
                    if township.value in new_taipei_township_dict:
                        new_taipei_township_dict[township.value] = new_taipei_township_dict.get(township.value, 0) + 1
                        #new_taipei_township_dict[township.value] += 1
                    else:
                        new_taipei_township_dict[township.value] = 1
            m += 2
        print(new_taipei_township_dict)

        new_taipei_township = []
        number_new_taipei_township = []
        for i in new_taipei_township_dict:
            new_taipei_township.append(i)
            number_new_taipei_township.append(new_taipei_township_dict[i])
        #print(new_taipei_township)
        #print(number_new_taipei_township)

        color = ["b","g","r","c","m","y","k","tab:blue","tab:orange","tab:green","tab:red","tab:purple","tab:brown","tab:pink","tab:gray","tab:olive","tab:cyan","yellow","lime","tan","dodgerblue","magenta","royalblue","mediumslateblue","mediumaquamarine","goldenrod"]
        fig, ax = plt.subplots()
        ax.set_title("新北市各區步道數",{"fontsize":20})
        plt.xlabel("數量",{"fontsize":15})   
        plt.ylabel("行政區",{"fontsize":15})  
        plt.barh(new_taipei_township,number_new_taipei_township,color = color,tick_label = new_taipei_township,height = 0.5) 
        # plt.show()
        return fig



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = MyWidget()
    Form.show()    
    sys.exit(app.exec_())