plo = {}
x = int(input("จำนวนคน: "))
i = 1
maxhit = 0

def name1():
    global maxhit
    key = input("ชื่อ: ")
    value = int(input("คะแนน: "))
    means = int(input("เวลา: "))
    HitFac = value / means
    StateP = 0
    statepercent = 0
    if HitFac > maxhit:
        maxhit = HitFac
    plo[key] = (value, means, HitFac, StateP, statepercent)

def name3():
    print("{0: <15}{1: <15}{2: <15}{3: <15}{4: <15}{5: <15}".format("ชื่อ", "คะแนน", "เวลา", "HIT_FAC", "STATE_POINT", "STATE_PERCENT"))
    for key, (value, means, HitFac, StateP, statepercent) in plo.items():
        StateP = (value * HitFac) / maxhit
        statepercent = (StateP / maxhit) * 100
        print("{0: <15}{1: <15}{2: <15}{3: <15}{4: <15}{5: <15}".format(key, value, means, HitFac, StateP, statepercent))

while i <= x:
    name1()
    i += 1 

name3()
