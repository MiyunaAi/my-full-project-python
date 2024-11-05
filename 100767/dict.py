"""thisdict = {
    "fname" : "Thatanon",
    "lname" : "Thumaud",
    "years" : 2004
}
x = thisdict["fname"] = 2020
print(thisdict)"""


"""thisdict = {
    "fname" : "Thatanon",
    "lname" : "Thumaud",
    "years" : 2004
}

thisdict["nation"] = "thai"             #add keyใหม่ก assign
thisdict["Tel"] =  "0958620453"         #addphone 
print(thisdict)"""


thisdict = {
    "fname" : "Thatanon",
    "lname" : "Thumaud",
    "years" : 2004,                               
    "nation": "Thai"
}

thisdict.pop("years")          #ลบข้อมูลที่ต้องการตัวอย่างคือ year
thisdict.popitem()          #ลบข้อมูลที่เพิ่มล่าสุด
print(thisdict)
#del thisdict"""
