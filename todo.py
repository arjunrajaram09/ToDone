#----------------------------------------------#
# 2. Password - restriction -- how many letters, numbers etc
# 3. Add scroll for task list and thirty days tasks

        

#----------------------------------------------#
# TODO From Duds -
# 1. change completeddate to completed_date everywhere
# 2. change interdue to international_due_date everywhere

# 4. Remove logout button
# 5. Make the font larger in task list in task screen
#
#

#Created by Arjun P. Rajaram
#Started in early August 2023

from tkinter import *
from database import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import date,datetime, timedelta,time


    
def dailyover():
    
##    global dailyw; dailyw = Toplevel(loginw)
    time = (datetime.now()).strftime("%Y-%m-%d__%H'%M")
    showntime = (datetime.now()).strftime("%m/%d/%Y %H:%M")

##    print(time,type(time))
    
##    time = (datetime.now()).strftime("%m/%d/%Y %H:%M")
##    dailyw.geometry("1000x730")
##    taskw.withdraw()
##    dailyw.title("Daily Overview")
##    dailyw.resizable(False,False)
##    canvas = Canvas(taskw, height=730,width=1000,)
##    canvas.pack()
##    bback = Button(dailyw, text='<< Back to Task Screen',width=20,height=2,command=(ridofdaily))
##    bback.place(x=25,y=675)
    twentyfourhr= datetime.now() - timedelta(hours = 24)
    twentyfourhr=parser.parse(twentyfourhr.strftime('%Y-%m-%d %H:%M'))
    comp = readallcompleted(usern)


    file = open(time,"w+")
    file.write("Current Date and Time: "+showntime+"\n\n")
    file.write("Tasks Completed over the Last 24 Hours:\n")
    
    for i in range(len(comp)):
        comptime=(parser.parse(comp[i][3]))

        comptask=comp[i][4]
        if comptime>=twentyfourhr:
            compontime = comp[i][2]
            comptime=str(comptime)
            file.write("Task: "+comptask+"    "+"Date: "+comptime+"    "+"Completed on Time?: "+compontime+"\n")
    file.write("\n")
    dayone= datetime.now() + timedelta(hours = 24)
    dayone=parser.parse(dayone.strftime('%Y-%m-%d'))

    daythree= datetime.now() + timedelta(hours =72 )
    daythree=parser.parse(daythree.strftime('%Y-%m-%d'))

    dayfive= datetime.now() + timedelta(hours = 120)
    dayfive=parser.parse(dayfive.strftime('%Y-%m-%d'))
    
    tasks=(read_all_tasks_for_user(usern))
    file.write("Task(s) due Tommorow:\n")
    for l in range(len(tasks)):
        duedate=tasks[l][3]
        duetask=tasks[1][1]
        duedate = datetime.strptime(duedate, '%Y-%m-%d %H:%M:%S')
        if duedate == dayone:
            file.write(duetask+"\n")
    file.write("\nTask(s) due in Three Days:\n")
    for ld in range(len(tasks)):
        duedate=tasks[ld][3]
        duetask=tasks[ld][1]
        duedate = datetime.strptime(duedate, '%Y-%m-%d %H:%M:%S')
        if duedate == daythree:
            file.write(duetask+"\n")
    file.write("\nTask(s) due in Five Days:\n")
    for ldd in range(len(tasks)):
        duedate=tasks[ldd][3]
        duetask=tasks[ldd][1]
        duedate = datetime.strptime(duedate, '%Y-%m-%d %H:%M:%S')    
        if duedate == dayfive:
            file.write(duetask+"\n")
    file.close()

##            compdate=comptime[0]
##            comptime=comptime[1]

            
        

    

def logout():
    loginw.deiconify()
    taskw.destroy()
    
def ridofthirty():
    taskw.deiconify()
    thirtyw.destroy()
    
