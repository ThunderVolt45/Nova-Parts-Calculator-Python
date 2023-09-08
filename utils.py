import re

def lineEditToNum(string: str) :
    temp = re.sub(r'[^0-9]', '', string)
    
    if temp == "" : return "0"
    
    num = int(temp)
    
    if num > 100 : num = 100
    elif num < 0 : num = 0
    
    return str(num)

def getWattReinforce(watt: int, reinforce: int) :
    return int(getWattBase(watt) * reinforce / 100) 

def getHealthReinforce(value: int, reinforce: int, isBody: bool) :
    return int(getHealthBase(value, isBody) * reinforce / 100)

def getDamageReinforce(value: int, reinforce: int, isWeapon: bool) :
    return int(getDamageBase(value, isWeapon) * reinforce / 100)

def getWattBase(watt: int) :
    return int(watt / 4)

def getHealthBase(val: int, isBody: bool) :
    # 입력 값으로 체력을 받아야 한다
    if isBody :
        return int(50 + val / 4)
    
    # 입력 값으로 와트를 받아야 한다
    else :
        if val - 70 <= 0 :
            return 50
        else :
            return int(50 + (val - 70) / 4)
    
def getDamageBase(val: int, isWeapon: bool) :
    if isWeapon :
        return int(val / 4 + 3)
    else : 
        if val / 30 < 3 : 
            return 3
        else :
            return int(val / 30)