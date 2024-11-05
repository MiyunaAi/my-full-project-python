class car :
    def __init__(self,name,color):
        self.name = name
        self.color = color

    def showcar(self) :
        print("infomation : name =",self.name,",Color=",self.color)

class newcar(car):
    def __init__(self,name,color,gear) :
#       car.__init__(self,name,color) 
        super().__init__(name,color)     #ใช้super ในการสืบทอด
        self.gear = gear  #เพิ่มpropertieให้ child class
    def showcar2(self):
        print(self.name,self.color,self.gear)

x = newcar("lamborghini","chocky pink","kapook") #addเพิ่มkapok
#x.showcar()
x.showcar2()
#print(x.gear)      