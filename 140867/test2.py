# โปรแกรมคำนวณผลการซ้อมยิงปืนลูกซอง

def get_participant_data(num_participants):
    """
    ฟังก์ชันสำหรับรับข้อมูลการซ้อมจากผู้ใช้
    """
    participants = []
    for i in range(num_participants):
        print(f"\nกรุณากรอกข้อมูลสำหรับผู้เข้าร่วมคนที่ {i+1}:")
        name = input("ชื่อผู้ซ้อม: ")
        while True:
            try:
                score = float(input("คะแนน: "))
                time = float(input("ระยะเวลาที่ใช้ (วินาที): "))
                if time <= 0:
                    print("ระยะเวลาต้องมากกว่า 0 วินาที กรุณากรอกใหม่.")
                    continue
                break
            except ValueError:
                print("กรุณากรอกตัวเลขที่ถูกต้องสำหรับคะแนนและเวลา.")
        
        participant = {
            'Name': name,
            'Score': score,
            'Time': time,
            'Hit Factor': 0.0,
            'State Points': 0.0,
            'State Percent': 0.0
        }
        participants.append(participant)
    return participants

def calculate_hit_factors(participants):
    """
    ฟังก์ชันสำหรับคำนวณค่า Hit Factor สำหรับผู้เข้าร่วมทุกคน
    """
    for participant in participants:
        participant['Hit Factor'] = participant['Score'] / participant['Time']

def calculate_state_points(participants, max_points=100):
    """
    ฟังก์ชันสำหรับคำนวณค่า State Points และ State Percent สำหรับผู้เข้าร่วมทุกคน
    """
    max_hit_factor = max(participant['Hit Factor'] for participant in participants)
    for participant in participants:
        participant['State Points'] = (participant['Hit Factor'] / max_hit_factor) * max_points
        participant['State Percent'] = (participant['Hit Factor'] / max_hit_factor) * 100

def sort_participants_by_state_percent(participants):
    """
    ฟังก์ชันสำหรับจัดเรียงผู้เข้าร่วมตามค่า State Percent จากมากไปน้อย
    """
    return sorted(participants, key=lambda x: x['State Percent'], reverse=True)

def display_results(participants):
    """
    ฟังก์ชันสำหรับแสดงผลลัพธ์ของการคำนวณ
    """
    print("\nผลการซ้อมยิงปืนลูกซอง:")
    print("{:<5} {:<20} {:<10} {:<10} {:<12} {:<15} {:<15}".format(
        "อันดับ", "ชื่อผู้ซ้อม", "คะแนน", "เวลา(วินาที)", "Hit Factor", "State Points", "State Percent"
    ))
    print("-" * 90)
    for idx, participant in enumerate(participants, start=1):
        print("{:<5} {:<20} {:<10.2f} {:<10.2f} {:<12.2f} {:<15.2f} {:<15.2f}".format(
            idx,
            participant['Name'],
            participant['Score'],
            participant['Time'],
            participant['Hit Factor'],
            participant['State Points'],
            participant['State Percent']
        ))

def main():
    """
    ฟังก์ชันหลักของโปรแกรม
    """
    print("=== โปรแกรมคำนวณผลการซ้อมยิงปืนลูกซอง ===")
    while True:
        try:
            num_participants = int(input("กรุณากรอกจำนวนผู้เข้าร่วม: "))
            if num_participants <= 0:
                print("จำนวนผู้เข้าร่วมต้องมากกว่า 0 กรุณากรอกใหม่.")
                continue
            break
        except ValueError:
            print("กรุณากรอกตัวเลขที่ถูกต้องสำหรับจำนวนผู้เข้าร่วม.")
    
    participants = get_participant_data(num_participants)
    calculate_hit_factors(participants)
    calculate_state_points(participants)
    sorted_participants = sort_participants_by_state_percent(participants)
    display_results(sorted_participants)

if __name__ == "__main__":
    main()
