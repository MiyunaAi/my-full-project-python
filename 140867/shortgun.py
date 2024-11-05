def calculate_hitfac(score, time):
    return score / time

def calculate_statep(score, hitfac, maxhit):
    return (score * hitfac) / maxhit

def calculate_statepercent(statep, ptsmax):
    return (statep / ptsmax) * 100

def main():
    participants = []
    print("ยินดีต้อนรับสู่ หลินปิงฮันเตอร์")
    num_participants = int(input("จำนวนผู้เข้าร่วม: "))
    
    for i in range(num_participants):
        print(f"\nข้อมูลของผู้เข้าร่วมคนที่ {i+1}:")
        name = input("ชื่อ: ")
        score = int(input("คะแนน: "))
        time = int(input("เวลา: "))
        
        hitfac = calculate_hitfac(score, time)
        
        participant = {
            'name': name,
            'score': score,
            'time': time,
            'hitfac': hitfac,
            'statep': 0,        
            'statepercent': 0    
        }
        participants.append(participant)
    

    maxhit = max([p['hitfac'] for p in participants])
    

    for participant in participants:
        participant['statep'] = calculate_statep(participant['score'], participant['hitfac'], maxhit)
    ptsmax = max([p['statep'] for p in participants])
    
    for participant in participants:
        participant['statepercent'] = calculate_statepercent(participant['statep'], ptsmax)
    
    participants.sort(key=lambda x: x['statepercent'], reverse=True)
    
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

main()
