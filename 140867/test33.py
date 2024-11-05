llist = {}
print("ยินดีต้อนรับ สู่หลินปิงปืนเซนเตอร์")
x=int(input("จำนวนคน : "))
from datetime import datetime
current_time = datetime.now()
print("เวลา :", current_time)
print("-------------------------------")
i=1
maxhit=0
statepercent=0
StateP=0
ptsmax=0
def main():
    global llist,maxhit,ptsmax
    name = input("ชื่อ : ")
    score = int(input("คะแนน : "))
    time= int(input("เวลา : "))
    HitFac=score/time

    if HitFac>maxhit :
        maxhit=HitFac
    StateP=(score*HitFac)/maxhit
    if StateP>ptsmax :
        ptsmax = StateP
    statepercent=(StateP/ptsmax)*100
    llist[name] = score,time,HitFac,StateP,statepercent
def show():
    print("-----------------------------------------------------------------")
    print("{0: <15}{1: <15}{2: <15}{3: <15}{4: <15}{5: <15}".format("ชื่อ","คะแนน","เวลา","HIT_FAC","STATE_POINT","STATE_PERCENT"))
    for key,(score,time,HitFac,StateP,statepercent) in llist.items():
        print("{0: <15}{1: <15}{2: <15}{3: <15}{4: <15}{5: <15}".format(key,score,time,HitFac,StateP,statepercent))
while (i <= x):
    main()
    i+=1 
show()
