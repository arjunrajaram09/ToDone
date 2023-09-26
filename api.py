#Runs API for todo
from flask import Flask
from flask import request

from database import *
app = Flask(__name__)

@app.route('/gettask/<user>', methods = [ 'GET' ])
def tasks(user):
    setup_db()
    tasks=read_all_tasks_for_user(user)
    return tasks

@app.route("/addtask", methods = [ 'POST' ])
def addtask_api():
    task = request.json
    description = task["description"]
    due_date = task["due_date"]
    user = task["user"]
    setup_db()
    add_task(description, due_date, user)
    return "Task Successfully Added"

@app.route("/updatetask", methods = [ 'PUT' ])
def updatetask_api():
    task = request.json
    description = task["description"]
    due_date = task["due_date"]
    lineid = task["id"]
    setup_db()
    update_task(description, due_date, lineid)
    return "Task Successfully Updated"

@app.route("/deletetask", methods = [ 'DELETE' ])
def deletetask_api():
    task = request.json

    lineid = task["id"]
    setup_db()
    delete_task(lineid)
    return "Task Successfully Deleted"