def thirtydays():
    global thirtyw; thirtyw = Toplevel(loginw)
    today = date.today()
    
    thirtyw.geometry('1000x730+25+25')
    taskw.withdraw()

    thirtyw.title("30 Day Overview")
    thirtyw.resizable(False,False)
    canvas = Canvas(thirtyw, height=730,width=1000,bg = '#e3e3e3')
    canvas.pack()

    bback = Button(thirtyw, text='<< Back to Task Screen',width=20,height=2,command=(ridofthirty))
    bback.place(x=25,y=675)

    ldate= Label(thirtyw, text='d')
    ldate.place(x=200,y=400)

    coll = ('date', 'desc', 'completed')
    global thirtytasks; thirtytasks = ttk.Treeview(thirtyw, columns=coll, show='headings',height=30,selectmode='none')

    thirtytasks.heading('date', text='Date')
    thirtytasks.column("desc",anchor=CENTER, stretch=NO, width=320)
        
    thirtytasks.heading('desc', text='Tasks Completed on Date')
    thirtytasks.column("date",anchor=CENTER, stretch=NO, width=320)

    thirtytasks.heading('completed', text='How many Completed on Time')
    thirtytasks.column("completed",anchor=CENTER, stretch=NO, width=320)
    thirtytasks.place(x=20,y=20)
    monthdays=[]
    comp=(readallcompleted(usern))
    for nday in range(31):
        monthdays.append((today - timedelta(days = nday)))
    #monthdays.remove(monthdays[0])
    
    for i in range(30):
        count = count_tasks_user(usern, monthdays[i])
        counton = count_on_time_user(usern,monthdays[i])
        thirtytasks.insert('', 'end', text='yes', values=(monthdays[i],str(count), str(counton)))



def taskclicked(n):
    taskclick = tasklist.focus()
    taskclick=(tasklist.item(taskclick,'values'))
    if taskclick != '' and (eatask.get() != taskclick[0]):
        eatask.delete(0,END)
        eatask.insert(0,taskclick[0])
        dcal.set_date(taskclick[1])

def addtasks():
    newtask = eatask.get()
    newdate = (dcal.get())
    alltasks = read_all_tasks_for_user(usern)
    if newtask != '' :
        add_task(newtask,newdate, usern)

        alltasks= read_all_tasks_for_user(usern)
        tasklist.insert('', 'end', text=str(len(alltasks)+1), values=(str(alltasks[len(alltasks)-1][1]),str(alltasks[len(alltasks)-1][2]),str(alltasks[len(alltasks)-1][0])))
        eatask.delete(0, 'end')
        dcal.set_date(date.today()) 
        
def updatetask():
    changeline = tasklist.focus()
    if changeline !='':
        currentline=(tasklist.item(changeline,'values'))
        newtask = eatask.get()
        newdate = (dcal.get())
        alltasks = read_all_tasks_for_user(usern)

        lineid=currentline[2]
        update_task(newtask,newdate,lineid)
        changedline= tasklist.selection()[0]
        tasklist.item(changedline, text="updated", values=(newtask, newdate,lineid))
        eatask.delete(0, 'end')
        
def deletetask():
    changeline = tasklist.focus()
    if changeline !='':
        currentline=(tasklist.item(changeline,'values'))

        lineid=currentline[2]
        select= tasklist.selection()[0]
        tasklist.delete(select)

        delete_task(lineid)
        eatask.delete(0, 'end')

def completetask():
    changeline = tasklist.focus()
    if changeline !='':
        currentline=(tasklist.item(changeline,'values'))
        alltasks = read_all_tasks_for_user(usern)
        lineid=currentline[2]
        completedtask(lineid)
        select= tasklist.selection()[0]
        print(select)
        tasklist.delete(select)
        eatask.delete(0, 'end')
def completeall():
    tas=read_all_tasks_for_user(usern)

    for i in range(len(tas)):
        d=tas[i][0]
        completedtask(d)
    for t in tasklist.get_children():
        tasklist.delete(t)
        
        

# SORT TASKS BY DESCRIPTION    
def sortalpha(lis):
    return lis[1]

