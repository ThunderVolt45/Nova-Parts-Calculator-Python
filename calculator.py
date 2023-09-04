import sys
import utils
from PyQt5.QtWidgets import *
from PyQt5 import uic
from partSelector import partSelector

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("calculator.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        # QPushButton 기능 연결
        self.LegBtn.clicked.connect(self.LegBtnFunction)
        self.BodyBtn.clicked.connect(self.BodyBtnFunction)
        self.WeaponBtn.clicked.connect(self.WeaponBtnFunction)
        self.AccBtn.clicked.connect(self.AccBtnFunction)
        
        # QLineEdit 기능 연결
        self.Leg_wattReinforce.textChanged.connect(self.LegWattReinforce)
        self.Leg_healthReinforce.textChanged.connect(self.LegHealthReinforce)
        self.Leg_damageReinforce.textChanged.connect(self.LegDamageReinforce)
        self.Body_wattReinforce.textChanged.connect(self.BodyWattReinforce)
        self.Body_healthReinforce.textChanged.connect(self.BodyHealthReinforce)
        self.Body_damageReinforce.textChanged.connect(self.BodyDamageReinforce)
        self.Weapon_wattReinforce.textChanged.connect(self.WeaponWattReinforce)
        self.Weapon_healthReinforce.textChanged.connect(self.WeaponHealthReinforce)
        self.Weapon_damageReinforce.textChanged.connect(self.WeaponDamageReinforce)
        
        # QComboBox 기능 연결
        self.Leg_Subcore.currentIndexChanged.connect(self.LegSubcoreSelect)
        self.Body_Subcore.currentIndexChanged.connect(self.BodySubcoreSelect)
        self.Weapon_Subcore.currentIndexChanged.connect(self.WeaponSubcoreSelect)
        
    def LegBtnFunction(self) :
        self.second = partSelector()
        self.second.exec() # 두 번째 창이 꺼질 때까지 대기
        print("Leg Btn")
        
    def BodyBtnFunction(self) :
        self.second = partSelector()
        self.second.exec() # 두 번째 창이 꺼질 때까지 대기
        print("Body Btn")
        
    def WeaponBtnFunction(self) :
        self.second = partSelector()
        self.second.exec() # 두 번째 창이 꺼질 때까지 대기
        print("Weapon Btn")
        
    def AccBtnFunction(self) :
        self.second = partSelector()
        self.second.exec() # 두 번째 창이 꺼질 때까지 대기
        print("Acc Btn")
        
    def LegWattReinforce(self) : 
        string = self.Leg_wattReinforce.text()
        self.Leg_wattReinforce.setText(utils.lineEditToNum(string))
        
    def LegHealthReinforce(self) : 
        string = self.Leg_healthReinforce.text()
        self.Leg_healthReinforce.setText(utils.lineEditToNum(string))
        
    def LegDamageReinforce(self) : 
        string = self.Leg_damageReinforce.text()
        self.Leg_damageReinforce.setText(utils.lineEditToNum(string))
        
    def BodyWattReinforce(self) : 
        string = self.Body_wattReinforce.text()
        self.Body_wattReinforce.setText(utils.lineEditToNum(string))
        
    def BodyHealthReinforce(self) : 
        string = self.Body_healthReinforce.text()
        self.Body_healthReinforce.setText(utils.lineEditToNum(string))
        
    def BodyDamageReinforce(self) : 
        string = self.Body_damageReinforce.text()
        self.Body_damageReinforce.setText(utils.lineEditToNum(string))
        
    def WeaponWattReinforce(self) : 
        string = self.Weapon_wattReinforce.text()
        self.Weapon_wattReinforce.setText(utils.lineEditToNum(string))
        
    def WeaponHealthReinforce(self) : 
        string = self.Weapon_healthReinforce.text()
        self.Weapon_healthReinforce.setText(utils.lineEditToNum(string))
        
    def WeaponDamageReinforce(self) : 
        string = self.Weapon_damageReinforce.text()
        self.Weapon_damageReinforce.setText(utils.lineEditToNum(string))
        
    def LegSubcoreSelect(self) :
        print(self.Leg_Subcore.currentIndex())
        
    def BodySubcoreSelect(self) :
        print(self.Body_Subcore.currentIndex())
        
    def WeaponSubcoreSelect(self) :
        print(self.Weapon_Subcore.currentIndex())

if __name__ == "__main__" :
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()