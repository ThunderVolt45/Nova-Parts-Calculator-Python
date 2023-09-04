import re

def lineEditToNum(string) :
    temp = re.sub(r'[^0-9]', '', string)
    
    if temp == "" : return "0"
    
    num = int(temp)
    
    if num > 100 : num = 100
    elif num < 0 : num = 0
    
    return str(num)