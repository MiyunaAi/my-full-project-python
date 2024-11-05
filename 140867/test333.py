def ked():
    print("-----------------------------------------------------------------------------------")
def main():
    global llist,maxhit,ptsmax
    name = input("ชื่อ : ")
    score = int(input("คะแนน : "))
    time= int(input("เวลา : "))
    ked()
    HitFac=score/time

    if HitFac>maxhit :
        maxhit=HitFac
    StateP=(score*HitFac)/maxhit
    if StateP>ptsmax :
        ptsmax = StateP
    statepercent=(StateP/ptsmax)*100
    llist[name] = score,time,HitFac,StateP,statepercent
def show():
    ked()
    print("{0: <15}{1: <15}{2: <15}{3: <15}{4: <15}{5: <15}".format("ชื่อ","คะแนน","เวลา","HIT_FAC","STATE_POINT","STATE_PERCENT"))
    for name,(score,time,HitFac,StateP,statepercent) in llist.items():
        print("{0: <15}{1: <15}{2: <15}{3: <15}{4: <15}{5: <15}".format(name,score,time,HitFac,StateP,statepercent))
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
        maxhit=0
        statepercent=0
        StateP=0
        ptsmax=0
        while (i <= x):
            main()
            i+=1 
        show()
    except ValueError : 
        ked()
        print("รับเฉพาะตัวเลข ไอ้สัสไปพิมมาใหม่")
        ked()

