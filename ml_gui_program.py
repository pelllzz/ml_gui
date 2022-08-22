from cgitb import text
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
import sys, pickle
from data_visulize import data_
from table_display import DataFrameModel

# Create UI Class
class UI(QMainWindow):
    # Main UI
    def __init__(self) :
        super(UI, self).__init__()
        uic.loadUi("ui_files/mainWindow.ui", self)
        #self.show()

        global data, setps
        data = data_()

        # Layout Parameters
        # 얘네들 중에 Nonetype 에러가 뜬다면 designer에서 이름이랑 타입이 맞는지 확인부터 해봅시다
        self.Browse = self.findChild(QPushButton, "Browse")
        self.columns = self.findChild(QListWidget, "columnList")
        self.table = self.findChild(QTableView, "tableView")
        self.data_shape = self.findChild(QLabel, "shape")
        self.submit = self.findChild(QPushButton, "submit")
        self.target_name = self.findChild(QLabel, "target_name") 
        self.drop_column = self.findChild(QComboBox, "dropColumn")
        self.drop_button = self.findChild(QPushButton, "drop_btn")
        self.scaler = self.findChild(QComboBox, "sclaer")
        self.scale_btn = self.findChild(QPushButton, "scale_btn")

        # Warning : Encoding Issue
        # CSV Encoding에 문제가 있는 경우 현재 제대로 열리지 않는 현상 있음 (UTF8 이라던가)
        self.Browse.clicked.connect(self.get_csv)

        # columns 안에 있는 target을 클릭해봅시다
        self.columns.clicked.connect(self.find_target)

        # Scaling Target Function
        self.submit.clicked.connect(self.set_target)

        # Drop Target Function
        self.drop_button.clicked.connect(self.dropC)

        # Scale Value Setting Function
        self.scale_btn.clicked.connect(self.scale_value)

    # File Upload (Select Data File)
    def filldetails(self, flag = 1):
        if flag == 0:
            self.df = data_.read_file(self, str(self.file_path))

        #print(type(self.columns))
        self.columns.clear()
        self.column_list = data_.get_column_list(self, self.df)
        # print(self.column_list)
        
        # Get Data.columns & Type
        for i, j in enumerate(self.column_list):
            stri = f'{j} ------ {self.df[j].dtype}'
            print(stri)
            self.columns.insertItem(i, stri)

        x, y = self.df.shape
        self.data_shape.setText(f'({x}, {y})')
        self.fill_comboBox()

    def fill_comboBox(self):
        # 컬럼 DROP 리스트를 위한 fill_comboBox
        # print(type(self.scaler))
        # print(type(self.drop_column))
        self.drop_column.clear()
        self.drop_column.addItems(self.column_list)

        # 컬럼 확인을 위한 fill_comboBox
        x = DataFrameModel(self.df)
        self.table.setModel(x)
        
    def find_target(self):
        self.item = self.columns.currentItem().text().split(' ')[0]
        print(self.columns.currentItem().text().split(' ')[0])

    def set_target(self):
        self.target_value = self.item
        self.target_name.setText(self.target_value)

    def dropC(self):
        selected = self.drop_column.currentText()
        self.df = data.drop_columns(self.df, selected)
        self.filldetails()

    def scale_value(self):
        if self.scaler.currentText() == 'Standard Scaler':
            data.standard_scaler(self.df, self.target_value)
        elif self.scaler.currentText() == 'Min-Max Scaler':
            data.minMax_scaler(self.df, self.target_value)
        elif self.scaler.currentText() == 'Power Scaler':
            data.power_scaler(self.df, self.target_value)
        else:
            data.robuster_scaler(self.df, self.target_value)

        self.filldetails()

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