import json
import utils
import constant

# JSON 파일 읽기
global legData
with open(constant.FILE_PATH_LEG, "r", encoding="UTF-8") as file:
    legData = json.load(file)

global bodyData
with open(constant.FILE_PATH_BODY, "r", encoding="UTF-8") as file:
    bodyData = json.load(file)

global weaponData
with open(constant.FILE_PATH_WEAPON, "r", encoding="UTF-8") as file:
    weaponData = json.load(file)

global accData
with open(constant.FILE_PATH_ACC, "r", encoding="UTF-8") as file:
    accData = json.load(file)

global subCoreData
with open(constant.FILE_PATH_SUBCORE, "r", encoding="UTF-8") as file:
    subCoreData = json.load(file)

def GetWeight(partsIndex: tuple):
    # 무게 / 하중 계산
    weight = 0
        
    weight += bodyData[partsIndex[1]]["Weight"]
    weight += weaponData[partsIndex[2]]["Weight"]
    weight += accData[partsIndex[3]]["Weight"]
    
    return weight

def GetWatt(partsIndex: tuple, subIndex: tuple, reinforce: tuple, calculateAsFloat: bool):
    # 와트 계산
    watt = 0

    watt += legData[partsIndex[0]]["Watt"]
    watt += bodyData[partsIndex[1]]["Watt"]
    watt += weaponData[partsIndex[2]]["Watt"]
    watt += accData[partsIndex[3]]["Watt"]
    watt += subCoreData["Watt"][subIndex[0]]
    watt += subCoreData["Watt"][subIndex[1]]
    watt += subCoreData["Watt"][subIndex[2]]
    watt -= utils.getWattReinforce(legData[partsIndex[0]]["Watt"], reinforce[0], calculateAsFloat)
    watt -= utils.getWattReinforce(bodyData[partsIndex[1]]["Watt"], reinforce[1], calculateAsFloat)
    watt -= utils.getWattReinforce(weaponData[partsIndex[2]]["Watt"], reinforce[2], calculateAsFloat)

    magnification = 0
    magnification += subCoreData["WattBonus"][subIndex[0]]
    magnification += subCoreData["WattBonus"][subIndex[1]]
    magnification += subCoreData["WattBonus"][subIndex[2]]

    watt *= 1 + magnification / 100
    
    if calculateAsFloat : return watt
    else : return int(watt)

def GetHealth(partsIndex: tuple, subIndex: tuple, reinforce: tuple, calculateAsFloat: bool):
    # 체력 계산
    health = 0
    
    health += legData[partsIndex[0]]["Health"]
    health += bodyData[partsIndex[1]]["Health"]
    health += weaponData[partsIndex[2]]["Health"]
    health += accData[partsIndex[3]]["Health"]
    health += subCoreData["Health"][subIndex[0]]
    health += subCoreData["Health"][subIndex[1]]
    health += subCoreData["Health"][subIndex[2]]
    health += utils.getHealthReinforce(legData[partsIndex[0]]["Watt"], reinforce[0], False, calculateAsFloat)
    health += utils.getHealthReinforce(bodyData[partsIndex[1]]["Health"], reinforce[1], True, calculateAsFloat)
    health += utils.getHealthReinforce(weaponData[partsIndex[2]]["Watt"], reinforce[2], False, calculateAsFloat)
        
    magnification = 0
    magnification += legData[partsIndex[0]]["HealthBonus"]
    magnification += bodyData[partsIndex[1]]["HealthBonus"]
    magnification += weaponData[partsIndex[2]]["HealthBonus"]
    magnification += accData[partsIndex[3]]["HealthBonus"]
        
    health *= 1 + magnification / 100
    
    if calculateAsFloat : return health
    else : return int(health)

def GetDamage(partsIndex: tuple, subIndex: tuple, reinforce: tuple, calculateAsFloat: bool):
    # 공격력 계산
    damage = 0
    
    damage += legData[partsIndex[0]]["Damage"]
    damage += bodyData[partsIndex[1]]["Damage"]
    damage += weaponData[partsIndex[2]]["Damage"]
    damage += accData[partsIndex[3]]["Damage"]
    damage += subCoreData["Damage"][subIndex[0]]
    damage += subCoreData["Damage"][subIndex[1]]
    damage += subCoreData["Damage"][subIndex[2]]
    damage += utils.getDamageReinforce(legData[partsIndex[0]]["Watt"], reinforce[0], False, calculateAsFloat)
    damage += utils.getDamageReinforce(bodyData[partsIndex[1]]["Watt"], reinforce[1], False, calculateAsFloat)
    damage += utils.getDamageReinforce(weaponData[partsIndex[2]]["Damage"], reinforce[2], True, calculateAsFloat)
        
    magnification = 0
    magnification += legData[partsIndex[0]]["DamageBonus"]
    magnification += bodyData[partsIndex[1]]["DamageBonus"]
    magnification += weaponData[partsIndex[2]]["DamageBonus"]
    magnification += accData[partsIndex[3]]["DamageBonus"]
        
    damage *= 1 + magnification / 100
    
    if calculateAsFloat : return damage
    else : return int(damage)
    
