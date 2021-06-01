import csv
from datetime import date, datetime
import sqlite3 as sql

def get_date():
    today = date.today()
    return today.strftime("%Y-%m-%d")

def send_help_database_admin(username):
    prefix = "help"
    conn = sql.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS admin (ID integer primary key AUTOINCREMENT,tID TEXT, Username TEXT, Content TEXT, Label TEXT)')
    #get the latest tweet
    latest = []
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM "+username+" ORDER BY ID DESC LIMIT 1")
        try:
            latest = cur.fetchone()
        except TypeError:
            print("did not find it")
            pass
    #save new label to the user
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE " + username + " SET label = (?) WHERE id =(?) ", (prefix,latest[0]))
            con.commit()
            msg = "User Record successfully updated"
    except:
        con.rollback()
        msg = "error in User update operation"
    finally:
        print(msg)
        con.close()
    #save this tweet info to admin
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO admin (tID,Username,Content,Label) VALUES (?,?,?,?)", (latest[0],username, latest[1],latest[2]))
            con.commit()
            msg = "User Record successfully added"
    except:
        con.rollback()
        msg = "error in User insert operation"
    finally:
        print(msg)
        con.close()
    conn.close()
    return latest

def confirm_tweet_sql(username):
    prefix = "con_"
    latest = []
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM "+username+" ORDER BY ID DESC LIMIT 1")
        try:
            latest = cur.fetchone()
        except TypeError:
            print("did not find it")
            pass
    new_label =prefix + (latest[2].split("_"))[1]
    print(latest)
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE " + username + " SET label = (?) WHERE id =(?) ", (new_label,latest[0]))
            con.commit()
            msg = "User Record successfully added"
    except:
        con.rollback()
        msg = "error in User insert operation"
    finally:
        print(msg)
        con.close()

def deny_tweet_sql(username):
    prefix = "con_"
    latest = []
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM " + username + " ORDER BY ID DESC LIMIT 1")
        try:
            latest = cur.fetchone()
        except TypeError:
            print("did not find it")
            pass
    reverse = (latest[2].split("_"))[1]
    if reverse == "benign":
        newAffix = "spam"
    elif reverse =="spam":
        newAffix = "benign"
    new_label = prefix + newAffix
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE " + username + " SET label = (?) WHERE id =(?) ", (new_label, latest[0]))
            con.commit()
            msg = "User Record successfully added"
    except:
        con.rollback()
        msg = "error in User insert operation"
    finally:
        print(msg)
        con.close()

def find_user_information_database(usrname):
    if usrname:
        spam_cnt = get_spam_cnt(usrname)
        benign_cnt = get_benign_cnt(usrname)
        time_cnt = get_time_cnt(usrname)
        total_num = spam_cnt+benign_cnt
        last_ten = get_past_ten_database(usrname)
        data = {
            "name" : usrname,
            "spam_cnt": spam_cnt,
            "benign_cnt": benign_cnt,
            "time_cnt" : time_cnt,
            "total_num": total_num,
            "last_ten": last_ten
        }
        return data

def get_spam_cnt(usrname):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        try:
            cnt = cur.execute("SELECT count(*) FROM "+usrname+" WHERE Label LIKE '%spam'")
            res = cnt.fetchone()
        except TypeError:
            print("did not find it")
            pass
        return res[0]

def get_spam_cnt_between(usrname, startDate,endDate):
    # tDate = datetime(2021, 3, 10).strftime("%Y-%m-%d")
    with sql.connect("database.db") as con:
        cur = con.cursor()
        try:
            cnt = cur.execute("SELECT count(*) FROM "+usrname+" WHERE Label LIKE '%spam' AND (Date BETWEEN (?) AND (?)) ",(startDate,endDate))
            res = cnt.fetchone()
            print(res[0])
        except TypeError:
            print("did not find it")
            pass
        return res[0]

def updateDB(usrname):
    tDate = datetime(2021, 5, 2).strftime("%Y-%m-%d")
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE " + usrname + " SET Date = (?) WHERE id BETWEEN 513 AND 525 ", (tDate,))
            con.commit()
    except:
        con.rollback()
    finally:
        con.close()

