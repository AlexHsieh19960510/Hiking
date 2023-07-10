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
        self.setWindowTitle("Hiking Difficulty")
        self.resize(750, 600)
        self.ui()
        # self.hiking_county()
        # self.hiking_new_taipei_city()

    def ui(self):

        self.canvas = FigureCanvas(self.hiking_difficulty())

        self.graphicview = QtWidgets.QGraphicsView(self)
        self.graphicview.setGeometry(50, 50, 600, 500)
        
        self.graphicscene = QtWidgets.QGraphicsScene()
        self.graphicscene.setSceneRect(0, 0, 580, 480)
        self.graphicscene.addWidget(self.canvas)
        
        self.graphicview.setScene(self.graphicscene)

    def hiking_difficulty(self):

        hiking_county_wb = op.load_workbook("excel_python_20230608_hiking.xlsx")
        hiking_county_ws = hiking_county_wb.active

        score_list = []
        score_dict = {}

        for i in list(hiking_county_ws.columns)[19]:
            #print(i.value)
            if "步道" in str(i.value):
                pass
            else:
                score_list.append(str(i.value))
                if str(i.value) in score_dict:
                    score_dict[str(i.value)] = score_dict.get(str(i.value), 0) + 1
                    #score_dict[str(i.value)] += 1
                else:
                    score_dict[str(i.value)] = 1
        print(score_dict)

        score = []
        number_score = []
        for i in score_dict:
            score.append(i)
            number_score.append(score_dict[i])
        print(score)
        print(number_score)

        color = ["b","g","r","c","m"]
        fig, ax = plt.subplots()
        ax.set_title("台灣步道難易度統計",{"fontsize":20})
        plt.xlabel("數量",{"fontsize":15})   
        plt.ylabel("難易度",{"fontsize":15})  
        plt.barh(score,number_score,color = color,tick_label = score,height = 0.5) 
        # plt.show()
        return fig

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = MyWidget()
    Form.show()    
    sys.exit(app.exec_())
