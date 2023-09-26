import sqlite3
from datetime import date,datetime
import dateutil.parser as parser

def setup_db():
    global connection
    global cursor
    connection = create_db_connection("todo.db")
    cursor = create_db_tables()

def create_db_connection(dbname):
    connection = None
    connection = sqlite3.connect(dbname)
    return connection

def create_db_tables():
    cursor = connection.cursor()
    #Clear tasks list VVVVVVV
    #cursor.execute("DROP TABLE IF EXISTS task")
    #cursor.execute("DROP TABLE IF EXISTS user")
    cursor.execute("CREATE TABLE IF NOT EXISTS user (name TEXT PRIMARY KEY, password TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS task (ID INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT, due_date DATE, completeddate DATE, ontime TEXT, interdue DATE, user TEXT,comptime DATE)")
    connection.commit()
    return cursor

# USER Table
def add_user(name, password):
    cursor.execute("INSERT INTO user (name, password) VALUES (?, ?)", (name, password))
    connection.commit()
    
def read_all_users():
    users = cursor.execute("SELECT name, password FROM user").fetchall()
    return users

def read_user(name):
    cursor.execute("SELECT name FROM user WHERE name=?", (name,))
    user = cursor.fetchone()
    return user

def read_user_and_pass(name, password):
    cursor.execute("SELECT name FROM user WHERE name=? AND password=?", (name, password))
    user = cursor.fetchone()
    return user

def delete_user():
    cursor.execute("DELETE FROM user")
    connection.commit()



# TASK Table
def read_all_tasks():
   tasks = cursor.execute("SELECT id, description, due_date, user FROM task").fetchall()
   return tasks

def read_all_tasks_for_user(user):
    tasks = cursor.execute("SELECT id, description, due_date,interdue, user FROM task WHERE user=? AND completeddate=01/01/1900", (user,)).fetchall()
    return tasks

def count_tasks_user(user, date):
    count = cursor.execute("SELECT COUNT(*) FROM task WHERE user=? AND completeddate=?", (user,date)).fetchone()
    return count[0]
def count_on_time_user(user, date):
    count = cursor.execute("SELECT COUNT(*) FROM task WHERE user=? AND completeddate=? AND ontime='YES'", (user,date)).fetchone()
    return count[0]

def readallcompleted(user):
    tasks = cursor.execute("SELECT id,completeddate,ontime,comptime,description FROM task WHERE user=? AND completeddate NOT IN (01/01/1900)", (user,)).fetchall()
    return tasks

def read_task(id):
    cursor.execute("SELECT description, due_date FROM task WHERE id=?", (id))
    task = cursor.fetchone()
    return task

def add_task(description,due_date,user):
    interdate = parser.parse(due_date)
    cursor.execute("INSERT INTO task (description, due_date, user,completeddate,ontime,interdue,comptime) VALUES (?,?,?,01/01/1900,'N/A',?,01/01/1900)", (description, due_date, user,interdate))
    connection.commit()
    
def update_task(task,date,lid):
    interdate = parser.parse(date)
    cursor.execute("UPDATE task SET description=?, due_date=?,interdue=? WHERE id=?",(task,date,interdate,lid))
    connection.commit()
    
def delete_task(lineid):
    cursor.execute("DELETE FROM task WHERE id=?",(lineid,))
    connection.commit()

def completedtask(lid):
    cursor.execute("SELECT due_date FROM task WHERE id=?", (lid,))
    due = (cursor.fetchone())[0]
    due = ((str(parser.parse(due))).split(' '))[0]

    due= datetime.strptime(str(due),'%Y-%m-%d').date()
    current = datetime.now()

    time = current.strftime("%Y-%m-%d %H:%M")
    today = date.today()
    today= datetime.strptime(str(today),'%Y-%m-%d').date()
    cursor.execute("UPDATE task SET completeddate=? WHERE id=?",(today,lid))
    cursor.execute("UPDATE task SET comptime=? WHERE id=?",(time,lid))
    if today<=due:
        cursor.execute("UPDATE task SET ontime='YES' WHERE id=?",(lid,))
    else:
        cursor.execute("UPDATE task SET ontime='NO' WHERE id=?",(lid,))
    connection.commit()    
