class nisit :
    def __init__(self,name,year,major,sex) :
        self.name = name
        self.year = year
        self.major = major
        self.sex = sex
    def showbob(self) :
        print("--------------------------------","\nLhin Infomation","\n--------------------------------")
        print("name :", self.name)
        print("YearClass :", self.year)
        print("Major :", self.major)
        print("Sex :", self.sex)

x = nisit('name','year','major','sex')
print('Welcome to Lhin infomation',"\n--------------------------------")
b = input("pls enter name : ")
x.name = b

c = input("pls enter year : ")
x.year = c

d = input("pls enter major : ")
x.major = d

e = input("pls enter sex : ")
x.sex = e


x.showbob()
                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          