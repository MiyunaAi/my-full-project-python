cart = {}

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

add_to_cart(cart)

