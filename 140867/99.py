
# รับข้อมูลจากผู้ใช้งาน
num_participants = int(input("กรุณากรอกจำนวนผู้เข้าร่วม : "))
max = float(input('กรุณาคะแนนสูงสุด : '))
participants = []


# วนลูปเพื่อรับข้อมูลผู้เข้าร่วมแต่ละคน
for i in range(num_participants):
    print(f"\nข้อมูลสำหรับผู้เข้าร่วมคนที่ {i + 1}:")
    name = input("ชื่อผู้ซ้อม: ")
    score = int(input("คะแนนที่ได้: "))
    time = float(input("ระยะเวลาที่ใช้ (วินาที): "))   
    hitfactor = score/time
    if hitfactor > hitmax :
        hitmax = hitmax
    statepts = (score*hitfactor)/hitmax
    if statepts > ptsmax :
        ptsmax = statepts
    stateper =  (statepts/ptsmax)*100                                        
    participants.append({'name': name, 'score': score, 'time': time, 'hitfactor': hitfactor, 'statepts':statepts, 'stateper':stateper})
    


# แสดงผลลัพธ์ที่จัดเรียงแล้ว
print("\nผลลัพธ์การซ้อมยิงปืนลูกซอง (เรียงตามคะแนนและเวลา):")
for i, participant in enumerate(participants):
    print(f"อันดับ {i + 1}: {participant['name']} - คะแนน: {participant['score']}, เวลา: {participant['time']} วินาที Hit Factor{participant['hitfactor']} STATE POINTS {participant['statepts']} STATE PERCENT {participant['stateper']}")

