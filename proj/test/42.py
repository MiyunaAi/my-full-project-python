import tkinter as tk
from tkinter import messagebox
import qrcode
import crcmod
from PIL import Image, ImageTk

def calculate_crc(payload):
    crc16 = crcmod.mkCrcFun(0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)
    crc = crc16(bytes(payload, 'utf-8'))
    return f"{crc:04X}"

def generate_qr():
    try:
        amount = float(amount_entry.get())
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        
        promptpay_id = "0958620453"
        formatted_promptpay_id = "0066" + promptpay_id[1:]  # เปลี่ยน 0 เริ่มต้นเป็น 0066

        # สร้าง payload สำหรับพร้อมเพย์ตามมาตรฐาน PromptPay
        payload = (
            "000201"                  # Payload Format Indicator
            "010212"                  # Point of Initiation Method
            "29370016A000000677010111"  # Application ID สำหรับ PromptPay
            f"01130066{formatted_promptpay_id}"  # PromptPay ID แบบเบอร์โทร
            "5802TH"                  # ประเทศไทย
            "5303764"                 # รหัสสกุลเงินบาท (764)
        )

        # เพิ่มจำนวนเงิน ถ้ามี
        if amount > 0:
            amount_str = f"{amount:.2f}".replace(".", "")  # เอาจุดทศนิยมออก
            payload += f"54{len(amount_str):02d}{amount_str}"

        # เพิ่ม CRC
        payload += "6304"
        crc = calculate_crc(payload)
        qr_string = payload + crc

        # สร้าง QR Code
        qr = qrcode.make(qr_string)
        qr = qr.resize((200, 200))  # ปรับขนาด QR Code
        qr_img = ImageTk.PhotoImage(qr)

        # อัพเดต QR Code ใน GUI
        qr_label.config(image=qr_img)
        qr_label.image = qr_img

    except ValueError:
        messagebox.showerror("Error", "กรุณาใส่จำนวนเงินที่ถูกต้อง")

app = tk.Tk()
app.title("QR PromptPay Generator")
app.geometry("300x400")

amount_label = tk.Label(app, text="จำนวนเงิน (บาท):")
amount_label.pack(pady=10)

amount_entry = tk.Entry(app)
amount_entry.pack(pady=10)

generate_btn = tk.Button(app, text="สร้าง QR Code", command=generate_qr)
generate_btn.pack(pady=20)

qr_label = tk.Label(app)
qr_label.pack(pady=10)

app.mainloop()