def get_benign_cnt_between(usrname, startDate,endDate):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        try:
            cnt = cur.execute("SELECT count(*) FROM "+usrname+" WHERE Label LIKE '%benign' AND (Date BETWEEN (?) AND (?)) ",(startDate,endDate))
            res = cnt.fetchone()
            print(res[0])
        except TypeError:
            print("did not find it")
            pass
        return res[0]

def time_formatter(date):
    date_list  = date.split("-")
    year = date_list[0]
    month = date_list[1]
    day = date_list[2]
    return month+"-"+day+"-"+year

def get_tweets_between(usrname, startDate,endDate):
    list = []
    with sql.connect("database.db") as con:
        cur = con.cursor()
        try:
            cur.execute("SELECT Label,Date,Content FROM "+usrname+" WHERE Date BETWEEN (?) AND (?) ",(startDate,endDate))
            for row in cur:
                new_date = time_formatter(row[1])
                t = (row[0], new_date, row[2])
                list.append(t)
        except TypeError:
            print("did not find it")
            pass
        return list

def get_benign_cnt(usrname):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        try:
            cnt = cur.execute("SELECT count(*) FROM "+usrname+" WHERE Label LIKE '%benign'")
            res = cnt.fetchone()
        except TypeError:
            print("did not find it")
            pass
        return res[0]

def get_total_num(usrname):
    return get_spam_cnt(usrname)+get_benign_cnt(usrname)

def get_time_cnt(usrname):
    dict = {}
    with sql.connect("database.db") as con:
        cur = con.cursor()
        try:
            cur.execute("SELECT Date FROM "+usrname)
            for row in cur:
                if row[0] in dict:
                    dict[row[0]] += 1
                else:
                    dict[row[0]] = 1
        except TypeError:
            print("did not find it")
            pass
    return dict

def get_past_ten_database(usrname):
    ten_list = []
    with sql.connect("database.db") as con:
        cur = con.cursor()
        try:
            cur.execute("SELECT Label,ID,Date, Content FROM " + usrname + " ORDER BY ID DESC LIMIT 10")
            for row  in cur:
                new_date = time_formatter(row[2])
                t = (row[0],row[1],new_date,row[3])
                ten_list.append(t)
        except TypeError:
            print("did not find it")
            pass
    return ten_list

def get_past_fiften_database(usrname):
    fiften_list = []
    with sql.connect("database.db") as con:
        cur = con.cursor()
        try:
            cur.execute("SELECT ID,Date, Content, Label FROM " + usrname + " ORDER BY ID ASC LIMIT 15")
            for row in cur:
                new_date = time_formatter(row[1])
                t = (row[0],new_date,  row[2], row[3])
                fiften_list.append(t)
        except TypeError:
            print("did not find it")
            pass
    return fiften_list

def get_fiften_frame(usrname,covered):
    fiften_list = []
    print("covered: "+covered)
    with sql.connect("database.db") as con:
        cur = con.cursor()
        try:
            cur.execute("SELECT ID, Date,Content, Label FROM " + usrname + " ORDER BY ID LIMIT 15 OFFSET "+covered)
            for row in cur:
                new_date = time_formatter(row[1])
                t = (row[0], new_date, row[2], row[3])
                fiften_list.append(t)
        except TypeError:
            print("did not find it")
            pass
    return fiften_list

def checkbox_label_database(usrname,id,label):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        try:
            cur.execute("UPDATE " + usrname + " SET label = (?) WHERE id =(?) ", (label,id))
        except TypeError:
            print("did not find it")
            pass

def select_to_csv(username):
    file_path = "wordClouds/" + username + ".csv"
    init_csv(file_path)
    with sql.connect("database.db") as con:
        with open(file_path, "a", newline='') as csvfile:
            cur = con.cursor()
            try:
                cur.execute("SELECT Label,Content FROM " + username)
                for row in cur:
                    row[1].replace("#"," ")
                    writer = csv.writer(csvfile)
                    writer.writerow(row)
            except TypeError:
                print("did not find it")
                pass
    con.close()

def init_csv(file_path):
    tag_list = ["Type", "Tweet"]
    with open(file_path, 'w', newline='') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        wr.writerow(tag_list)
