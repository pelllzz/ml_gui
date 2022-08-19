from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
import sys, pickle
from data_visulize import data_

# Create UI Class
class UI(QMainWindow):
    def __init__(self) :
        super(UI, self).__init__()
        uic.loadUi("ui_files/mainWindow.ui", self)
        #self.show()

        global data, setps
        data = data_()
        
        self.Browse = self.findChild(QPushButton, "Browse")
        self.columns = self.findChild(QListWidget, "columnList")

        self.Browse.clicked.connect(self.get_csv)

    def filldetails(self, flag = 1):
        if flag == 0:
            self.df = data_.read_file(self, str(self.file_path))

        self.columns.clear()
        self.column_list = data_.get_column_list(self, self.df)
        #print(self.column_list)
        
        for i, j in enumerate(self.column_list):
            stri = f'{j}------{self.df[j].dtype}'
            print(stri)
            self.columns.insertItem(i, stri)


    def get_csv(self):
        self.file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "csv(*.csv)")
        self.columns.clear()

        if self.file_path != "":
            self.filldetails(0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    window.show()
    sys.exit(app.exec_())