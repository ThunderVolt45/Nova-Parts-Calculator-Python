import re

def lineEditToNum(string: str) :
    temp = re.sub(r'[^0-9]', '', string)
    
    if temp == "" : return "0"
    
    num = int(temp)
    
    if num > 100 : num = 100
    elif num < 0 : num = 0
    
    return str(num)

def getWattReinforce(watt: int, reinforce: int, calculateAsFloat: bool) :
    if calculateAsFloat :
        return getWattBase(watt, calculateAsFloat) * reinforce / 100
    else :
        return int(getWattBase(watt, calculateAsFloat) * reinforce / 100)

def getHealthReinforce(value: int, reinforce: int, isBody: bool, calculateAsFloat: bool) :
    if calculateAsFloat :
        return getHealthBase(value, isBody, calculateAsFloat) * reinforce / 100
    else :
        return int(getHealthBase(value, isBody, calculateAsFloat) * reinforce / 100)

def getDamageReinforce(value: int, reinforce: int, isWeapon: bool, calculateAsFloat: bool) :
    if calculateAsFloat :
        return getDamageBase(value, isWeapon, calculateAsFloat) * reinforce / 100
    else :
        return int(getDamageBase(value, isWeapon, calculateAsFloat) * reinforce / 100)

def getWattBase(watt: int, calculateAsFloat: bool) :
    if calculateAsFloat :
        return watt / 4
    else :
        return int(watt / 4)

def getHealthBase(val: int, isBody: bool, calculateAsFloat: bool) :
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
    
    if calculateAsFloat :
        return health
    else :
        return int(health)
    
def getDamageBase(val: int, isWeapon: bool, calculateAsFloat: bool) :
    damage = 0
    
    if isWeapon :
        damage = val / 4 + 3
    else : 
        if val / 30 < 3 : 
            damage = 3
        else :
            damage = val / 30
    
    if calculateAsFloat :
        return damage
    else :
        return int(damage)