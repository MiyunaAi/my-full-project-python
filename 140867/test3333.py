def ked():
    print("-----------------------------------------------------------------------------------")
def main():
    global llist
    name = input("ชื่อ : ")
    score = int(input("คะแนน : "))
    time= int(input("เวลา : "))
    ked()
    HitFac=score/time
    llist[name] = score,time,HitFac
def main2():
    global Hitfac,maxhit,llist,score,name,StateP,ptsmax
    for Hitfac in llist:
        if Hitfac > maxhit :
            maxhit = Hitfac
    llist[name] = maxhit
    for StateP in llist :
        if StateP > ptsmax :
            ptsmax = StateP
    llist[name] = ptsmax
    #if hitfac>maxhit :
        #maxhit=HitFac
    #if StateP>ptsmax :
        #ptsmax = StateP
def main3():
    global Hitfac,statepercent,StateP,score,maxhit,ptsmax
    for key,()
        StateP=(score*Hitfac)/maxhit
        statepercent=(StateP/ptsmax)*100
def show():
    ked()
    print("{0: <15}{1: <15}{2: <15}{3: <15}{4: <15}{5: <15}".format("ชื่อ","คะแนน","เวลา","HIT_FAC","STATE_POINT","STATE_PERCENT"))
    for name,(score,time,HitFac,StateP,statepercent) in llist.items():
        print("{0: <15}{1: <15}{2: <15}{3: <15}{4: <15}{5: <15}".format(key,score,time,HitFac,StateP,statepercent))
    ked()


while True :
    try :
        llist = {}
        print("ยินดีต้อนรับ สู่หลินปิงปืนเซนเตอร์")
        x=int(input("จำนวนคน : "))
        from datetime import datetime
        current_time = datetime.now()
        print("เวลา :", current_time)
        ked()
        i=1
        Hitfac=0
        maxhit=0
        statepercent=0
        StateP=0
        ptsmax=0
        while (i <= x):
            main()
            i+=1 
    except ValueError : 
        ked()
        print("รับเฉพาะตัวเลข ไอ้สัสไปพิมมาใหม่")
        ked()
    show()
