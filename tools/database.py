import sqlite3 as sql

def init_tweet_table(username):
    conn = sql.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS '+username+' (ID integer primary key AUTOINCREMENT, Content TEXT, Label TEXT, Date Date, Score TEXT)')
    conn.close()

def init_public_table():
    conn = sql.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS public_tweet (ID integer primary key AUTOINCREMENT, Content TEXT, Label TEXT, Date Date, Score TEXT)')
    print("init table")
    conn.close()

def check_username(username):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        try:
            cnt = cur.execute("SELECT count(*) FROM users  WHERE Username= (?)",(username, ))
            res = cnt.fetchone()
        except TypeError:
            print("did not find it")
            pass
        return res[0]

def check_email(username):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        try:
            cnt = cur.execute("SELECT count(*) FROM users  WHERE Email= (?)",(username, ))
            res = cnt.fetchone()
        except TypeError:
            print("did not find it")
            pass
        return res[0]

def insert_into_sql(username,content,label,date,score):
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO "+username+" (Content,Label,Date,Score) VALUES (?,?,?,?)", ( content, label, date, score))
            con.commit()
            msg = "Record successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"
    finally:
        print(msg)
        con.close()

def insert_into_public(content,label,date,score):
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO public_tweet (Content,Label,Date,Score) VALUES (?,?,?,?)", (content, label, date, score))
            con.commit()
            msg = "Record successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"
    finally:
        print(msg)
        con.close()

def write_to_public(content,label,date,score):
    init_public_table()
    insert_into_public(content,label,date,score)

def write_user_to_database(user_info_list):
    conn = sql.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (ID integer primary key AUTOINCREMENT, Username TEXT, Email TEXT, Password TEXT)')
    Username = user_info_list[0]
    Email = user_info_list[1]
    Password = user_info_list[2]
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (Username,Email,Password) VALUES (?,?,?)", (Username, Email, Password))
            con.commit()
            msg = "User Record successfully added"
    except:
        con.rollback()
        msg = "error in User insert operation"
    finally:
        print(msg)
        con.close()
    conn.close()

def find_user_in_database(emailInput, pswInput):
    conn = sql.connect('database.db')
    userInfo = []
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE Email = (?) AND Password = (?)",(emailInput,pswInput))
        try:
            userInfo = cur.fetchone()
        except TypeError:
            print("did not find it")
            pass
    conn.close()
    return userInfo