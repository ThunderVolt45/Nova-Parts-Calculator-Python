import re
import os
import sys
import json
import ctypes
import utils
import constant
import assemble
from PyQt6.QtWidgets import *
from PyQt6 import uic, QtCore
from partSelector import partSelector
from typeSelector import typeSelector

###############################################################
# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
def resource_path(relativePath):
    # Get absolute path to resource, works for dev and for PyInstaller
    basePath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(basePath, relativePath)

def enable_windows_dpi_awareness():
    if sys.platform != "win32":
        return

    try:
        if ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4)):
            return
    except (AttributeError, OSError):
        pass

    try:
        if ctypes.windll.shcore.SetProcessDpiAwareness(2) == 0:
            return
    except (AttributeError, OSError):
        pass

    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except (AttributeError, OSError):
        pass

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
    
    totalWatt = 0
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
            
        # QPushButton 기능 연결
        self.LegBtn.clicked.connect(self.LegBtnFunction)
        self.BodyBtn.clicked.connect(self.BodyBtnFunction)
        self.WeaponBtn.clicked.connect(self.WeaponBtnFunction)
        self.AccBtn.clicked.connect(self.AccBtnFunction)
        self.Assemble_btn.clicked.connect(self.Assemble)
        self.Initialize_btn.clicked.connect(self.Initialize)
        
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
        self.Acc_armorReinforce.textChanged.connect(self.AccArmorReinforce)
        self.Acc_healthReinforce.textChanged.connect(self.AccHealthReinforce)
        self.Acc_damageReinforce.textChanged.connect(self.AccDamageReinforce)
        self.Skill_TeamdualPlayer.textChanged.connect(self.SetTeamdualPlayer)
        self.Skill_SacrifyWatt.textChanged.connect(self.SetSacrifyWatt)
        self.Skill_TeamattackPlayer.textChanged.connect(self.SetTeamAttackPlayer)
        self.Skill_TeamdefensePlayer.textChanged.connect(self.SetTeamDefensePlayer)
        self.Status_SquareDamage.textChanged.connect(self.SetSquareDamagePlayer)
        self.Status_SquareSpeed.textChanged.connect(self.SetSquareSpeedPlayer)
        self.Status_SquareCooldown.textChanged.connect(self.SetSquareCooldownPlayer)
        
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
        
        # QCheckBox 기능 연결
        self.Status_BodyLowHealth.stateChanged.connect(self.SetTotalDamageArmor)
        self.Status_WeaponEffect.stateChanged.connect(self.SetWeaponEffect)
        self.Status_Towering.stateChanged.connect(self.SetTowering)
        self.Status_Deathmatch.stateChanged.connect(self.SetTotalDamage)
        self.Skill_Attackbase.stateChanged.connect(self.SetTotalDamage)
        self.Skill_Defensebase.stateChanged.connect(self.SetTotalArmor)
        self.Skill_GAAttack.stateChanged.connect(self.SetTotalDamage)
        self.Skill_GASpeed.stateChanged.connect(self.SetTotalSpeed)
        self.Skill_GADelay.stateChanged.connect(self.SetTotalCooldown)
        self.Skill_Despera.stateChanged.connect(self.SetTotalDamage)
        self.Skill_Devilspirit.stateChanged.connect(self.SetTotalDamage)
        self.Skill_GADefense.stateChanged.connect(self.SetTotalArmor)
        self.Skill_GASight.stateChanged.connect(self.SetTotalSight)
        self.Skill_Moral.stateChanged.connect(self.SetTotalDamageArmor)

        self.Initialize()

    def LegBtnFunction(self) :
        global legIndex
        temp = [ constant.LEG, legIndex ]
        
        self.BtnFunction(temp)
        
        # 두 번째 창에서 값을 전달 받음
        legIndex = self.second.value
        
        self.LegSetup()

    def LegSetup(self) :
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
        
        # self.BtnFunction(temp)
        self.BtnTypeFunction(temp)
        
        # 두 번째 창에서 값을 전달 받음
        bodyIndex = self.second.value

        self.BodySetup()

    def BodySetup(self) :
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
        
        # self.BtnFunction(temp)
        self.BtnTypeFunction(temp)
        
        # 두 번째 창에서 값을 전달 받음
        weaponIndex = self.second.value

        self.WeaponSetup()

    def WeaponSetup(self) :
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

        self.AccSetup()

    def AccSetup(self) :
        self.AccBtn.setText(accData[accIndex]["Name"])
        self.Acc_healthBase.setText(str(accData[accIndex]["Health"]))
        self.Acc_damageBase.setText(str(accData[accIndex]["Damage"]))
        self.Acc_armorBase.setText(str(accData[accIndex]["Armor"]))

        self.Acc_weight.setText("무게 " + str(accData[accIndex]["Weight"]))
        self.Acc_watt.setText("와트 " + str(accData[accIndex]["Watt"]))
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

        self.SetAccReinforceValue()
        
    @QtCore.pyqtSlot()
    def BtnFunction(self, list) : # Widget 연결
        self.second = partSelector()
        self.signal.connect(self.second.on_signal_from_main) # 시그널 연결
        self.signal.emit(list) # 값 전달
        self.second.exec() # 두 번째 창이 꺼질 때까지 대기
    
    @QtCore.pyqtSlot()
    def BtnTypeFunction(self, list) :
        self.second = typeSelector()
        self.signal.connect(self.second.on_signal_from_main) # 시그널 연결
        self.signal.emit(list) # 값 전달
        self.second.exec() # 두 번째 창이 꺼질 때까지 대기
        
    def LegWattReinforce(self) : 
        string = self.Leg_wattReinforce.text()
        self.Leg_wattReinforce.setText(utils.lineEditToNum(string, 100))
        self.SetLegReinforceValue()
        
    def LegHealthReinforce(self) : 
        string = self.Leg_healthReinforce.text()
        self.Leg_healthReinforce.setText(utils.lineEditToNum(string, 100))
        self.SetLegReinforceValue()
        
    def LegDamageReinforce(self) : 
        string = self.Leg_damageReinforce.text()
        self.Leg_damageReinforce.setText(utils.lineEditToNum(string, 100))
        self.SetLegReinforceValue()
        
    def BodyWattReinforce(self) : 
        string = self.Body_wattReinforce.text()
        self.Body_wattReinforce.setText(utils.lineEditToNum(string, 100))
        self.SetBodyReinforceValue()
        
    def BodyHealthReinforce(self) : 
        string = self.Body_healthReinforce.text()
        self.Body_healthReinforce.setText(utils.lineEditToNum(string, 100))
        self.SetBodyReinforceValue()
        
    def BodyDamageReinforce(self) : 
        string = self.Body_damageReinforce.text()
        self.Body_damageReinforce.setText(utils.lineEditToNum(string, 100))
        self.SetBodyReinforceValue()
        
    def WeaponWattReinforce(self) : 
        string = self.Weapon_wattReinforce.text()
        self.Weapon_wattReinforce.setText(utils.lineEditToNum(string, 100))
        self.SetWeaponReinforceValue()
        
    def WeaponHealthReinforce(self) : 
        string = self.Weapon_healthReinforce.text()
        self.Weapon_healthReinforce.setText(utils.lineEditToNum(string, 100))
        self.SetWeaponReinforceValue()
        
    def WeaponDamageReinforce(self) : 
        string = self.Weapon_damageReinforce.text()
        self.Weapon_damageReinforce.setText(utils.lineEditToNum(string, 100))
        self.SetWeaponReinforceValue()

    def AccArmorReinforce(self):
        string = self.Acc_armorReinforce.text()
        self.Acc_armorReinforce.setText(utils.lineEditToNum(string, 10))
        self.SetAccReinforceValue()

    def AccHealthReinforce(self):
        string = self.Acc_healthReinforce.text()
        self.Acc_healthReinforce.setText(utils.lineEditToNum(string, 200))
        self.SetAccReinforceValue()

    def AccDamageReinforce(self):
        string = self.Acc_damageReinforce.text()
        self.Acc_damageReinforce.setText(utils.lineEditToNum(string, 20))
        self.SetAccReinforceValue()

    def SetTeamdualPlayer(self):
        string = self.Skill_TeamdualPlayer.text()
        self.Skill_TeamdualPlayer.setText(utils.lineEditToNum(string, 12))
        self.SetTotalDamage()
        self.SetTotalArmor()

    def SetSacrifyWatt(self):
        string = self.Skill_SacrifyWatt.text()
        self.Skill_SacrifyWatt.setText(utils.lineEditToNum(string, 2500))
        self.SetTotalArmor()

    def SetTeamAttackPlayer(self):
        string = self.Skill_TeamattackPlayer.text()
        self.Skill_TeamattackPlayer.setText(utils.lineEditToNum(string, 12))
        self.SetTotalDamage()

    def SetTeamDefensePlayer(self):
        string = self.Skill_TeamdefensePlayer.text()
        self.Skill_TeamdefensePlayer.setText(utils.lineEditToNum(string, 12))
        self.SetTotalArmor()

    def SetSquareDamagePlayer(self):
        string = self.Status_SquareDamage.text()
        self.Status_SquareDamage.setText(utils.lineEditToNum(string, 50))
        self.SetTotalDamage()

    def SetSquareSpeedPlayer(self):
        string = self.Status_SquareSpeed.text()
        self.Status_SquareSpeed.setText(utils.lineEditToNum(string, 50))
        self.SetTotalSpeed()

    def SetSquareCooldownPlayer(self):
        string = self.Status_SquareCooldown.text()
        self.Status_SquareCooldown.setText(utils.lineEditToNum(string, 50))
        self.SetTotalCooldown()

    def SetLegReinforceValue(self) :
        wattBase = utils.getWattBase(legData[legIndex]["Watt"])
        healthBase = utils.getHealthBase(legData[legIndex]["Watt"], False)
        damageBase = utils.getDamageBase(legData[legIndex]["Watt"], False)

        if not calculateAsFloat:
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

    def SetAccReinforceValue(self):
        if not accData[accIndex]["HasRandomOption"] :
            self.Acc_armorAdd.setText("/ 0")
            self.Acc_healthAdd.setText("/ 0")
            self.Acc_damageAdd.setText("/ 0")
        else :
            self.Acc_armorAdd.setText("/ 10")
            self.Acc_healthAdd.setText("/ 200")
            self.Acc_damageAdd.setText("/ 20")

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

    def SetTotalDamage(self) :
        if not self.Assemble_damage.text().isdigit() :
            self.Assemble_totaldamage.setText("없음")
        else :
            totalWatt = int(self.Assemble_watt.text())
            damageResult = int(self.Assemble_damage.text())
            halfDamage = int(damageResult / 2) # 공격력의 50%
            damage30 = int((damageResult * 30) / 100) # 공격력의 30%
            if self.Status_BodyLowHealth.isChecked() :
                if bodyData[bodyIndex]["LowHealthEffect"] == 2 : # 버서커
                    damageResult += halfDamage
            if self.Status_WeaponEffect.isChecked() :
                if weaponData[weaponIndex]["WeaponEffect"] == 3 : # 해머쇼크N
                    damageResult += halfDamage
                elif weaponData[weaponIndex]["WeaponEffect"] == 4 : # 아누아이, 베베세
                    damageResult += damage30
                elif weaponData[weaponIndex]["WeaponEffect"] == 5 : # 멀티샷건
                    damageResult = int(damageResult / 3)
            if self.Skill_Despera.isChecked() :
                damageResult += halfDamage
            if self.Skill_Devilspirit.isChecked() :
                damageResult += halfDamage
            if self.Status_Towering.isChecked() :
                if accData[accIndex]["Towering"] == 2 : # 타워링II, III
                    damageResult = int((damageResult * 3) / 2)
                elif accData[accIndex]["Towering"] == 1 : # 타워링, S
                    damageResult *= 2
            if self.Skill_Attackbase.isChecked() :
                damageResult += utils.getAttackDefenseBase(totalWatt)
            damageResult += utils.getTeamDual(totalWatt, int(self.Skill_TeamdualPlayer.text()))
            if self.Skill_GAAttack.isChecked() :
                damageResult += 15
            if self.Skill_Moral.isChecked() :
                damageResult += 20
            damageResult += 3 * int(self.Skill_TeamattackPlayer.text())
            damageResult += 50 * int(self.Status_SquareDamage.text())
            if self.Status_Deathmatch.isChecked() :
                damageResult *= 2
            self.Assemble_totaldamage.setText(str(damageResult))

    def SetTotalArmor(self) :
        totalWatt = int(self.Assemble_watt.text())
        armorResult = int(self.Assemble_armor.text())
        if self.Status_BodyLowHealth.isChecked() :
            if bodyData[bodyIndex]["LowHealthEffect"] == 1 : # 킬핀, 제니스
                armorResult += 40
        if self.Status_WeaponEffect.isChecked() :
            if weaponData[weaponIndex]["WeaponEffect"] == 2 : # 해머쇼크
                armorResult += 25
        if self.Status_Towering.isChecked() :
            if accData[accIndex]["Towering"] != 0 :
                armorResult += 20
        if self.Skill_Defensebase.isChecked() :
            armorResult += utils.getAttackDefenseBase(totalWatt)
        if self.Skill_GADefense.isChecked() :
            armorResult += 15
        if self.Skill_Moral.isChecked() :
            armorResult += 20
        armorResult += utils.getTeamDual(totalWatt, int(self.Skill_TeamdualPlayer.text()))
        armorResult += int((int(self.Skill_SacrifyWatt.text()) * 3) / 100)
        armorResult += 3 * int(self.Skill_TeamdefensePlayer.text())
        self.Assemble_totalarmor.setText(str(armorResult))

    def SetTotalSight(self) :
        sightResult = int(self.Assemble_sight.text())
        if self.Skill_GASight.isChecked() :
            sightResult += 9
        if sightResult > 30 : sightResult = 30
        self.Assemble_totalsight.setText(str(sightResult))

    def SetTotalHealth(self) :
        healthResult = int(self.Assemble_health.text())
        if self.Status_Towering.isChecked() :
            if accData[accIndex]["Towering"] == 2 : # 타워링II, III
                healthResult = int((healthResult * 3) / 2)
            elif accData[accIndex]["Towering"] == 1 : # 타워링, S
                healthResult *= 2
        self.Assemble_totalhealth.setText(str(healthResult))

    def SetTotalRange(self) :
        rangeResult = int(self.Assemble_range.text())
        if self.Status_Towering.isChecked() :
            if accData[accIndex]["Towering"] == 2 : # 타워링II, III
                rangeResult -= 2
            elif accData[accIndex]["Towering"] == 1 : # 타워링, S
                rangeResult += 3

        minRange = int(weaponData[weaponIndex]["RangeMinimum"])
        if rangeResult < minRange :
            rangeResult = minRange
        if minRange > 0 :
            self.Assemble_totalrange.setText(str(minRange) + " - " + str(rangeResult))
        else :
            self.Assemble_totalrange.setText(str(rangeResult))

    def SetTotalSpeed(self) :
        speedResult = int(self.Assemble_speed.text())
        if self.Skill_GASpeed.isChecked() :
            speedResult += 20
        if self.Status_WeaponEffect.isChecked() :
            if weaponData[weaponIndex]["WeaponEffect"] == 1 : # 리코일건N
                speedResult += 30

        speedResult += 20 * int(self.Status_SquareSpeed.text())
        if speedResult > 120 : speedResult = 120
        self.Assemble_totalspeed.setText(str(speedResult))

    def SetTotalCooldown(self) :
        cooldownResult = int(self.Assemble_cooldown.text())
        if self.Status_Towering.isChecked() :
            if accData[accIndex]["Towering"] == 2 : # 타워링II, III
                cooldownResult -= 50
        if self.Skill_GADelay.isChecked() :
            cooldownResult -= 50

        cooldownResult -= 100 * int(self.Status_SquareCooldown.text())
        if cooldownResult < 50 : cooldownResult = 50
        self.Assemble_totalcooldown.setText(str(cooldownResult))

    def SetHealAmount(self) :
        damageResult = int(self.Assemble_totaldamage.text()) if self.Assemble_totaldamage.text().isdigit() else 0
        healPercentage = weaponData[weaponIndex]["HealAmount"]
        if damageResult > 0 and healPercentage != 0 :
            healAmount = int((damageResult * healPercentage) / 100)
            self.Assemble_healamount.setText(str(healAmount))
        else :
            self.Assemble_healamount.setText("0")

    def SetRegenAmount(self) :
        healthResult = int(self.Assemble_totalhealth.text())
        regenText = re.findall(r"-?\d+", self.Assemble_regen.text())
        regenPercentage = int(''.join(regenText))
        if healthResult > 0 and regenPercentage != 0 :
            regenAmount = int((healthResult * regenPercentage) / 100)
            self.Assemble_regenamount.setText(str(regenAmount))
        else :
            self.Assemble_regenamount.setText("0")

    def SetTowering(self) :
        self.SetTotalDamage()
        self.SetTotalArmor()
        self.SetTotalHealth()
        self.SetTotalRange()
        self.SetTotalCooldown()

    def SetTotalDamageArmor(self) :
        self.SetTotalDamage()
        self.SetTotalArmor()

    def SetWeaponEffect(self) :
        self.SetTotalDamage()
        self.SetTotalArmor()
        self.SetTotalSpeed()

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
        self.Assemble_health.setText(str(assemble.GetHealth(partsIndex, subIndex, healthReinforce, int(self.Acc_healthReinforce.text()), self.actionFloat.isChecked())))
        self.SetTotalHealth()
        
        # 리젠 계산
        self.Assemble_regen.setText(str(int(assemble.GetRegenerate(partsIndex, subIndex))) + "%")
        
        # 속도 계산
        self.Assemble_speed.setText(str(int(assemble.GetSpeed(partsIndex, subIndex))))
        self.SetTotalSpeed()
        
        # 연사 계산
        self.Assemble_cooldown.setText(str(int(assemble.GetCooldown(partsIndex, subIndex))))
        self.SetTotalCooldown()
        
        # 사거리 계산
        self.Assemble_range.setText(str(int(assemble.GetRange(partsIndex, subIndex))))

        self.Assemble_minrange.setText(str(weaponData[weaponIndex]["RangeMinimum"]))
        self.SetTotalRange()

        # 범위 계산
        splash = assemble.GetSplash(partsIndex, subIndex)
        
        if weaponData[weaponIndex]["Splash"] == 0 :
            self.Assemble_splash.setText("없음")
        else :
            self.Assemble_splash.setText(str(int(splash)))
            
        # 시야 계산
        self.Assemble_sight.setText(str(int(assemble.GetSight(partsIndex, subIndex))))
        self.SetTotalSight()
        
        # 공격 계산
        damageReinforce = (int(self.Leg_damageReinforce.text()), int(self.Body_damageReinforce.text()), int(self.Weapon_damageReinforce.text()))
        
        if not weaponData[weaponIndex]["CanAttackGround"] and not weaponData[weaponIndex]["CanAttackAir"] :
            self.Assemble_damage.setText("없음")
        else :
            self.Assemble_damage.setText(str(assemble.GetDamage(partsIndex, subIndex, damageReinforce, int(self.Acc_damageReinforce.text()), self.actionFloat.isChecked())))
        self.SetTotalDamage()
        
        # 체력 비례 데미지 계산
        dph = assemble.GetDamagePerHealth(partsIndex, subIndex)
        
        if dph != 0 :
            self.Assemble_dph.setText(str(int(dph)) + "%")
        else :
            self.Assemble_dph.setText("없음")
            
        # 방어 무시 계산
        self.Assemble_pierce.setText(str(int(assemble.GetPierce(partsIndex, subIndex))))
        
        # 방어 계산
        self.Assemble_armor.setText(str(int(assemble.GetArmor(partsIndex, subIndex, int(self.Acc_armorReinforce.text())))))
        self.SetTotalArmor()

        # 체력 회복량 계산
        self.SetHealAmount()
        self.SetRegenAmount()
        
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

    def Initialize(self) :
        # 인덱스 초기화
        global legIndex
        global bodyIndex
        global weaponIndex
        global accIndex
        legIndex = 0
        bodyIndex = 0
        weaponIndex = 0
        accIndex = 0

        # 서브코어 초기화
        self.Leg_Subcore.clear()
        self.Body_Subcore.clear()
        self.Weapon_Subcore.clear()
        for i in range(len(subCoreData["ID"])):
            self.Leg_Subcore.addItem(subCoreData["Name"][i])
            self.Body_Subcore.addItem(subCoreData["Name"][i])
            self.Weapon_Subcore.addItem(subCoreData["Name"][i])

        self.LegSetup()
        self.BodySetup()
        self.WeaponSetup()
        self.AccSetup()

        # 강화수치 초기화
        self.Leg_wattReinforce.setText("0")
        self.Leg_healthReinforce.setText("0")
        self.Leg_damageReinforce.setText("0")

        self.Body_wattReinforce.setText("0")
        self.Body_healthReinforce.setText("0")
        self.Body_damageReinforce.setText("0")

        self.Weapon_wattReinforce.setText("0")
        self.Weapon_healthReinforce.setText("0")
        self.Weapon_damageReinforce.setText("0")

        self.Acc_healthReinforce.setText("0")
        self.Acc_damageReinforce.setText("0")
        self.Acc_armorReinforce.setText("0")

        self.Assemble()

        # styleSheet 초기화
        self.LegBtn.setStyleSheet("")
        self.BodyBtn.setStyleSheet("")
        self.WeaponBtn.setStyleSheet("")
        self.AccBtn.setStyleSheet("")
        self.Assemble_weight.setStyleSheet("")

    def CalculateAsFloat(self) :
        global calculateAsFloat
        calculateAsFloat = self.actionFloat.isChecked()
        self.SetLegReinforceValue()
        self.SetBodyReinforceValue()
        self.SetWeaponReinforceValue()

if __name__ == "__main__" :
    enable_windows_dpi_awareness()

    QApplication.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    app.setApplicationName("Nova Parts Calculator")

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec()
