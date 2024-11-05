class Nisit:
    def __init__(self, name, year, major, sex):
        self.name = name
        self.year = year
        self.major = major
        self.sex = sex

    def show_info(self):
        print("--------------------------------")
        print("Lhin Information")
        print("--------------------------------")
        if sex == 'male' :
            print("สวัสดีครับ")
        else:
            print("สวัสดีค่ะ")
        print("Name :", self.name)
        print("Year Class :", self.year)
        print("Major :", self.major)
        print("Sex :", self.sex)


student = Nisit('name', 'year', 'major', 'sex')
print('Welcome to Lhin Information', "\n--------------------------------")

student.name = input("Please enter name: ")
student.year = input("Please enter year: ")
student.major = input("Please enter major: ")
student.sex = input("Please enter sex: ")

student.show_info()
