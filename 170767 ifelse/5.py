print ("สวัสดีครับ นี่คือโปรเน็นของ ตะดอบอินเตอร์เน็ต 5g","\n*****************************","\nโปรโทร กด 1","\nโปรเน็ต กด 2")
x = int(input("เลือกกด ประเภทแพ๊คที่ท่านใช้ : "))
if x == 1:
    print("****************","เลือกโปรโมชั่นของการโทร","\nแพ๊คโปรโทรทุกเครือข่าย 18 นาที-----> กด 1 ","\nแพ๊คโปรโทรทุกเครือข่าย 60 นาที-----> กด 2 ","\nแพ๊คโปรโทรทุกเครือข่าย 100 นาที-----> กด 3 ")
    tel = int(input("โปรดเลือกแพ๊คที่ท่านต้องการ -----> "))
    if tel == 1: 
        print("****************","\nโทรทุกเครือข่าย 18 นาที","\n9 บาท 1 วัน","\nกด *777*4012#")
    elif tel == 2:
        print("****************","\nโทรทุกเครือข่าย 60 นาที","\n19 บาท 1 วัน","\nกด *777*7078#")
    elif tel == 3:
        print("****************","\nโทรทุกเครือข่าย 100 นาที","\n20 บาท 1 วัน","\nกด *777*246#")
elif x == 2: 
    print("\n***********","\n\nเน็ตและโทรไม่จำกัด ------->กด 1","\nอินเทอร์เน็ต","\nเน็ตไม่จำกัด ความเร็ว 384 kbps","\nโทร","\nโทรฟรีในเครือข่าย AIS ระหว่างเวลา 5:00-17:00 น. (ครั้งละไม่เกิน 60 นาที) พิเศษ ฟรี 10 SMS และ 5 MMS")
    print("\n***********","\n\nเน็ตและโทรไม่จำกัด ------->กด 2","\nอินเทอร์เน็ต","\nเน็ตไม่จำกัด ความเร็ว 512 kbps","\nโทร","\nโทรฟรีในเครือข่าย AIS ระหว่างเวลา 5:00-18:00 น. (ครั้งละไม่เกิน 60 นาที)")
    print("\n***********","\n\nเน็ตและโทรไม่จำกัด ------->กด 3","\nอินเทอร์เน็ต","\nเน็ตไม่จำกัด ความเร็ว 384 kbps","\nโทร","\nโทรฟรีในเครือข่าย AIS ตลอด 24 ชม. (ครั้งละไม่เกิน 60 นาที)")
    print("\n***********","\n\nเน็ตและโทรไม่จำกัด ------->กด 4","\nอินเทอร์เน็ต","\nเน็ตไม่จำกัด ความเร็ว 4Mbps","\nโทร","\nโทรฟรีในเครือข่าย AIS ตลอด 24 ชม. (ครั้งละไม่เกิน 60 นาที)")
    net = int(input("โปรดเลือกกดแพ๊คที่ท่านต้องการ"))
    if net == 1:
        print("\n--------------------------------","\n\nเน็ตและโทรไม่จำกัด","\nอินเทอร์เน็ต","\nเน็ตไม่จำกัด ความเร็ว 384 kbps","\nโทร","\nโทรฟรีในเครือข่าย AIS ระหว่างเวลา 5:00-17:00 น. (ครั้งละไม่เกิน 60 นาที) พิเศษ ฟรี 10 SMS และ 5 MMS","22 บาท 1 วัน","กด รหัส *777*35# โทรออก")
    
    