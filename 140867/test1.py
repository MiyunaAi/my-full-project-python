# ฟังก์ชั่นสำหรับแสดงรายการสินค้า
def show_products():
    print("รายการสินค้า:")
    for i, item in enumerate(products, start=1):
        print(f"{i}. {item} - {products[item]} บาท")

# ฟังก์ชั่นสำหรับหยิบสินค้าเข้าตะกร้า
def add_to_cart(cart):
    try:
        product_number = int(input("กรุณาใส่หมายเลขสินค้าที่ต้องการหยิบเข้าตะกร้า: "))
        if 1 <= product_number <= len(products):
            product_name = list(products.keys())[product_number - 1]
            if product_name in cart:
                cart[product_name] += 1
            else:
                cart[product_name] = 1
            print(f"เพิ่ม {product_name} ลงในตะกร้าเรียบร้อยแล้ว")
        else:
            print("หมายเลขสินค้าที่เลือกไม่ถูกต้อง")
    except ValueError:
        print("กรุณาใส่หมายเลขสินค้าเป็นตัวเลข")

# ฟังก์ชั่นสำหรับแสดงจำนวนและราคาของสินค้าที่หยิบทั้งหมด
def show_cart(cart):
    if not cart:   #ถ้า ไม่มี obbject ในcart
        print("ตะกร้าของคุณยังว่างอยู่")
    else:
        print("สินค้าในตะกร้า:")
        total = 0
        for item, quantity in cart.items():
            price = products[item] * quantity
            print(f"{item} - {quantity} ชิ้น - {price} บาท")
            total += price
        print(f"ราคารวมทั้งหมด: {total} บาท")

# ฟังก์ชั่นสำหรับปิดโปรแกรม
def exit_program():
    print("ขอบคุณที่ใช้บริการร้านค้าของเรา!")
    exit()

# รายการสินค้า
products = {
    "ข้าวสาร": 50,
    "น้ำมันพืช": 60,
    "นมกล่อง": 20,
    "น้ำตาล": 30,
    "บะหมี่กึ่งสำเร็จรูป": 10
}

# ตะกร้าสินค้า
cart = {}

# โปรแกรมหลัก
while True:
    print("\nโปรแกรมร้านค้า")
    print("1. แสดงรายการสินค้า")
    print("2. หยิบสินค้าเข้าตะกร้า")
    print("3. แสดงจำนวนและราคาของสินค้าที่หยิบทั้งหมด")
    print("4. ปิดโปรแกรม")

    try:
        choice = int(input("กรุณาเลือกทำรายการ: "))

        if choice == 1:
            show_products()
        elif choice == 2:
            add_to_cart(cart)
        elif choice == 3:
            show_cart(cart)
        elif choice == 4:
            exit_program()
        else:
            print("กรุณาเลือกหมายเลขที่ถูกต้อง")
    except ValueError:
        print("กรุณาใส่หมายเลขเมนูเป็นตัวเลข")
