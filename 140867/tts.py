bob = {}
max = int(input("คะแนนที่ได้มากสุด : "))
x = int(input("จำนวนคน : "))
def gg():
    print('--------------------------')
gg()
i = 1
maxhit = 0
def name1():
    global bob,maxhit
    z = input("pls enter you name : ")
    score = int(input("pls enter your score : "))
    time = int(input("pls enter your get time : "))
    gg()
    hitfac = score/time
    stateper = 0
    statepts = 0
    bob[z] = score,time,hitfac,statepts,stateper
def name2() :
    print("{0: <15}{1: <15}{2: <15}{3: <15}{4: <15}{5: <15}".format("name","score",'times','hitfactor','statepts','statepercent'))
    for z,(score,time,hitfac,statepts,stateper) in bob.items():
        statepts = (score*hitfac)/maxhit
        stateper = (statepts/max)*100
        if hitfac > maxhit:
            maxhit = hitfac
        print("{0: <15}{1: <15}{2: <15}{3: <15}{4: <15}{5: <15}".format(z,score,time,hitfac,statepts,stateper))
while(i<=x):
    name1()
    i+=1
name2()
