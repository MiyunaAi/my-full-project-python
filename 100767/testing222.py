print ("โปรแกรมคำนวณค่าผ่านทางมอเตอร์เวย์\n------------------------------\nรถยนต์ 4 ล้อ               กด 1\nรถยนต์ 6 ล้อ               กด 2\nรถยนต์มากกว่า 6 ล้อ         กด 3")
cardic = {
"1" : "ลาดกระบัง-->บางบ่อ...25...บาท\nลาดกระบัง-->บางประกง...30...บาท\nลาดกระบัง-->พนัสนิคม...45...บาท\nลาดกระบัง-->บ้านบึง...55...บาท\nลาดกระบัง-->บางพระ...60...บาท",
"2" : "ลาดกระบัง-->บางบ่อ...45...บาท\nลาดกระบัง-->บางประกง...45...บาท\nลาดกระบัง-->พนัสนิคม...75...บาท\nลาดกระบัง-->บ้านบึง...90...บาท\nลาดกระบัง-->บางพระ...100...บาท\n",
"3" : "ลาดกระบัง-->บางบ่อ...60...บาท\nลาดกระบัง-->บางประกง...70...บาท\nลาดกระบัง-->พนัสนิคม...110...บาท\nลาดกระบัง-->บ้านบึง...130...บาท\nลาดกระบัง-->บางพระ...140...บาท\n"}
choose = int(input("เลือกประเภทยานพาหนะ : "))
bob = cardic["1"]
if choose == 1:print("*********ค่าบริการรถ 4 ล้อ คือ*********"),print(bob)
bob1 = cardic["2"]
if choose == 2:print("*********ค่าบริการรถ 6 ล้อ คือ*********"),print(bob1)
bob2 = cardic["3"]
if choose == 3:print("*********ค่าบริการรถมากกว่า 6 ล้อ คือ*********"),print(bob2)