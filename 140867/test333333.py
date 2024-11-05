def calculate_hitfac(score, time):
    return score / time

def calculate_statep(score, hitfac, maxhit):
    return (score * hitfac) / maxhit

def calculate_statepercent(statep, ptsmax):
    return (statep / ptsmax) * 100

def main():
    participants = []
    
    # รับจำนวนผู้เข้าร่วม
    num_participants = int(input("จำนวนผู้เข้าร่วม: "))
    
    # วนรับข้อมูลผู้เข้าร่วม
    for i in range(num_participants):
        print(f"\nข้อมูลของผู้เข้าร่วมคนที่ {i+1}:")
        name = input("ชื่อ: ")
        score = int(input("คะแนน: "))
        time = int(input("เวลา: "))
        
        # คำนวณ HitFac
        hitfac = calculate_hitfac(score, time)
        
        # เก็บข้อมูลผู้เข้าร่วมใน dictionary
        participant = {
            'name': name,
            'score': score,
            'time': time,
            'hitfac': hitfac,
            'statep': 0,        # ค่า statep จะถูกคำนวณในภายหลัง
            'statepercent': 0    # ค่า statepercent จะถูกคำนวณในภายหลัง
        }
        participants.append(participant)
    
    # หาค่าสูงสุดของ HitFac
    maxhit = max([p['hitfac'] for p in participants])
    
    # วนคำนวณ StateP และหาค่าสูงสุดของ StateP
    for participant in participants:
        participant['statep'] = calculate_statep(participant['score'], participant['hitfac'], maxhit)
    ptsmax = max([p['statep'] for p in participants])
    
    # วนคำนวณ StatePercent
    for participant in participants:
        participant['statepercent'] = calculate_statepercent(participant['statep'], ptsmax)
    
    # จัดเรียงผู้เข้าร่วมตาม StatePercent จากมากไปน้อย
    participants.sort(key=lambda x: x['statepercent'], reverse=True)
    
    # แสดงผลลัพธ์
    print("\nผลลัพธ์การซ้อมยิงปืนลูกซอง:")
    print("{0: <15}{1: <10}{2: <10}{3: <10}{4: <10}{5: <15}".format("ชื่อ", "คะแนน", "เวลา", "HitFac", "StateP", "StatePercent"))
    for participant in participants:
        print("{0: <15}{1: <10}{2: <10}{3: <10.2f}{4: <10.2f}{5: <15.2f}".format(
            participant['name'], 
            participant['score'], 
            participant['time'], 
            participant['hitfac'], 
            participant['statep'], 
            participant['statepercent']
        ))

if __name__ == "__main__":
    main()
