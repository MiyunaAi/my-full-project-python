List=[]
i=1
print('Lhin Spa and Hotel','\n----------------------------')
while(True):
    x = input("\nเพิ่มรายการหมอนวด [a] \nแสดงข้อมูลหมอนวดที่ท่านเลือก [b] \nออกจากระบบ [c] \n-----------------------\nเลือกอะไรจ๊ะเบบี๊ : ")
    if x == "a":
        info = input("ป้อนรายการลูกค้า (รหัสเบอร์คนนวดที่ท่านต้องการ : ชื่อคนนวดที่ท่านต้องการ : เบอร์สมาชิกของท่าน)  ")
        List.append(info)
        print("*********เพิ่มรายการเข้าสู่ระบบเรียบร้อย*********")
        print("----------------------")
    if x == "b":
        print("รหัสเบอร์คนนวดที่ท่านต้องการ------ชื่อคนนวด------เบอร์สมาชิกของท่าน")
        for i in List:
            print(i)
        print("----------------------")
    if x == "c":
        y = input("ต้องการออกจากโปรแกรมหรือไม่? yes/no : ")
        print("---------------------------------Thank you -----------------------------------")
        if y =="yes":
            break