def alphalist():
    alltasks = read_all_tasks_for_user(usern)
    alltasks.sort(key=sortalpha)
    tasklist.delete(*tasklist.get_children())
    eatask.delete(0,END)
#Wish there was a faster way to update the list box
    for i in range(0,len(alltasks)):
        tasklist.insert('', 'end', text=str(i+1), values=(str(alltasks[i][1]),str(alltasks[i][2]),str(alltasks[i][0]) ))
def sortcreate(lis):
    return lis[0]

def createdlist():
    alltasks = read_all_tasks_for_user(usern)
    alltasks.sort(reverse=True,key=sortcreate)
    tasklist.delete(*tasklist.get_children())
    eatask.delete(0,END)
#Wish there was a faster way to update the list box
    for i in range(0,len(alltasks)):
        tasklist.insert('', 'end', text=str(i+1), values=(str(alltasks[i][1]),str(alltasks[i][2]),str(alltasks[i][0]) ))

def rcreatedlist():
    alltasks = read_all_tasks_for_user(usern)
    alltasks.sort(key=sortcreate)
    tasklist.delete(*tasklist.get_children())
    eatask.delete(0,END)
#Wish there was a faster way to update the list box
    for i in range(0,len(alltasks)):
        tasklist.insert('', 'end', text=str(i+1), values=(str(alltasks[i][1]),str(alltasks[i][2]),str(alltasks[i][0]) ))

def sortduedate(lis):
    return lis[3]
def duelist():
    alltasks = read_all_tasks_for_user(usern)
    alltasks.sort(key=sortduedate)
    tasklist.delete(*tasklist.get_children())
    eatask.delete(0,END)
#Wish there was a faster way to update the list box
    for i in range(0,len(alltasks)):
        tasklist.insert('', 'end', text=str(i+1), values=(str(alltasks[i][1]),str(alltasks[i][2]),str(alltasks[i][0]) ))


def registeracc():
    newuser=((enuser.get()).lower()).strip()
    newpass=enpass.get().strip()
    newrepass = erepass.get().strip()
    if newuser == '':
        lregerror.config(text = 'ERROR: Must enter a username',fg='#e31809',font=('Helvetica', 17, 'bold'))
    elif newpass == '':
        lregerror.config(text = 'ERROR: Must enter a password',fg='#e31809',font=('Helvetica', 17, 'bold'))
    elif newpass != newrepass:
        lregerror.config(text = 'ERROR: Passwords must match',fg='#e31809',font=('Helvetica', 17, 'bold'))
    elif len(newpass)<6:
        lregerror.config(text = 'ERROR: Password too short',fg='#e31809',font=('Helvetica', 17, 'bold'))
    else:
        euser.delete(0, 'end')
        epass.delete(0, 'end')
        enuser.delete(0, 'end')
        enpass.delete(0, 'end')
        erepass.delete(0, 'end')

        row = read_user(newuser)

        if (row == None):
            add_user(newuser, newpass)
            loginw.deiconify()
            llogerror.config(text = '',fg='#e31809',font=('Helvetica', 18, 'bold'))
            regw.destroy()
        else:
            lregerror.config(text = 'ERROR: Username already exists',fg='#e31809',font=('Helvetica', 17, 'bold'))
        
def regscrn():
    loginw.withdraw()
    global regw
    regw = Toplevel(loginw)

    regw.geometry('1000x730+25+25')
