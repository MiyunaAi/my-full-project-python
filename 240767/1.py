print("ป้อนชื่ออาหารสุดโปรดของคุณ หรือ exit เพื่อออกจากโปรแกรม")
i = 1 
menu = []
while (True):
    x = input("pls enter food " + str(i) + 'คือ : ')
    if x == "exit":
        break 
    menu.append(x)
    i += 1 
print("อาหารสุดโปรดของคุณมีดังนี้ ",menu)
    
        