import sqlite3 
#print(sqlite3.sqlite_version)
conn = sqlite3.connect (r"C:\Users\xenos\Documents\dat\example.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fname VARCHAR(30) NOT NULL,
                lname VARCHAR(30) NOT NULL,
                email VARCHAR(100) NOT NULL
            )''')
c.execute('''INSERT INTO users (id,fname,lname,email) VALUES (NULL,"BOB","BEn","Bobbyemailcom")''')
c.execute('''INSERT INTO users VALUES (NULL,"Bb","Bb","Bb")''')
c.execute('''INSERT INTO users VALUES (NULL,"Thatanon","Thumaud","thatanon.t@kkumail.com")''')
           
conn.commit()
 
conn.close()