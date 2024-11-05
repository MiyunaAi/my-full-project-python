
class Nisit:
    def __init__(self, first_name, last_name, year, major, gender):
        self.first_name = first_name  
        self.last_name = last_name  
        self.year = year  
        self.major = major  
        self.gender = gender  
    
    def introduce(self):
        print(f"สวัสดีครับ/ค่ะ ฉันชื่อ {self.first_name} {self.last_name}")
        print(f"ฉันเรียนอยู่ปี {self.year}, สาขา {self.major}")
        print(f"เพศ {self.gender}")


first_name = input("กรุณากรอกชื่อ: ")
last_name = input("กรุณากรอกนามสกุล: ")
year = int(input("กรุณากรอกชั้นปี: "))
major = input("กรุณากรอกสาขา: ")
gender = input("กรุณากรอกเพศ: ")


student = Nisit(first_name, last_name, year, major, gender)

# method 
student.introduce()
