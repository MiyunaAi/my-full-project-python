#thislist =  ["msu", "ku", "psu","cmu" ,"tu", "cu","kku","ubu","bu","swu"]
#print(thislist[-3])

#thislist = ["Com", "ED", "KKU",99] #ระบุจุด index 1นับ สิ้นสุด3 ไม่นับจ้า
#print(thislist[1:3])

#thislist = ["Com", "ED", "KKU",99]
#print(thislist[:3])

#thislist = ["Com", "ED", "KKU",99]
#print(thislist[1:])

#thislist = ["Com", "ED", "KKU",99]
#print(thislist)
#thislist[0] = "ComED"                       #เปลี่ยนค่าตามตำแหน่งที่ต้องการอย่างตัวอย่างคือตำแหน่งที่0 
#print(thislist)
#thislist[3] = 98                             #เปลี่ยนค่าตามตำแหน่งที่ต้องการอย่างตัวอย่างคือตำแหน่งที่3
#print(thislist)


#thislist = ["Com", "ED", "KKU", 59]
#thislist.append("hello mommy")                 #appendเอาข้อมูลไปต่อในลิสท้ายขวาสุด
#print(thislist)

#thislist = ["Com", "ED", "KKU", 99]
#thislist.insert(1,"Lamyai")                 #insertเอาข้อมูลไปต่อในลิสที่ต้องการ
#print(thislist)

#thislist = ["Com", "ED", "KKU", 99]
#thislist.remove("Com")                   #removeลบข้อมูลในลิสที่ต้องการ
#print(thislist)

#thislist = ["Com", "ED", "KKU", 99]
#thislist.pop()                           #popลบข้อมูลท้ายสุด
#print(thislist)

#thislist = ["Com", "ED", "KKU", 99]
#del thislist[3]                          #Delลบลิสที่ต้องการ ถ้าไม่ใส่[]จะลบลิสหมดจ้า

#thislist = ["Com", "ED", "KKU", 99]
#thislist.clear()                         #clearทำให้ค่าในลิสเป็นค่าล่าง
#print(thislist)

#mommytuple = ("Com", "ED", "KKU")         #tuple เป็นคอลลเลคชั่นเรียงลำกดับข้อมูลเรียง ไม่สามารถแก้ไข้ข้อมูลได้
#print(mommytuple)       



#mommytuple = ("Com", "ED", "KKU")        
#print(mommytuple[1])
#mommytuple = ("Com", "ED", "KKU")        #indexคือสิ่งที่ต้องการ อยู่ใน []
#print(mommytuple[-1])
#mommytuple = ("Com", "ED", "KKU")        
#print(mommytuple[0:1])


#x = ("Com", "ED", "KKU")
#y = list(x)
#y[0] = "ComED"              #เปลี่ยนข้อมูลเฉยๆ
#x = tuple(y)
#print(x)


#x = ("Com", "ED", "KKU")
#del x 
#print(x)

#thisset = {"Com", "ED", "KKU","KKU"}           #เปลี่ยนข้อมูลไม่ได้แต่แอดได้แต่ตำแหน่งมันสุ่มที่เก็บนะ
#print(thisset)

#thisset = {"Com", "ED", "KKU","KKU",}
#for x in thisset: 
    #print(x)

#thisset = {"Com", "ED", "KKU"}
#thisset.add("Hello")
#print(thisset)
#thisset.update(["I", "Am", "Batman"])           #แอดข้อมูล
#print(thisset)


#thisset = {"Com", "ED", "KKU"} #{"Com", "ED", "KKU"}
#thisset.remove("Com") #{ "ED", "KKU"}
#thisset.discard("ED") #{ED , KKU}
#thisset.clear() #{}
#del thisset #delete