def GetRegenerate(partsIndex: tuple, subIndex: tuple):
    # 리젠 계산
    regen = 0
    
    regen += legData[partsIndex[0]]["Regenerate"]
    regen += bodyData[partsIndex[1]]["Regenerate"]
    regen += weaponData[partsIndex[2]]["Regenerate"]
    regen += accData[partsIndex[3]]["Regenerate"]
    regen += subCoreData["Regenerate"][subIndex[0]]
    regen += subCoreData["Regenerate"][subIndex[1]]
    regen += subCoreData["Regenerate"][subIndex[2]]
    
    return regen

def GetSpeed(partsIndex: tuple, subIndex: tuple):
    # 속도 계산
    speed = 0
        
    speed += legData[partsIndex[0]]["Speed"]
    speed += bodyData[partsIndex[1]]["Speed"]
    speed += weaponData[partsIndex[2]]["Speed"]
    speed += accData[partsIndex[3]]["Speed"]
    speed += subCoreData["Speed"][subIndex[0]]
    speed += subCoreData["Speed"][subIndex[1]]
    speed += subCoreData["Speed"][subIndex[2]]
    
    if speed > 120 : speed = 120
    
    return speed

def GetCooldown(partsIndex: tuple, subIndex: tuple):
    # 연사 계산
    cooldown = 0
        
    cooldown += legData[partsIndex[0]]["Cooldown"]
    cooldown += bodyData[partsIndex[1]]["Cooldown"]
    cooldown += weaponData[partsIndex[2]]["Cooldown"]
    cooldown += accData[partsIndex[3]]["Cooldown"]
    cooldown += subCoreData["Cooldown"][subIndex[0]]
    cooldown += subCoreData["Cooldown"][subIndex[1]]
    cooldown += subCoreData["Cooldown"][subIndex[2]]
        
    if cooldown < 50 : cooldown = 50
    
    return cooldown

def GetRange(partsIndex: tuple, subIndex: tuple):
    # 사거리 계산
    range = 0
        
    range += legData[partsIndex[0]]["Range"]
    range += bodyData[partsIndex[1]]["Range"]
    range += weaponData[partsIndex[2]]["Range"]
    range += accData[partsIndex[3]]["Range"]
    range += subCoreData["Range"][subIndex[0]]
    range += subCoreData["Range"][subIndex[1]]
    range += subCoreData["Range"][subIndex[2]]
    
    return range

def GetSplash(partsIndex: tuple, subIndex: tuple):
    # 범위 계산
    splash = 0
        
    splash += legData[partsIndex[0]]["Splash"]
    splash += bodyData[partsIndex[1]]["Splash"]
    splash += weaponData[partsIndex[2]]["Splash"]
    splash += accData[partsIndex[3]]["Splash"]
    splash += subCoreData["Splash"][subIndex[0]]
    splash += subCoreData["Splash"][subIndex[1]]
    splash += subCoreData["Splash"][subIndex[2]]
    
    return splash

def GetSight(partsIndex: tuple, subIndex: tuple):
    # 시야 계산
    sight = 0
    
    sight += legData[partsIndex[0]]["Sight"]
    sight += bodyData[partsIndex[1]]["Sight"]
    sight += weaponData[partsIndex[2]]["Sight"]
    sight += accData[partsIndex[3]]["Sight"]
    sight += subCoreData["Sight"][subIndex[0]]
    sight += subCoreData["Sight"][subIndex[1]]
    sight += subCoreData["Sight"][subIndex[2]]
    
    if sight > 30 : sight = 30
    
    return sight

def GetDamagePerHealth(partsIndex: tuple, subIndex: tuple):
    # 체력 비례 데미지 계산
    dph = 0
    
    dph += legData[partsIndex[0]]["DamagePerHealth"]
    dph += bodyData[partsIndex[1]]["DamagePerHealth"]
    dph += weaponData[partsIndex[2]]["DamagePerHealth"]
    dph += accData[partsIndex[3]]["DamagePerHealth"]
    dph += subCoreData["DamagePerHealth"][subIndex[0]]
    dph += subCoreData["DamagePerHealth"][subIndex[1]]
    dph += subCoreData["DamagePerHealth"][subIndex[2]]
    
    return dph

def GetPierce(partsIndex: tuple, subIndex: tuple):
    # 방어 무시 계산
    pierce = 0
    
    pierce += legData[partsIndex[0]]["Pierce"]
    pierce += bodyData[partsIndex[1]]["Pierce"]
    pierce += weaponData[partsIndex[2]]["Pierce"]
    pierce += accData[partsIndex[3]]["Pierce"]
    pierce += subCoreData["Pierce"][subIndex[0]]
    pierce += subCoreData["Pierce"][subIndex[1]]
    pierce += subCoreData["Pierce"][subIndex[2]]
    
    return pierce

def GetArmor(partsIndex: tuple, subIndex: tuple):
    # 방어 계산
    armor = 0
    
    armor += legData[partsIndex[0]]["Armor"]
    armor += bodyData[partsIndex[1]]["Armor"]
    armor += weaponData[partsIndex[2]]["Armor"]
    armor += accData[partsIndex[3]]["Armor"]
    armor += subCoreData["Armor"][subIndex[0]]
    armor += subCoreData["Armor"][subIndex[0]]
    armor += subCoreData["Armor"][subIndex[0]]
    
    if armor < 0 : armor = 0
    
    return armor