##    global x; x=regw.winfo_x()
##    global y; y=regw.winfo_y()
    regw.config(bg = '#c9c9c9')
    regw.title("ToDone Register")
    regw.resizable(False,False)
    canvas = Canvas(regw, height=730,width=1000,bg = '#e3e3e3')
    canvas.pack()
    
    global lregerror; lregerror = Label(regw, text='',bg = '#e3e3e3')
    lregerror.place(x=380,y=550)
    
    lnuser= Label(regw, text="Username",font=('Helvetica', 24,'bold'),bg = '#e3e3e3')
    global enuser; enuser = Entry(regw,font=('Helvetica', 24))
    lnuser.place(x=100,y=230)

    enuser.place(x=400,y=230)

    lreg = Label(regw,text="Register an Account",font=('Courier',50,'bold' ),bg = '#e3e3e3')
    lreg.place(x=115,y=40)
    
    lnpass= Label(regw, text="Password",font=('Helvetica', 24,'bold'),bg = '#e3e3e3')
    global enpass; enpass = Entry(regw,show="*",font=('Helvetica', 24,'bold'))
    lnpass.place(x=100,y=290)
    enpass.place(x=400,y=290)

    lrepass= Label(regw, text="Re-Type Password",font=('Helvetica', 24,'bold'),bg = '#e3e3e3')
    global erepass; erepass = Entry(regw,show="*",font=('Helvetica', 24,'bold'))
    lrepass.place(x=100,y=350)
    erepass.place(x=400,y=350)
    
    bsreg = Button(regw, text='Register Account',width=15,height=2,command=registeracc,font=('Helvetica', 24,'bold'))
    bsreg.place(x=420,y=430)
    
#Gets the actual task making screen
def taskscrn():
    today = date.today()
       
    loginw.withdraw()
    global taskw; taskw = Toplevel(loginw)
    euser.delete(0, 'end')
    epass.delete(0, 'end')
    taskw.geometry('1000x730+25+25')

##    global x; x=taskw.winfo_x()
##    global y; y=taskw.winfo_y()
    taskw.title("Task Creation")
    taskw.resizable(False,False)
    canvas = Canvas(taskw, height=730,width=1000,bg = '#e3e3e3')
    canvas.pack()

    blogout = Button(taskw,text='Logout',width=15,height=2,command=logout)
    blogout.place(x=25,y=675)
    print(read_all_tasks_for_user(usern))
    canvas.create_rectangle( 20, 20, 980, 467,width=2)
    canvas.create_line(0,550,1000,550, width=2)
    
    badd = Button(taskw, text='Add Task',width=10,height=2,command=addtasks)
    badd.place(x=900,y=560)
    
    canvas.create_rectangle( 900, 610, 979, 650)

    bup = Button(taskw, text='Update Task',width=10,height=2,command=updatetask)
    bup.place(x=900,y=610)

    coll = ( 'desc', 'date', 'id')

    global tasklist; tasklist = ttk.Treeview(taskw, columns=coll, show='headings',height=21,selectmode='browse')

  #  style = ttk.Style()
 #   style.configure("Treeview.Heading", font=(None, 30))
    tasklist.heading('desc', text='Task Description')
    tasklist.column("desc",anchor=W, stretch=NO, width=478)
    
    tasklist.heading('date', text='Due Date')
    tasklist.column("date",anchor=CENTER, stretch=NO, width=478)

    tasklist.heading('id', text='ID')
    tasklist.column("id",anchor=W, stretch=NO, width=0)

    tasklist.place(x=21,y=20)
    tasklist.bind('<ButtonRelease-1>', taskclicked)
    alltasks = read_all_tasks_for_user(usern)
    
    for i in range(0,len(alltasks)):
        tasklist.insert('', 'end', text=str(i+1), values=(str(alltasks[i][1]),str(alltasks[i][2]), str(alltasks[i][0]) ))  

    bdel = Button(taskw, text='Delete Task',width=10,height=2,command=deletetask)
    bdel.place(x=900,y=660)
    
    bthirtyreport = Button(taskw, text='See 30 day overview',height=2,command=thirtydays)
    bthirtyreport.place(x=20,y=480)

    bdailyreport = Button(taskw, text='Create Daily overview',height=2,command=dailyover)
    bdailyreport.place(x=170,y=480)

    balphasort = Button(taskw, text='Sort tasks alphabetically',height=2,command=alphalist)
    balphasort.place(x=300,y=480)

    bduesort= Button(taskw, text='Sort tasks by due date',height=2,command=duelist)
    bduesort.place(x=470,y=480)

    bcreatesort = Button(taskw, text='Sort tasks by newest created',height=2,command=createdlist)
    bcreatesort.place(x=620,y=480)

    brcreatesort = Button(taskw, text='Sort tasks by oldest created',height=2,command=rcreatedlist)
    brcreatesort.place(x=805,y=480)

    latask= Label(taskw, text=" Task Name",bg = '#e3e3e3')
    global eatask; eatask = Entry(taskw)
    latask.place(x=25,y=580)
    eatask.place(x=120,y=580, width=250)

    ladate= Label(taskw, text=" Task Date",bg = '#e3e3e3')
    ladate.place(x=25,y=630)

    bcomplete = Button(taskw, text='Complete Task',height=2,command=completetask)
    bcomplete.place(x=400,y=565)

    bcompleteall = Button(taskw, text='Complete All Tasks',height=2,command=completeall)
    bcompleteall.place(x=525,y=565)

    end = datetime.strptime("12/31/2099", "%m/%d/%Y")

