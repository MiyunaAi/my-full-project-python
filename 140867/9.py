

# ฟังก์ชันเพื่อจัดเรียงผลลัพธ์
def sort_results(participants):
    return sorted(participants, key=lambda x: (-x['score'], x['time']))

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
    statepts = (score*hitfactor)/max
    stateper0 = score/100
    stateper =  statepts/stateper0                                             
    participants.append({'name': name, 'score': score, 'time': time, 'hitfactor': hitfactor, 'statepts':statepts, 'stateper':stateper})
    
# จัดเรียงผลลัพธ์ตามคะแนนและเวลา
sorted_participants = sort_results(participants)

# แสดงผลลัพธ์ที่จัดเรียงแล้ว
print("\nผลลัพธ์การซ้อมยิงปืนลูกซอง (เรียงตามคะแนนและเวลา):")
for i, participant in enumerate(sorted_participants):
    print(f"อันดับ {i + 1}: {participant['name']} - คะแนน: {participant['score']}, เวลา: {participant['time']} วินาที Hit Factor{participant['hitfactor']} STATE POINTS {participant['statepts']} STATE PERCENT {participant['stateper']}")

