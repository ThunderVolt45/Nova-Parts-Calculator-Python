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
        
        self.Leg_weight.setText("하중 " + str(legData["Weight"][legIndex]))
        self.Leg_speed.setText("속도 " + str(legData["Speed"][legIndex]))
        self.Leg_armor.setText("방어 " + str(legData["Armor"][legIndex]))
        self.Leg_splash.setText("스플 감소 " + str(-legData["SplashReduce"][legIndex]) + "%")
        self.Leg_regen.setText("체력 회복 " + str(legData["Regenerate"][legIndex]) + "%")
        self.Leg_sight.setText("시야 " + str(legData["Sight"][legIndex]))
        self.Leg_range.setText("사거리 " + str(legData["Range"][legIndex]))
        self.Leg_cooldown.setText("연사 " + str(legData["Cooldown"][legIndex]))
        
        hb = int(legData["HealthBonus"][legIndex])
        if hb >= 0 :  
            self.Leg_healthMagnification.setText("체력 +" + str(legData["HealthBonus"][legIndex]) + "%")
        else :
            self.Leg_healthMagnification.setText("체력 " + str(legData["HealthBonus"][legIndex]) + "%")
            
        db = int(legData["DamageBonus"][legIndex])
        if db >= 0 :  
            self.Leg_damageMagnification.setText("공격 +" + str(legData["DamageBonus"][legIndex]) + "%")
        else :
            self.Leg_damageMagnification.setText("공격 " + str(legData["DamageBonus"][legIndex]) + "%")
        
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
        
        self.Body_weight.setText("무게 " + str(bodyData["Weight"][bodyIndex]))
        self.Body_speed.setText("속도 " + str(bodyData["Speed"][bodyIndex]))
        self.Body_armor.setText("방어 " + str(bodyData["Armor"][bodyIndex]))
        self.Body_sight.setText("시야 " + str(bodyData["Sight"][bodyIndex]))
        self.Body_regen.setText("체력 회복 " + str(bodyData["Regenerate"][bodyIndex]) + "%")
        self.Body_range.setText("사거리 " + str(bodyData["Range"][bodyIndex]))
        self.Body_cooldown.setText("연사 " + str(bodyData["Cooldown"][bodyIndex]))
        
        hb = int(bodyData["HealthBonus"][bodyIndex])
        if hb >= 0 :  
            self.Body_healthMagnification.setText("체력 +" + str(bodyData["HealthBonus"][bodyIndex]) + "%")
        else :
            self.Body_healthMagnification.setText("체력 " + str(bodyData["HealthBonus"][bodyIndex]) + "%")
            
        db = int(bodyData["DamageBonus"][bodyIndex])
        if db >= 0 :  
            self.Body_damageMagnification.setText("공격 +" + str(bodyData["DamageBonus"][bodyIndex]) + "%")
        else :
            self.Body_damageMagnification.setText("공격 " + str(bodyData["DamageBonus"][bodyIndex]) + "%")
        
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
        
        self.Weapon_weight.setText("무게 " + str(weaponData["Weight"][weaponIndex]))
        self.Weapon_speed.setText("속도 " + str(weaponData["Speed"][weaponIndex]))
        self.Weapon_armor.setText("방어 " + str(weaponData["Armor"][weaponIndex]))
        self.Weapon_regen.setText("체력 회복 " + str(weaponData["Regenerate"][weaponIndex]) + "%")
        self.Weapon_dph.setText("DPH " + str(weaponData["DamagePerHealth"][weaponIndex]) + "%")
        self.Weapon_sight.setText("시야 " + str(weaponData["Sight"][weaponIndex]))
        self.Weapon_cooldown.setText("연사 " + str(weaponData["Cooldown"][weaponIndex]))
        self.Weapon_splash.setText("범위 " + str(weaponData["Splash"][weaponIndex]))
        
        rm = int(weaponData["RangeMinimum"][weaponIndex])
        if rm != 0 :
            self.Weapon_range.setText("사거리 " + str(weaponData["RangeMinimum"][weaponIndex]) + " - "+ str(weaponData["Range"][weaponIndex]))
        else :
            self.Weapon_range.setText("사거리 " + str(weaponData["Range"][weaponIndex]))
        
        hb = int(weaponData["HealthBonus"][weaponIndex])
        if hb >= 0 :
            self.Weapon_healthMagnification.setText("체력 +" + str(weaponData["HealthBonus"][weaponIndex]) + "%")
        else :
            self.Weapon_healthMagnification.setText("체력 " + str(weaponData["HealthBonus"][weaponIndex]) + "%")
            
        db = int(weaponData["DamageBonus"][weaponIndex])
        if db >= 0 :
            self.Weapon_damageMagnification.setText("공격 +" + str(weaponData["DamageBonus"][weaponIndex]) + "%")
        else :
            self.Weapon_damageMagnification.setText("공격 " + str(weaponData["DamageBonus"][weaponIndex]) + "%")
        
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
            + " / " + str(utils.getHealthBase(weaponData["Watt"][weaponIndex], False))
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
            
    def Assemble(self) :
        # 하중 계산
        weight = 0
        load = legData["Weight"][legIndex]
        
        weight += bodyData["Weight"][bodyIndex]
        weight += weaponData["Weight"][weaponIndex]
        weight += accData["Weight"][accIndex]
        
        self.Assemble_weight.setText(str(weight) + " / " + str(load))
        
        # 와트 계산
        watt = 0
        
        watt += legData["Watt"][legIndex]
        watt += bodyData["Watt"][bodyIndex]
        watt += weaponData["Watt"][weaponIndex]
        watt += accData["Watt"][accIndex]
        watt += subCoreData["Watt"][self.Leg_Subcore.currentIndex()]
        watt += subCoreData["Watt"][self.Body_Subcore.currentIndex()]
        watt += subCoreData["Watt"][self.Weapon_Subcore.currentIndex()]
        watt -= utils.getWattReinforce(legData["Watt"][legIndex], int(self.Leg_wattReinforce.text()))
        watt -= utils.getWattReinforce(bodyData["Watt"][bodyIndex], int(self.Body_wattReinforce.text()))
        watt -= utils.getWattReinforce(weaponData["Watt"][weaponIndex], int(self.Weapon_wattReinforce.text()))
        
        magnification = 0
        magnification += subCoreData["WattBonus"][self.Leg_Subcore.currentIndex()]
        magnification += subCoreData["WattBonus"][self.Body_Subcore.currentIndex()]
        magnification += subCoreData["WattBonus"][self.Weapon_Subcore.currentIndex()]
        
        watt *= 1 + magnification / 100
        
        self.Assemble_watt.setText(str(int(watt)))
        
        # 체력 계산
        health = 0
        
        health += legData["Health"][legIndex]
        health += bodyData["Health"][bodyIndex]
        health += weaponData["Health"][weaponIndex]
        health += accData["Health"][accIndex]
        health += subCoreData["Health"][self.Leg_Subcore.currentIndex()]
        health += subCoreData["Health"][self.Body_Subcore.currentIndex()]
        health += subCoreData["Health"][self.Weapon_Subcore.currentIndex()]
        health += utils.getHealthReinforce(legData["Health"][legIndex], int(self.Leg_healthReinforce.text()), False)
        health += utils.getHealthReinforce(bodyData["Health"][bodyIndex], int(self.Body_healthReinforce.text()), True)
        health += utils.getHealthReinforce(weaponData["Health"][weaponIndex], int(self.Weapon_healthReinforce.text()), False)
        
        magnification = 0
        magnification += legData["HealthBonus"][legIndex]
        magnification += bodyData["HealthBonus"][bodyIndex]
        magnification += weaponData["HealthBonus"][weaponIndex]
        magnification += accData["HealthBonus"][accIndex]
        
        health *= 1 + magnification / 100
        
        self.Assemble_health.setText(str(int(health)))
        
        # 리젠 계산
        regen = 0
        
        regen += legData["Regenerate"][legIndex]
        regen += bodyData["Regenerate"][bodyIndex]
        regen += weaponData["Regenerate"][weaponIndex]
        regen += accData["Regenerate"][accIndex]
        regen += subCoreData["Regenerate"][self.Leg_Subcore.currentIndex()]
        regen += subCoreData["Regenerate"][self.Body_Subcore.currentIndex()]
        regen += subCoreData["Regenerate"][self.Weapon_Subcore.currentIndex()]
        
        self.Assemble_regen.setText(str(int(regen)) + "%")
        
        # 속도 계산
        speed = 0
        
        speed += legData["Speed"][legIndex]
        speed += bodyData["Speed"][bodyIndex]
        speed += weaponData["Speed"][weaponIndex]
        speed += accData["Speed"][accIndex]
        speed += subCoreData["Speed"][self.Leg_Subcore.currentIndex()]
        speed += subCoreData["Speed"][self.Body_Subcore.currentIndex()]
        speed += subCoreData["Speed"][self.Weapon_Subcore.currentIndex()]
        
        self.Assemble_speed.setText(str(int(speed)))
        
        # 연사 계산
        cooldown = 0
        
        cooldown += legData["Cooldown"][legIndex]
        cooldown += bodyData["Cooldown"][bodyIndex]
        cooldown += weaponData["Cooldown"][weaponIndex]
        cooldown += accData["Cooldown"][accIndex]
        cooldown += subCoreData["Cooldown"][self.Leg_Subcore.currentIndex()]
        cooldown += subCoreData["Cooldown"][self.Body_Subcore.currentIndex()]
        cooldown += subCoreData["Cooldown"][self.Weapon_Subcore.currentIndex()]
        
        if cooldown < 50 :
            cooldown = 50
            
        self.Assemble_cooldown.setText(str(int(cooldown)))
        
        # 사거리 계산
        range = 0
        
        range += legData["Range"][legIndex]
        range += bodyData["Range"][bodyIndex]
        range += weaponData["Range"][weaponIndex]
        range += accData["Range"][accIndex]
        range += subCoreData["Range"][self.Leg_Subcore.currentIndex()]
        range += subCoreData["Range"][self.Body_Subcore.currentIndex()]
        range += subCoreData["Range"][self.Weapon_Subcore.currentIndex()]
        
        if weaponData["RangeMinimum"][weaponIndex] != 0 :
            self.Assemble_range.setText(str(weaponData["RangeMinimum"][weaponIndex]) + " - " + str(int(range)))
        else :
            self.Assemble_range.setText(str(int(range)))
            
        # 범위 계산
        splash = 0
        
        splash += legData["Splash"][legIndex]
        splash += bodyData["Splash"][bodyIndex]
        splash += weaponData["Splash"][weaponIndex]
        splash += accData["Splash"][accIndex]
        splash += subCoreData["Splash"][self.Leg_Subcore.currentIndex()]
        splash += subCoreData["Splash"][self.Body_Subcore.currentIndex()]
        splash += subCoreData["Splash"][self.Weapon_Subcore.currentIndex()]
        
        if weaponData["Splash"][weaponIndex] == 0 :
            self.Assemble_splash.setText("없음")
        else :
            self.Assemble_splash.setText(str(int(splash)))
            
        # 시야 계산
        sight = 0
        
        sight += legData["Sight"][legIndex]
        sight += bodyData["Sight"][bodyIndex]
        sight += weaponData["Sight"][weaponIndex]
        sight += accData["Sight"][accIndex]
        sight += subCoreData["Sight"][self.Leg_Subcore.currentIndex()]
        sight += subCoreData["Sight"][self.Body_Subcore.currentIndex()]
        sight += subCoreData["Sight"][self.Weapon_Subcore.currentIndex()]
        
        if sight > 30 : sight = 30
        
        self.Assemble_sight.setText(str(int(sight)))
        
        # 공격 계산
        damage = 0
        
        damage += legData["Damage"][legIndex]
        damage += bodyData["Damage"][bodyIndex]
        damage += weaponData["Damage"][weaponIndex]
        damage += accData["Damage"][accIndex]
        damage += subCoreData["Damage"][self.Leg_Subcore.currentIndex()]
        damage += subCoreData["Damage"][self.Body_Subcore.currentIndex()]
        damage += subCoreData["Damage"][self.Weapon_Subcore.currentIndex()]
        damage += utils.getDamageReinforce(legData["Damage"][legIndex], int(self.Leg_damageReinforce.text()), False)
        damage += utils.getDamageReinforce(bodyData["Damage"][bodyIndex], int(self.Body_damageReinforce.text()), False)
        damage += utils.getDamageReinforce(weaponData["Damage"][weaponIndex], int(self.Weapon_damageReinforce.text()), True)
        
        magnification = 0
        magnification += legData["DamageBonus"][legIndex]
        magnification += bodyData["DamageBonus"][bodyIndex]
        magnification += weaponData["DamageBonus"][weaponIndex]
        magnification += accData["DamageBonus"][accIndex]
        
        damage *= 1 + magnification / 100
        
        self.Assemble_damage.setText(str(int(damage)))
        
        # 체력 비례 데미지 계산
        dph = 0
        
        dph += legData["DamagePerHealth"][legIndex]
        dph += bodyData["DamagePerHealth"][bodyIndex]
        dph += weaponData["DamagePerHealth"][weaponIndex]
        dph += accData["DamagePerHealth"][accIndex]
        dph += subCoreData["DamagePerHealth"][self.Leg_Subcore.currentIndex()]
        dph += subCoreData["DamagePerHealth"][self.Body_Subcore.currentIndex()]
        dph += subCoreData["DamagePerHealth"][self.Weapon_Subcore.currentIndex()]
        
        if dph != 0 :
            self.Assemble_dph.setText(str(int(dph)) + "%")
        else :
            self.Assemble_dph.setText("없음")
            
        # 방어 무시 계산
        pierce = 0
        
        pierce += legData["Pierce"][legIndex]
        pierce += bodyData["Pierce"][bodyIndex]
        pierce += weaponData["Pierce"][weaponIndex]
        pierce += accData["Pierce"][accIndex]
        pierce += subCoreData["Pierce"][self.Leg_Subcore.currentIndex()]
        pierce += subCoreData["Pierce"][self.Body_Subcore.currentIndex()]
        pierce += subCoreData["Pierce"][self.Weapon_Subcore.currentIndex()]
        
        self.Assemble_pierce.setText(str(int(pierce)))
        
        # 방어 계산
        armor = 0
        
        armor += legData["Armor"][legIndex]
        armor += bodyData["Armor"][bodyIndex]
        armor += weaponData["Armor"][weaponIndex]
        armor += accData["Armor"][accIndex]
        armor += subCoreData["Armor"][self.Leg_Subcore.currentIndex()]
        armor += subCoreData["Armor"][self.Body_Subcore.currentIndex()]
        armor += subCoreData["Armor"][self.Weapon_Subcore.currentIndex()]
        
        # 기타 특수 능력 정보 표시
        string = ""
        
        if legData["Special"][legIndex] :
            string += legData["Special"][legIndex] + "\n"
            
        if bodyData["Special"][bodyIndex] :
            string += bodyData["Special"][bodyIndex] + "\n"
            
        if weaponData["Special"][weaponIndex] :
            string += weaponData["Special"][weaponIndex] + "\n"
            
        if accData["Special"][accIndex] :
            string += accData["Special"][accIndex] + "\n"
        
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
        
        # 형태 불일치
        if bodyData["Type"][bodyIndex] != weaponData["Type"][weaponIndex] :
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
        if legData["N"][legIndex] + bodyData["N"][bodyIndex] + weaponData["N"][weaponIndex] > 1 :
            if legData["N"][legIndex] :
                self.LegBtn.setStyleSheet("QPushButton"
                                          "{"
                                          "border : 2px solid red;"
                                          "background : white;"
                                          "color : red"
                                          "}")
            if bodyData["N"][bodyIndex] :
                self.BodyBtn.setStyleSheet("QPushButton"
                                          "{"
                                          "border : 2px solid red;"
                                          "background : white;"
                                          "color : red"
                                          "}")
            if weaponData["N"][weaponIndex] :
                self.WeaponBtn.setStyleSheet("QPushButton"
                                          "{"
                                          "border : 2px solid red;"
                                          "background : white;"
                                          "color : red"
                                          "}")
                
        # 아포칼립스
        if weaponIndex == 60 :
            if bodyData["Weight"][bodyIndex] < 30 :
                self.BodyBtn.setStyleSheet("QPushButton"
                                          "{"
                                          "border : 2px solid red;"
                                          "background : white;"
                                          "color : red"
                                          "}")
            if "타워링" in accData["Name"][accIndex] :
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
        elif bodyData["Type"][bodyIndex] != weaponData["Type"][weaponIndex] :
            self.Assemble_label.setText("형태 불일치")
            
        # 하중 초과
        elif weight > load :
            self.Assemble_label.setText("하중 초과")
            
        # N템 개수 초과
        elif legData["N"][legIndex] + bodyData["N"][bodyIndex] + weaponData["N"][weaponIndex] > 1 :
            self.Assemble_label.setText("N템 개수 초과")
            
        # 아포칼립스
        elif weaponIndex == 60 :
            if bodyData["Weight"][bodyIndex] < 30 :
                self.Assemble_label.setText("무게 30 이상 몸통 필요")
            elif "타워링" in accData["Name"][accIndex] :
                self.Assemble_label.setText("타워링과 조립 불가")
        
        # 조립 완료
        else :
            self.LegBtn.setStyleSheet("")
            self.BodyBtn.setStyleSheet("")
            self.WeaponBtn.setStyleSheet("")
            self.AccBtn.setStyleSheet("")
            self.Assemble_weight.setStyleSheet("")
            self.Assemble_label.setText("조립 완료")
        
        
        

if __name__ == "__main__" :
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()