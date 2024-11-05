# ฟังก์ชั่นแสดงเมนูคำสั่ง
def show_menu():
    print("\nDictionary Program")
    print("1. เพิ่มคำ")
    print("2. ลบคำ")
    print("3. แสดงคำ")
    print("4. ออก")

# ฟังก์ชั่นเพิ่มคำศัพท์
def add_word(dictionary):
    word = input("Enter the word: ")
    word_type = input("กรุณาเลือกประเภทของคำ ( คำนาม, กริยา, คำคุณศัพท์): ")
    meaning = input("กรุณาพิมพ์ ความหมายของคำที่ท่านพิมพ์: ")
    
    if word not in dictionary:
        dictionary[word] = {"type": word_type, "meaning": meaning}
        print(f"Word '{word}' added successfully!")
    else:
        print(f"The word '{word}' already exists in the dictionary.")

# ฟังก์ชั่นลบคำศัพท์
def remove_word(dictionary):
    word = input("Enter the word to remove: ")
    if word in dictionary:
        del(dictionary[word])
        print("Word '{word}' removed successfully!")
    else:
        print("The word '{word}' does not exist in the dictionary.")

# ฟังก์ชั่นแสดงคำศัพท์ทั้งหมด
def show_all_words(dictionary):
    if dictionary:
        print(f"\nWords in the dictionary:")
        for word, details in dictionary.items():
            print(f"{word} ({details['type']}): {details['meaning']}")
    else:
        print("The dictionary is empty.")

# โปรแกรมหลักๆครับพี่ชาย
def main():
    dictionary = {}
    while True:
        show_menu()
        choice = input("เลือกอะไรดีตีครับ: ")
        
        if choice == '1':
            add_word(dictionary)
        elif choice == '2':
            remove_word(dictionary)
        elif choice == '3':
            show_all_words(dictionary)
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")

# เริ่มโปรแกรมจ้าทิด

main()