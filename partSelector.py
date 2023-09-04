import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_partSelector = uic.loadUiType("partSelector.ui")[0]

class partSelector(QDialog, QWidget, form_partSelector):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        # QComboBox 기능 연결
        self.comboBox.currentIndexChanged.connect(self.selector)
        
        # QPushButton 기능 연결
        self.select.clicked.connect(self.confirm)
        self.cancel.clicked.connect(self.exit)
        
        # 두 번째 창 실행
        self.show()
        
    def selector(self):
        print(self.comboBox.currentIndex())
        
    def confirm(self):
        self.close()
        
    def exit(self):
        self.close()