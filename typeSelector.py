import os
import sys
import json
import constant
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore

###############################################################
# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
def resource_path(relativePath):
    # Get absolute path to resource, works for dev and for PyInstaller
    basePath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(basePath, relativePath)

form = resource_path("typeSelector.ui")
form_typeSelector = uic.loadUiType(form)[0]
###############################################################

global data

class typeSelector(QDialog, QWidget, form_typeSelector):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        # 초기화
        self.value = 0
        
        # QPushButton 기능 연결
        self.select.clicked.connect(self.confirm)
        self.cancel.clicked.connect(self.exit)
        
        # 두 번째 창 실행
        self.show()
        
    # 메인 창으로부터 메시지 수신
    @QtCore.pyqtSlot(list)
    def on_signal_from_main(self, value):
        global data
        
        # 왜 파이썬에는 switch문이 없지? (진짜 모름)
        if value[0] == constant.BODY :
            with open(constant.FILE_PATH_BODY, "r", encoding = "UTF-8") as file :
                data = json.load(file)
                
        elif value[0] == constant.WEAPON :
            with open(constant.FILE_PATH_WEAPON, "r", encoding = "UTF-8") as file :
                data = json.load(file)
                
        self.comboBox_Type.clear()
        self.comboBox_Parts.clear()
        
        self.comboBox_Type.addItem("없음")
        self.comboBox_Type.addItem("탑형")
        self.comboBox_Type.addItem("팔형")
        self.comboBox_Type.addItem("어깨형")
        
        self.comboBox_Type.setCurrentIndex(data[value[1]]["Type"])
        
        for i in range(len(data)):
            if data[i]["Type"] == self.comboBox_Type.currentIndex():
                self.comboBox_Parts.addItem(data[i]["Name"])
        
        for i in range(self.comboBox_Parts.count()):
            if data[value[1]]["Name"] == self.comboBox_Parts.itemText(i):
                self.comboBox_Parts.setCurrentIndex(i)
                
        # QComboBox 기능 연결
        self.comboBox_Type.currentIndexChanged.connect(self.onChangeType)
    
    def onChangeType(self):
        self.comboBox_Parts.clear()
        
        global data
        
        for i in range(len(data)):
            if data[i]["Type"] == self.comboBox_Type.currentIndex():
                self.comboBox_Parts.addItem(data[i]["Name"])
    
    def confirm(self):
        value = 0
        
        for i in range(len(data)):
            if data[i]["Name"] == self.comboBox_Parts.currentText():
                value = i
    
        # 원래 창에 값 전달
        self.value = value
        self.close()
        
    def exit(self):
        self.close()