def intro (name, *hobby, **address) :
     print("Hello i am "+name+".")
     print("My address : ")
     for kw in address : 
          print(kw + ":" + address [kw])    
     print("My hobby : ")
     for arg in hobby :
          print(arg)

intro("Bob","Sport","Music","Game","tur",province = "sisaket",nation = "Thailand",district = "Tadob")