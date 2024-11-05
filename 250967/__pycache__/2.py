import sqlite3
def insertTousers (fname,lname,email) :
    try :
        conn = sqlite3.connect (r"C:\Users\xenos\Documents\dat\example.db")
        c = conn.cursor()

        sql = '''INSERT INTO users (fname,lname,email) VALUES (?,?,?) '''
        data = (fname,lname,email)
        c.execute(sql,data)
        conn.commit()

        c.close()

    except sqlite3.Error as e:
        print('faile to insert : ',e)
    finally :
        if conn :
            conn.close()
insertTousers('Guido','Rossum','Pythonbob@gmail.com')
insertTousers('zetomaru','hagtagon','gnail@gmail.com')