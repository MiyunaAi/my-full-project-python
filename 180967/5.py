class Car :
    def __init__(self,name,color) :
        self.name = name
        self.color = color

    def showCar(self) :
        print("CaR Infomation")
        print("name :", self.name)
        print("color :", self.color)

#Mustang = Car("Mustang","Yellow")
#bob = Car("ควยดวง",'ควยนุ')
#Mustang.color = "black"
#Mustang.showCar()
#bob.showCar()

mustang = Car("Mustang","red")
del mustang.color

print(mustang,color)