#    global dcal; dcal = DateEntry(taskw, width= 16, foreground= "white",mindate=(date.today()),maxdate=(end))
    global dcal; dcal = DateEntry(taskw, width= 16, foreground= "white",maxdate=(end))
    dcal.place(x=125,y=630)

def loginacc():
    global usern; usern = ((euser.get()).lower()).strip()
    global passw; passw = epass.get().strip()
    enter = (usern,passw)
    rows= read_all_users()
    if usern=='':
        llogerror.config(text = 'ERROR: Must enter a Username',fg='#e31809',font=('Helvetica', 17, 'bold'))
    elif passw == '':
        llogerror.config(text = 'ERROR: Must enter a Password',fg='#e31809',font=('Helvetica', 17, 'bold'))
    elif enter not in rows:
        llogerror.config(text = 'ERROR: Account does not exist',fg='#e31809',font=('Helvetica', 17, 'bold'))
    else:
        taskscrn()
    
#Starts program, pretty much the main
def entryscrn():
    global started; started=1
    global loginw; loginw = Tk()
    loginw.geometry('1000x730+25+25')
    loginw.config(bg = '#c9c9c9')
    canvas = Canvas(loginw, height=730,width=1000,bg = '#e3e3e3')
    canvas.pack()



    
    loginw.title('ToDone Login')
    loginw.resizable(False,False)
    global created;created=1
    luser= Label(loginw, text="Username", font=('Helvetica', 24,'bold'))
    global euser; euser = Entry(loginw, font=('Arial', 24))
    luser.place(x=150,y=300)
    luser.config(bg = '#e3e3e3')
    euser.place(x=410,y=300)
    
    ltodone = Label(loginw,text="ToDone",font=('Courier',110,'bold' ),bg = '#e3e3e3')
    ltodone.place(x=230,y=40)

    lcreated = Label(loginw,text="Created by Arjun Rajaram",font=('Courier',12),bg = '#e3e3e3')
    lcreated.place(x=375,y = 200)
    
    global llogerror; llogerror = Label(loginw,text='',bg = '#e3e3e3')
    llogerror.place(x=350,y=650)
    llogerror.config(text = '',fg='#e31809',font=('Helvetica', 18, 'bold'))
    
    lpass= Label(loginw, text="Password", font=('Helvetica', 24,'bold'))
    global epass; epass = Entry(loginw,show="*", font=('Arial', 24))
    lpass.place(x=150,y=400)
    lpass.config(bg = '#e3e3e3')
    epass.place(x=410,y=400)
    
    blogin = Button(loginw, text='Login',width=20,height=2,font=('Arial',24,'bold'),command=loginacc)
    blogin.place(x=350,y=490)

    bregister = Button(loginw, text='Register',width=20,height=2,command=regscrn)
    bregister.place(x=30,y=680)
    lreg= Label(loginw, text="No Account?")
    lreg.place(x=70,y=655)
    lreg.config(bg='#e3e3e3')

    loginw.mainloop()

#start of program
if __name__ == "__main__":
    setup_db()
    #VVVV Deletes everything from table
    #delete_user_table()
    #^^^^ Deletes everything from table
    entryscrn()








