print("เลือกเมนูเพื่อทำรายการค่าผ่านทาง ตม เกาหลี","\n     #######################","\n        กด 1 เลือกเหมาจ่าย","\n        กด 2 เลือกจ่ายเพิ่ม")
x = int(input("เลือกกด : "))
y = int(input("กรุณากรอก ระยะทางที่ท่านจะเดินทาง : "))
if x == 2 :
    if y <= 25 :
        print("ค่าใช้จ่ายทั้งหมด = 25 บาท")
    else :
        print("ค่าใช้จ่ายทั้งหมด = 80 บาท")
elif x == 1 :
    if y <= 25 :
        print("ค่าใช้จ่ายทั้งหมด = 25 บาท")
    else :
        print("ค่าใช้จ่ายทั้งหมด 55 บาท")
print("###########################","\n------ขอบคุณที่ใช้บริการครับ------")
