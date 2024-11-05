import sqlite3
conn = sqlite3.connect (r"C:\Users\xenos\Documents\dat\example.db")
c = conn.cursor()
try :
        data= ('ABC','kuay','zzz@gmail.com','4')
        c.execute('''UPDATE users SET fname =?,lname =?,email =? WHERE id = ? ''',data)
        conn.commit()
        c.close()

except sqlite3.Error as e:
        print('faile to insert : ',e)
finally :
    if conn :
        conn.close()