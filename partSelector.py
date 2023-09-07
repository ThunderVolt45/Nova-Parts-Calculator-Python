import sys
import json
import constant
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_partSelector = uic.loadUiType("partSelector.ui")[0]

class partSelector(QDialog, QWidget, form_partSelector):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        # 초기화
        self.value = 0
        
        # QComboBox 기능 연결
        self.comboBox.currentIndexChanged.connect(self.selector)
        
        # QPushButton 기능 연결
        self.select.clicked.connect(self.confirm)
        self.cancel.clicked.connect(self.exit)
        
        # 두 번째 창 실행
        self.show()
        
    # 메인 창으로부터 메시지 수신
    @QtCore.pyqtSlot(list)
    def on_signal_from_main(self, value):
        self.comboBox.clear()
        
        data = None
        
        # 왜 파이썬에는 switch문이 없지? (진짜 모름)
        if value[0] == constant.LEG :
            with open(constant.FILE_PATH_LEG, "r", encoding = "UTF-8") as file :
                data = json.load(file)
                
        elif value[0] == constant.BODY :
            with open(constant.FILE_PATH_BODY, "r", encoding = "UTF-8") as file :
                data = json.load(file)
                
        elif value[0] == constant.WEAPON :
            with open(constant.FILE_PATH_WEAPON, "r", encoding = "UTF-8") as file :
                data = json.load(file)
            
        elif value[0] == constant.ACC :
            with open(constant.FILE_PATH_ACC, "r", encoding = "UTF-8") as file :
                data = json.load(file)
        
        for i in range(len(data["ID"])):
            self.comboBox.addItem(data["Name"][i])
        self.comboBox.setCurrentIndex(value[1])
        self.value = value[1]
            
    def selector(self):
        print(self.comboBox.currentIndex())
        
    def confirm(self):
        # 원래 창에 값 전달
        self.value = self.comboBox.currentIndex()
        self.close()
        
    def exit(self):
        self.close()