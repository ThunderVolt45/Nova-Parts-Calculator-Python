import os
import sys
import json
import utils
import constant
import assemble
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
from partSelector import partSelector

###############################################################
# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
def resource_path(relativePath):
    # Get absolute path to resource, works for dev and for PyInstaller
    basePath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(basePath, relativePath)

form = resource_path("calculator.ui")
form_class = uic.loadUiType(form)[0]
###############################################################

global legIndex
global bodyIndex
global weaponIndex
global accIndex
global calculateAsFloat

legIndex = 0
bodyIndex = 0
weaponIndex = 0
accIndex = 0
calculateAsFloat = False

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
        self.Assemble_btn.clicked.connect(self.Assemble)
        
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
            
        # QAction 기능 연결
        self.actionFloat.triggered.connect(self.CalculateAsFloat)
        
        
    def LegBtnFunction(self) :
        global legIndex
        temp = [ constant.LEG, legIndex ]
        
        self.BtnFunction(temp)
        
        # 두 번째 창에서 값을 전달 받음
        legIndex = self.second.value
        
        self.LegBtn.setText(legData[legIndex]["Name"])
        self.Leg_wattBase.setText(str(legData[legIndex]["Watt"]))
        self.Leg_healthBase.setText(str(legData[legIndex]["Health"]))
        self.Leg_damageBase.setText(str(legData[legIndex]["Damage"]))
        
        self.Leg_weight.setText("하중 " + str(legData[legIndex]["Weight"]))
        self.Leg_speed.setText("속도 " + str(legData[legIndex]["Speed"]))
        self.Leg_armor.setText("방어 " + str(legData[legIndex]["Armor"]))
        self.Leg_splash.setText("스플 감소 " + str(-legData[legIndex]["SplashReduce"]) + "%")
        self.Leg_regen.setText("체력 회복 " + str(legData[legIndex]["Regenerate"]) + "%")
        self.Leg_sight.setText("시야 " + str(legData[legIndex]["Sight"]))
        self.Leg_range.setText("사거리 " + str(legData[legIndex]["Range"]))
        self.Leg_cooldown.setText("연사 " + str(legData[legIndex]["Cooldown"]))
        
        hb = int(legData[legIndex]["HealthBonus"])
        if hb >= 0 :  
            self.Leg_healthMagnification.setText("체력 +" + str(legData[legIndex]["HealthBonus"]) + "%")
        else :
            self.Leg_healthMagnification.setText("체력 " + str(legData[legIndex]["HealthBonus"]) + "%")
            
        db = int(legData[legIndex]["DamageBonus"])
        if db >= 0 :  
            self.Leg_damageMagnification.setText("공격 +" + str(legData[legIndex]["DamageBonus"]) + "%")
        else :
            self.Leg_damageMagnification.setText("공격 " + str(legData[legIndex]["DamageBonus"]) + "%")
        
        self.SetLegReinforceValue()
        
    def BodyBtnFunction(self) :
        global bodyIndex
        temp = [ constant.BODY, bodyIndex ]
        
        self.BtnFunction(temp)
        
        # 두 번째 창에서 값을 전달 받음
        bodyIndex = self.second.value
        
        self.BodyBtn.setText(bodyData[bodyIndex]["Name"])
        self.Body_wattBase.setText(str(bodyData[bodyIndex]["Watt"]))
        self.Body_healthBase.setText(str(bodyData[bodyIndex]["Health"]))
        self.Body_damageBase.setText(str(bodyData[bodyIndex]["Damage"]))
        
        self.Body_weight.setText("무게 " + str(bodyData[bodyIndex]["Weight"]))
        self.Body_speed.setText("속도 " + str(bodyData[bodyIndex]["Speed"]))
        self.Body_armor.setText("방어 " + str(bodyData[bodyIndex]["Armor"]))
        self.Body_sight.setText("시야 " + str(bodyData[bodyIndex]["Sight"]))
        self.Body_regen.setText("체력 회복 " + str(bodyData[bodyIndex]["Regenerate"]) + "%")
        self.Body_range.setText("사거리 " + str(bodyData[bodyIndex]["Range"]))
        self.Body_cooldown.setText("연사 " + str(bodyData[bodyIndex]["Cooldown"]))
        
        hb = int(bodyData[bodyIndex]["HealthBonus"])
        if hb >= 0 :  
            self.Body_healthMagnification.setText("체력 +" + str(bodyData[bodyIndex]["HealthBonus"]) + "%")
        else :
            self.Body_healthMagnification.setText("체력 " + str(bodyData[bodyIndex]["HealthBonus"]) + "%")
            
        db = int(bodyData[bodyIndex]["DamageBonus"])
        if db >= 0 :  
            self.Body_damageMagnification.setText("공격 +" + str(bodyData[bodyIndex]["DamageBonus"]) + "%")
        else :
            self.Body_damageMagnification.setText("공격 " + str(bodyData[bodyIndex]["DamageBonus"]) + "%")
        
        self.SetBodyReinforceValue()
        
    def WeaponBtnFunction(self) :
        global weaponIndex
        temp = [ constant.WEAPON, weaponIndex ]
        
        self.BtnFunction(temp)
        
        # 두 번째 창에서 값을 전달 받음
        weaponIndex = self.second.value
        
        self.WeaponBtn.setText(weaponData[weaponIndex]["Name"])
        self.Weapon_wattBase.setText(str(weaponData[weaponIndex]["Watt"]))
        self.Weapon_healthBase.setText(str(weaponData[weaponIndex]["Health"]))
        self.Weapon_damageBase.setText(str(weaponData[weaponIndex]["Damage"]))
        
        self.Weapon_weight.setText("무게 " + str(weaponData[weaponIndex]["Weight"]))
        self.Weapon_speed.setText("속도 " + str(weaponData[weaponIndex]["Speed"]))
        self.Weapon_armor.setText("방어 " + str(weaponData[weaponIndex]["Armor"]))
        self.Weapon_regen.setText("체력 회복 " + str(weaponData[weaponIndex]["Regenerate"]) + "%")
        self.Weapon_dph.setText("DPH " + str(weaponData[weaponIndex]["DamagePerHealth"]) + "%")
        self.Weapon_sight.setText("시야 " + str(weaponData[weaponIndex]["Sight"]))
        self.Weapon_cooldown.setText("연사 " + str(weaponData[weaponIndex]["Cooldown"]))
        self.Weapon_splash.setText("범위 " + str(weaponData[weaponIndex]["Splash"]))
        
        rm = int(weaponData[weaponIndex]["RangeMinimum"])
        if rm != 0 :
            self.Weapon_range.setText("사거리 " + str(weaponData[weaponIndex]["RangeMinimum"]) + " - "+ str(weaponData[weaponIndex]["Range"]))
        else :
            self.Weapon_range.setText("사거리 " + str(weaponData[weaponIndex]["Range"]))
        
        hb = int(weaponData[weaponIndex]["HealthBonus"])
        if hb >= 0 :
            self.Weapon_healthMagnification.setText("체력 +" + str(weaponData[weaponIndex]["HealthBonus"]) + "%")
        else :
            self.Weapon_healthMagnification.setText("체력 " + str(weaponData[weaponIndex]["HealthBonus"]) + "%")
            
        db = int(weaponData[weaponIndex]["DamageBonus"])
        if db >= 0 :
            self.Weapon_damageMagnification.setText("공격 +" + str(weaponData[weaponIndex]["DamageBonus"]) + "%")
        else :
            self.Weapon_damageMagnification.setText("공격 " + str(weaponData[weaponIndex]["DamageBonus"]) + "%")
            
        if weaponData[weaponIndex]["CanAttackGround"] and weaponData[weaponIndex]["CanAttackAir"] :
            self.Weapon_attack.setText("지상 && 공중")
        elif weaponData[weaponIndex]["CanAttackGround"] :
            self.Weapon_attack.setText("지상")
        elif weaponData[weaponIndex]["CanAttackAir"] :
            self.Weapon_attack.setText("공중")
        else :
            self.Weapon_attack.setText("공격 능력 없음")
        
        self.SetWeaponReinforceValue()
        
    def AccBtnFunction(self) :
        global accIndex
        temp = [ constant.ACC, accIndex ]
        
        self.BtnFunction(temp)
        
        # 두 번째 창에서 값을 전달 받음
        accIndex = self.second.value
        
        self.AccBtn.setText(accData[accIndex]["Name"])
        self.Acc_weight.setText("무게 " + str(accData[accIndex]["Weight"]))
        self.Acc_watt.setText("와트 " + str(accData[accIndex]["Watt"]))
        self.Acc_health.setText("체력 " + str(accData[accIndex]["Health"]))
        self.Acc_damage.setText("공격 " + str(accData[accIndex]["Damage"]))
        self.Acc_armor.setText("방어 " + str(accData[accIndex]["Armor"]))
        self.Acc_sight.setText("시야 " + str(accData[accIndex]["Sight"]))
        self.Acc_range.setText("사거리 " + str(accData[accIndex]["Range"]))
        self.Acc_cooldown.setText("연사 " + str(accData[accIndex]["Cooldown"]))
        self.Acc_speed.setText("속도 " + str(accData[accIndex]["Speed"]))
        
        hb = int(accData[accIndex]["HealthBonus"])
        if hb >= 0 :
            self.Acc_healthMagnification.setText("체력 +" + str(hb) + "%")
        else :
            self.Acc_healthMagnification.setText("체력 " + str(hb) + "%")
            
        ab = int(accData[accIndex]["DamageBonus"])
        if ab >= 0 :
            self.Acc_damageMagnification.setText("공격 +" + str(ab) + "%")
        else :
            self.Acc_damageMagnification.setText("공격 " + str(ab) + "%")
            
        self.Acc_regen.setText("체력 회복 " + str(accData[accIndex]["Regenerate"]) + "%")
        
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
        wattBase = utils.getWattBase(legData[legIndex]["Watt"])
        healthBase = utils.getHealthBase(legData[legIndex]["Watt"], False)
        damageBase = utils.getDamageBase(legData[legIndex]["Watt"], False)
        
        if not calculateAsFloat :
            wattBase = int(wattBase)
            healthBase = int(healthBase)
            damageBase = int(damageBase)
            
        self.Leg_wattAdd.setText(
            str(utils.getWattReinforce(legData[legIndex]["Watt"], int(self.Leg_wattReinforce.text()), calculateAsFloat)) 
            + " / " + str(wattBase))
        self.Leg_healthAdd.setText(
            str(utils.getHealthReinforce(legData[legIndex]["Watt"], int(self.Leg_healthReinforce.text()), False, calculateAsFloat)) 
            + " / " + str(healthBase))
        self.Leg_damageAdd.setText(
            str(utils.getDamageReinforce(legData[legIndex]["Watt"], int(self.Leg_damageReinforce.text()), False, calculateAsFloat))
            + " / " + str(damageBase))
    
    def SetBodyReinforceValue(self) :
        wattBase = utils.getWattBase(bodyData[bodyIndex]["Watt"])
        healthBase = utils.getHealthBase(bodyData[bodyIndex]["Health"], True)
        damageBase = utils.getDamageBase(bodyData[bodyIndex]["Watt"], False)
        
        if not calculateAsFloat :
            wattBase = int(wattBase)
            healthBase = int(healthBase)
            damageBase = int(damageBase)
        
        self.Body_wattAdd.setText(
            str(utils.getWattReinforce(bodyData[bodyIndex]["Watt"], int(self.Body_wattReinforce.text()), calculateAsFloat)) 
            + " / " + str(wattBase))
        self.Body_healthAdd.setText(
            str(utils.getHealthReinforce(bodyData[bodyIndex]["Health"], int(self.Body_healthReinforce.text()), True, calculateAsFloat)) 
            + " / " + str(healthBase))
        self.Body_damageAdd.setText(
            str(utils.getDamageReinforce(bodyData[bodyIndex]["Watt"], int(self.Body_damageReinforce.text()), False, calculateAsFloat))
            + " / " + str(damageBase))
        
    def SetWeaponReinforceValue(self) :
        wattBase = utils.getWattBase(weaponData[weaponIndex]["Watt"])
        healthBase = utils.getHealthBase(weaponData[weaponIndex]["Watt"], False)
        damageBase = utils.getDamageBase(weaponData[weaponIndex]["Damage"], True)
        
        if not calculateAsFloat :
            wattBase = int(wattBase)
            healthBase = int(healthBase)
            damageBase = int(damageBase)
        
        self.Weapon_wattAdd.setText(
            str(utils.getWattReinforce(weaponData[weaponIndex]["Watt"], int(self.Weapon_wattReinforce.text()), calculateAsFloat)) 
            + " / " + str(wattBase))
        self.Weapon_healthAdd.setText(
            str(utils.getHealthReinforce(weaponData[weaponIndex]["Watt"], int(self.Weapon_healthReinforce.text()), False, calculateAsFloat)) 
            + " / " + str(healthBase))
        self.Weapon_damageAdd.setText(
            str(utils.getDamageReinforce(weaponData[weaponIndex]["Damage"], int(self.Weapon_damageReinforce.text()), True, calculateAsFloat))
            + " / " + str(damageBase))
        
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
            
    def Assemble(self) :
        partsIndex = (legIndex, bodyIndex, weaponIndex, accIndex)
        subIndex = (self.Leg_Subcore.currentIndex(), self.Body_Subcore.currentIndex(), self.Weapon_Subcore.currentIndex())
        
        # 하중 계산
        weight = assemble.GetWeight(partsIndex)
        load = legData[legIndex]["Weight"]
        self.Assemble_weight.setText(str(weight) + " / " + str(load))
        
        # 와트 계산
        wattReinforce = (int(self.Leg_wattReinforce.text()), int(self.Body_wattReinforce.text()), int(self.Weapon_wattReinforce.text()))
        self.Assemble_watt.setText(str(assemble.GetWatt(partsIndex, subIndex, wattReinforce, self.actionFloat.isChecked())))
        
        # 체력 계산
        healthReinforce = (int(self.Leg_healthReinforce.text()), int(self.Body_healthReinforce.text()), int(self.Weapon_healthReinforce.text()))
        self.Assemble_health.setText(str(assemble.GetHealth(partsIndex, subIndex, healthReinforce, self.actionFloat.isChecked())))
        
        # 리젠 계산
        self.Assemble_regen.setText(str(int(assemble.GetRegenerate(partsIndex, subIndex))) + "%")
        
        # 속도 계산
        self.Assemble_speed.setText(str(int(assemble.GetSpeed(partsIndex, subIndex))))
        
        # 연사 계산
        self.Assemble_cooldown.setText(str(int(assemble.GetCooldown(partsIndex, subIndex))))
        
        # 사거리 계산
        range = assemble.GetRange(partsIndex, subIndex)
        
        if weaponData[weaponIndex]["RangeMinimum"] != 0 :
            self.Assemble_range.setText(str(weaponData[weaponIndex]["RangeMinimum"]) + " - " + str(int(range)))
        else :
            self.Assemble_range.setText(str(int(range)))
            
        # 범위 계산
        splash = assemble.GetSplash(partsIndex, subIndex)
        
        if weaponData[weaponIndex]["Splash"] == 0 :
            self.Assemble_splash.setText("없음")
        else :
            self.Assemble_splash.setText(str(int(splash)))
            
        # 시야 계산
        self.Assemble_sight.setText(str(int(assemble.GetSight(partsIndex, subIndex))))
        
        # 공격 계산
        damageReinforce = (int(self.Leg_damageReinforce.text()), int(self.Body_damageReinforce.text()), int(self.Weapon_damageReinforce.text()))
        
        if not weaponData[weaponIndex]["CanAttackGround"] and not weaponData[weaponIndex]["CanAttackAir"] :
            self.Assemble_damage.setText("없음")
        else :
            self.Assemble_damage.setText(str(assemble.GetDamage(partsIndex, subIndex, damageReinforce, self.actionFloat.isChecked())))
        
        # 체력 비례 데미지 계산
        dph = assemble.GetDamagePerHealth(partsIndex, subIndex)
        
        if dph != 0 :
            self.Assemble_dph.setText(str(int(dph)) + "%")
        else :
            self.Assemble_dph.setText("없음")
            
        # 방어 무시 계산
        self.Assemble_pierce.setText(str(int(assemble.GetPierce(partsIndex, subIndex))))
        
        # 방어 계산
        self.Assemble_armor.setText(str(int(assemble.GetArmor(partsIndex, subIndex))))
        
        # 기타 특수 능력 정보 표시
        string = ""
        
        if legData[legIndex]["Special"] :
            string += legData[legIndex]["Special"] + "\n"
            
        if bodyData[bodyIndex]["Special"] :
            string += bodyData[bodyIndex]["Special"] + "\n"
            
        if weaponData[weaponIndex]["Special"] :
            string += weaponData[weaponIndex]["Special"] + "\n"
            
        if accData[accIndex]["Special"] :
            string += accData[accIndex]["Special"] + "\n"
        
        self.Assemble_etc.setPlainText(string)
        
        # 조립 유효성 검사
        self.AssembleValidate(weight, load)
        
    def AssembleValidate(self, weight: int, load: int) :
        # styleSheet 초기화
        self.LegBtn.setStyleSheet("")
        self.BodyBtn.setStyleSheet("")
        self.WeaponBtn.setStyleSheet("")
        self.AccBtn.setStyleSheet("")
        self.Assemble_weight.setStyleSheet("")
        
        # 부품 없음
        if legIndex == 0 :
            self.LegBtn.setStyleSheet("QPushButton"
                                      "{"
                                      "border : 2px solid red;"
                                      "background : white;"
                                      "color : red"
                                      "}")
        
        if bodyIndex == 0 :
            self.BodyBtn.setStyleSheet("QPushButton"
                                       "{"
                                       "border : 2px solid red;"
                                       "background : white;"
                                       "color : red"
                                       "}")
            
        if weaponIndex == 0 :
            self.WeaponBtn.setStyleSheet("QPushButton"
                                       "{"
                                       "border : 2px solid red;"
                                       "background : white;"
                                       "color : red"
                                       "}")
        
        # 형태 불일치
        if bodyIndex != 0 and weaponIndex != 0 and bodyData[bodyIndex]["Type"] != weaponData[weaponIndex]["Type"] :
            self.BodyBtn.setStyleSheet("QPushButton"
                                       "{"
                                       "border : 2px solid red;"
                                       "background : white;"
                                       "color : red"
                                       "}")
            self.WeaponBtn.setStyleSheet("QPushButton"
                                       "{"
                                       "border : 2px solid red;"
                                       "background : white;"
                                       "color : red"
                                       "}")
        
        # 하중 초과
        if weight > load :
            self.LegBtn.setStyleSheet("QPushButton"
                                          "{"
                                          "border : 2px solid red;"
                                          "background : white;"
                                          "color : red"
                                          "}")
            self.Assemble_weight.setStyleSheet("QLineEdit"
                                               "{"
                                               "border : 2px solid rgb(255, 0, 0);"
                                               "color : rgb(255, 0, 0)"
                                               "}")
        
        # N템 개수 초과
        if legData[legIndex]["N"] + bodyData[bodyIndex]["N"] + weaponData[weaponIndex]["N"] > 1 :
            if legData[legIndex]["N"] :
                self.LegBtn.setStyleSheet("QPushButton"
                                          "{"
                                          "border : 2px solid red;"
                                          "background : white;"
                                          "color : red"
                                          "}")
            if bodyData[bodyIndex]["N"] :
                self.BodyBtn.setStyleSheet("QPushButton"
                                          "{"
                                          "border : 2px solid red;"
                                          "background : white;"
                                          "color : red"
                                          "}")
            if weaponData[weaponIndex]["N"] :
                self.WeaponBtn.setStyleSheet("QPushButton"
                                          "{"
                                          "border : 2px solid red;"
                                          "background : white;"
                                          "color : red"
                                          "}")
                
        # 아포칼립스
        if weaponIndex == 60 :
            if bodyData[bodyIndex]["Weight"] < 30 :
                self.BodyBtn.setStyleSheet("QPushButton"
                                          "{"
                                          "border : 2px solid red;"
                                          "background : white;"
                                          "color : red"
                                          "}")
            if "타워링" in accData[accIndex]["Name"] :
                self.AccBtn.setStyleSheet("QPushButton"
                                          "{"
                                          "border : 2px solid red;"
                                          "background : white;"
                                          "color : red"
                                          "}")
        
        # 부품 없음
        if legIndex == 0 or bodyIndex == 0 or weaponIndex == 0 :
            self.Assemble_label.setText("부품 없음")
        
        # 형태 불일치
        elif bodyData[bodyIndex]["Type"] != weaponData[weaponIndex]["Type"] :
            self.Assemble_label.setText("형태 불일치")
            
        # 하중 초과
        elif weight > load :
            self.Assemble_label.setText("하중 초과")
            
        # N템 개수 초과
        elif legData[legIndex]["N"] + bodyData[bodyIndex]["N"] + weaponData[weaponIndex]["N"] > 1 :
            self.Assemble_label.setText("N템 개수 초과")
            
        # 아포칼립스
        elif weaponIndex == 60 and bodyData[bodyIndex]["Weight"] < 30 :
            self.Assemble_label.setText("무게 30 이상 몸통 필요")
        elif weaponIndex == 60 and "타워링" in accData[accIndex]["Name"] :
            self.Assemble_label.setText("타워링과 조립 불가")
        
        # 조립 완료
        else :
            self.LegBtn.setStyleSheet("")
            self.BodyBtn.setStyleSheet("")
            self.WeaponBtn.setStyleSheet("")
            self.AccBtn.setStyleSheet("")
            self.Assemble_weight.setStyleSheet("")
            self.Assemble_label.setText("조립 완료")
            
    def CalculateAsFloat(self) :
        global calculateAsFloat
        calculateAsFloat = self.actionFloat.isChecked()
        self.SetLegReinforceValue()
        self.SetBodyReinforceValue()
        self.SetWeaponReinforceValue()
        
        
        

if __name__ == "__main__" :
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()