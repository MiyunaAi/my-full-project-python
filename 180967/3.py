class Car :
    def __init__(self,name,color,human) :
        self.name = input("pls enter ")
        self.color = color
        self.human = human
    def showCar(self) :
        print("CaR Infomation")
        print("name :", self.name)
        print("color :", self.color)

x = Car("Lambogini","red","pae")
x.showCar()