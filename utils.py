import re

def lineEditToNum(string: str, maxval : int = 100) :
    temp = re.sub(r'[^0-9]', '', string)
    
    if temp == "" : return "0"
    
    num = int(temp)
    
    if num > maxval : num = maxval
    elif num < 0 : num = 0
    
    return str(num)

def getWattReinforce(watt: int, reinforce: int, calculateAsFloat: bool) :
    if calculateAsFloat :
        return getWattBase(watt) * reinforce / 100
    else :
        return int(getWattBase(watt) * reinforce / 100)

def getHealthReinforce(value: int, reinforce: int, isBody: bool, calculateAsFloat: bool) :
    if calculateAsFloat :
        return getHealthBase(value, isBody) * reinforce / 100
    else :
        return int(getHealthBase(value, isBody) * reinforce / 100)

def getDamageReinforce(value: int, reinforce: int, isWeapon: bool, calculateAsFloat: bool) :
    if calculateAsFloat :
        return getDamageBase(value, isWeapon) * reinforce / 100
    else :
        return int(getDamageBase(value, isWeapon) * reinforce / 100)

def getWattBase(watt: int) :
    return watt / 4

def getHealthBase(val: int, isBody: bool) :
    health = 0
    
    # 입력 값으로 체력을 받아야 한다
    if isBody :
        health = 50 + val / 4
    
    # 입력 값으로 와트를 받아야 한다
    else :
        if val - 70 <= 0 :
            health = 50
        else :
            health = 50 + (val - 70) / 4
    
    return health
    
def getDamageBase(val: int, isWeapon: bool) :
    damage = 0
    
    if isWeapon :
        damage = val / 4 + 3
    else : 
        if val / 30 < 3 : 
            damage = 3
        else :
            damage = val / 30
    
    return damage

# 공격 기본, 방어 기본 적용치 계산
def getAttackDefenseBase(watt: int) :
    damageArmorIncrease = (int)(3 + (watt / 200))
    return 10 if damageArmorIncrease > 10 else damageArmorIncrease

# 팀 듀얼 적용치 계산
def getTeamDual(watt: int, player: int) :
    damageArmorIncrease = (int)(1 + (watt / 300))

    if player > 12 : player = 12
    if player < 0 : player = 0

    return (5 if damageArmorIncrease > 5 else damageArmorIncrease) * player