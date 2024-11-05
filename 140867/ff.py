# กำหนดตัวแปร global
x = 0

def calculate():
    global x  # บอกว่าเราต้องการใช้ตัวแปร x ที่อยู่ภายนอกฟังก์ชัน
    int(input("pls enter num : "))
    for x # แก้ไขตัวแปร x

# เรียกใช้ฟังก์ชัน
calculate()

# ดูผลลัพธ์ของตัวแปร x หลังจากการคำนวณ
print(x)  # ผลลัพธ์จะเป็น 15
