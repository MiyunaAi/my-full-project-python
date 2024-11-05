# สร้างคลาสร้านค้า
class Shop:
    def __init__(self, shop_name):
        self.shop_name = shop_name  
        self.products = {}  

    def input_product(self):
        product_name = input("กรุณากรอกชื่อสินค้า: ")
        price = float(input("กรุณากรอกราคาสินค้า: "))
        quantity = int(input("กรุณากรอกจำนวนสินค้า: "))
        self.add_product(product_name, price, quantity)

    def display_products(self):
        if self.products:
            print(f"\nรายการสินค้าของร้าน {self.shop_name}:")
            for product_name, details in self.products.items():
                print(f"- {product_name} : ราคา {details['price']} บาท , จำนวน {details['quantity']} ชิ้น")
        else:
            print(f"\nร้าน {self.shop_name} ไม่มีสินค้าจำหน่ายในขณะนี้")

    def add_product(self, product_name, price, quantity):
        if product_name in self.products:
            self.products[product_name]['quantity'] += quantity
            print(f"เพิ่มสินค้า {product_name} จำนวน {quantity} ชิ้น เข้าสู่ร้าน")
        else:
            self.products[product_name] = {'price': price, 'quantity': quantity}
            print(f"เพิ่มสินค้าใหม่ {product_name} เข้าสู่ร้าน")

    def remove_product(self, product_name):
        if product_name in self.products:
            del self.products[product_name]
            print(f"ลบสินค้า {product_name} ออกจากร้าน")
        else:
            print(f"ไม่พบสินค้า {product_name} ในร้าน")

shop_name = input("กรุณากรอกชื่อร้าน: ")
my_shop = Shop(shop_name)

while True:
    print("\nกรุณาเลือกเมนู:")
    print("1. แสดงรายการสินค้า")
    print("2. เพิ่มรายการสินค้า")
    print("3. ลบรายการสินค้า")
    print("4. ออกจากโปรแกรม")
    print("----------------------")
    
    choice = input("กรุณาเลือกหมายเลขเมนู: ")
    
    if choice == "1":
        my_shop.display_products()
    elif choice == "2":
        my_shop.input_product()
    elif choice == "3":
        product_name = input("กรุณากรอกชื่อสินค้าที่ต้องการลบ: ")
        my_shop.remove_product(product_name)
    elif choice == "4":
        bb = input("ออกจากโปรแกรมหรือไม่ y/n : ")
        if bb == 'y' :
            break
    else:
        print("กรุณาเลือกเมนูที่ถูกต้อง")
