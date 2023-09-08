import sys
import json
import utils
import constant
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
from partSelector import partSelector

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("calculator.ui")[0]

global legIndex
global bodyIndex
global weaponIndex
global accIndex

legIndex = 0
bodyIndex = 0
weaponIndex = 0
accIndex = 0

# JSON 파일 읽기
global legData
with open(constant.FILE_PATH_LEG, "r", encoding = "UTF-8") as file :
    legData = json.load(file)
    
global bodyData
with open(constant.FILE_PATH_BODY, "r", encoding = "UTF-8") as file :
    bodyData = json.load(file)
    
global weaponData
with open(constant.FILE_PATH_WEAPON, "r", encoding = "UTF-8") as file :
    weaponData = json.load(file)
    
global accData
with open(constant.FILE_PATH_ACC, "r", encoding = "UTF-8") as file :
    accData = json.load(file)
    
global subCoreData
with open(constant.FILE_PATH_SUBCORE, "r", encoding = "UTF-8") as file :
    subCoreData = json.load(file)

# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    signal = QtCore.pyqtSignal(list)
    
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
        
        # QComboBox 초기화
        for i in range(len(subCoreData["ID"])):
            self.Leg_Subcore.addItem(subCoreData["Name"][i])
            self.Body_Subcore.addItem(subCoreData["Name"][i])
            self.Weapon_Subcore.addItem(subCoreData["Name"][i])
        
        
    def LegBtnFunction(self) :
        global legIndex
        temp = [ constant.LEG, legIndex ]
        
        self.BtnFunction(temp)
        
        # 두 번째 창에서 값을 전달 받음
        legIndex = self.second.value
        
        self.LegBtn.setText(legData["Name"][legIndex])
        self.Leg_wattBase.setText(str(legData["Watt"][legIndex]))
        self.Leg_healthBase.setText(str(legData["Health"][legIndex]))
        self.Leg_damageBase.setText(str(legData["Damage"][legIndex]))
        
        self.SetLegReinforceValue()
        
    def BodyBtnFunction(self) :
        global bodyIndex
        temp = [ constant.BODY, bodyIndex ]
        
        self.BtnFunction(temp)
        
        # 두 번째 창에서 값을 전달 받음
        bodyIndex = self.second.value
        
        self.BodyBtn.setText(bodyData["Name"][bodyIndex])
        self.Body_wattBase.setText(str(bodyData["Watt"][bodyIndex]))
        self.Body_healthBase.setText(str(bodyData["Health"][bodyIndex]))
        self.Body_damageBase.setText(str(bodyData["Damage"][bodyIndex]))
        
        self.SetBodyReinforceValue()
        
    def WeaponBtnFunction(self) :
        global weaponIndex
        temp = [ constant.WEAPON, weaponIndex ]
        
        self.BtnFunction(temp)
        
        # 두 번째 창에서 값을 전달 받음
        weaponIndex = self.second.value
        
        self.WeaponBtn.setText(weaponData["Name"][weaponIndex])
        self.Weapon_wattBase.setText(str(weaponData["Watt"][weaponIndex]))
        self.Weapon_healthBase.setText(str(weaponData["Health"][weaponIndex]))
        self.Weapon_damageBase.setText(str(weaponData["Damage"][weaponIndex]))
        
        self.SetWeaponReinforceValue()
        
    def AccBtnFunction(self) :
        global accIndex
        temp = [ constant.ACC, accIndex ]
        
        self.BtnFunction(temp)
        
        # 두 번째 창에서 값을 전달 받음
        accIndex = self.second.value
        
        self.AccBtn.setText(accData["Name"][accIndex])
        self.Acc_weight.setText("무게 " + str(accData["Weight"][accIndex]))
        self.Acc_watt.setText("와트 " + str(accData["Watt"][accIndex]))
        self.Acc_health.setText("체력 " + str(accData["Health"][accIndex]))
        self.Acc_damage.setText("공격 " + str(accData["Damage"][accIndex]))
        self.Acc_armor.setText("방어 " + str(accData["Armor"][accIndex]))
        self.Acc_sight.setText("시야 " + str(accData["Sight"][accIndex]))
        self.Acc_range.setText("사거리 " + str(accData["Range"][accIndex]))
        self.Acc_cooldown.setText("연사 " + str(accData["Cooldown"][accIndex]))
        self.Acc_speed.setText("속도 " + str(accData["Speed"][accIndex]))
        
        hb = int(accData["HealthBonus"][accIndex])
        if hb >= 0 :
            self.Acc_healthMagnification.setText("체력 +" + str(hb) + "%")
        else :
            self.Acc_healthMagnification.setText("체력 " + str(hb) + "%")
            
        ab = int(accData["DamageBonus"][accIndex])
        if ab >= 0 :
            self.Acc_damageMagnification.setText("공격 +" + str(ab) + "%")
        else :
            self.Acc_damageMagnification.setText("공격 " + str(ab) + "%")
            
        self.Acc_regen.setText("체력 회복 " + str(accData["Regenerate"][accIndex]) + "%")
        
    @QtCore.pyqtSlot()
    def BtnFunction(self, list) : # Widget 연결
        self.second = partSelector()
        self.signal.connect(self.second.on_signal_from_main) # 시그널 연결
        self.signal.emit(list) # 값 전달
        self.second.exec() # 두 번째 창이 꺼질 때까지 대기
        
    def LegWattReinforce(self) : 
        string = self.Leg_wattReinforce.text()
        self.Leg_wattReinforce.setText(utils.lineEditToNum(string))
        self.SetLegReinforceValue()
        
    def LegHealthReinforce(self) : 
        string = self.Leg_healthReinforce.text()
        self.Leg_healthReinforce.setText(utils.lineEditToNum(string))
        self.SetLegReinforceValue()
        
    def LegDamageReinforce(self) : 
        string = self.Leg_damageReinforce.text()
        self.Leg_damageReinforce.setText(utils.lineEditToNum(string))
        self.SetLegReinforceValue()
        
    def BodyWattReinforce(self) : 
        string = self.Body_wattReinforce.text()
        self.Body_wattReinforce.setText(utils.lineEditToNum(string))
        self.SetBodyReinforceValue()
        
    def BodyHealthReinforce(self) : 
        string = self.Body_healthReinforce.text()
        self.Body_healthReinforce.setText(utils.lineEditToNum(string))
        self.SetBodyReinforceValue()
        
    def BodyDamageReinforce(self) : 
        string = self.Body_damageReinforce.text()
        self.Body_damageReinforce.setText(utils.lineEditToNum(string))
        self.SetBodyReinforceValue()
        
    def WeaponWattReinforce(self) : 
        string = self.Weapon_wattReinforce.text()
        self.Weapon_wattReinforce.setText(utils.lineEditToNum(string))
        self.SetWeaponReinforceValue()
        
    def WeaponHealthReinforce(self) : 
        string = self.Weapon_healthReinforce.text()
        self.Weapon_healthReinforce.setText(utils.lineEditToNum(string))
        self.SetWeaponReinforceValue()
        
    def WeaponDamageReinforce(self) : 
        string = self.Weapon_damageReinforce.text()
        self.Weapon_damageReinforce.setText(utils.lineEditToNum(string))
        self.SetWeaponReinforceValue()
        
    def SetLegReinforceValue(self) :
        self.Leg_wattAdd.setText(
            str(utils.getWattReinforce(legData["Watt"][legIndex], int(self.Leg_wattReinforce.text()))) 
            + " / " + str(utils.getWattBase(legData["Watt"][legIndex]))
        )
        self.Leg_healthAdd.setText(
            str(utils.getHealthReinforce(legData["Watt"][legIndex], int(self.Leg_healthReinforce.text()), False)) 
            + " / " + str(utils.getHealthBase(legData["Watt"][legIndex], False))
        )
        self.Leg_damageAdd.setText(
            str(utils.getDamageReinforce(legData["Watt"][legIndex], int(self.Leg_damageReinforce.text()), False))
            + " / " + str(utils.getDamageBase(legData["Watt"][legIndex], False))
        )
    
    def SetBodyReinforceValue(self) :
        self.Body_wattAdd.setText(
            str(utils.getWattReinforce(bodyData["Watt"][bodyIndex], int(self.Body_wattReinforce.text()))) 
            + " / " + str(utils.getWattBase(bodyData["Watt"][bodyIndex]))
        )
        self.Body_healthAdd.setText(
            str(utils.getHealthReinforce(bodyData["Health"][bodyIndex], int(self.Body_healthReinforce.text()), True)) 
            + " / " + str(utils.getHealthBase(bodyData["Health"][bodyIndex], True))
        )
        self.Body_damageAdd.setText(
            str(utils.getDamageReinforce(bodyData["Watt"][bodyIndex], int(self.Body_damageReinforce.text()), False))
            + " / " + str(utils.getDamageBase(bodyData["Watt"][bodyIndex], False))
        )
        
    def SetWeaponReinforceValue(self) :
        self.Weapon_wattAdd.setText(
            str(utils.getWattReinforce(weaponData["Watt"][weaponIndex], int(self.Weapon_wattReinforce.text()))) 
            + " / " + str(utils.getWattBase(weaponData["Watt"][weaponIndex]))
        )
        self.Weapon_healthAdd.setText(
            str(utils.getHealthReinforce(weaponData["Watt"][weaponIndex], int(self.Weapon_healthReinforce.text()), False)) 
            + " / " + str(utils.getHealthBase(weaponData["Watt"][weaponIndex], True))
        )
        self.Weapon_damageAdd.setText(
            str(utils.getDamageReinforce(weaponData["Damage"][weaponIndex], int(self.Weapon_damageReinforce.text()), True))
            + " / " + str(utils.getDamageBase(weaponData["Damage"][weaponIndex], True))
        )
        
    def LegSubcoreSelect(self) :
        self.Leg_SubcoreLabel.setText(
            subCoreData["Special"][self.Leg_Subcore.currentIndex()])
        
    def BodySubcoreSelect(self) :
        self.Body_SubcoreLabel.setText(
            subCoreData["Special"][self.Body_Subcore.currentIndex()])
        
    def WeaponSubcoreSelect(self) :
        if self.Weapon_Subcore.currentIndex() == constant.SAGITTARIUS :
            self.Weapon_SubcoreLabel.setText(
                subCoreData["Sagittarius"])
        else : 
            self.Weapon_SubcoreLabel.setText(
                subCoreData["Special"][self.Weapon_Subcore.currentIndex()])

if __name__ == "__main__" :
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()