import csv
import mysql.connector
import pyautogui as pag
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtWidgets

class Login(QMainWindow):
    def __init__(self, cursor=None):
        super(Login, self).__init__()
        uic.loadUi("login.ui", self)
        self.show()
        
        self.actionClose.triggered.connect(exit)
        self.submitbtn.clicked.connect(lambda: self.login(cursor))
        
    def login(self,cursor):
        global userid, name, role, password, mail
        temp_userid = self.userIDedit.text()
        temp_password = self.passwordedit.text()
        try:
            cursor.execute(f"select * from users where userid = {temp_userid}")
            userid, name, role, password, mail = cursor.fetchone()
            if(password == temp_password):
                print("Verified User, Can use the portal")
                self.close()
            else:
                pag.alert("Incorrect UserID or Password.\nTry Again!", "Wrong password",)
                csv_writer.writerow(["Incorrect Passwords"])
                print("Wrong password!")
                self.userIDedit.setText("")
                self.passwordedit.setText("")
        except Exception as e:
            csv_writer.writerow([f"{e}"])
            pag.alert("Incorrect UserID.\nTry Again!", "Wrong password",)
            print("Wrong UserID or password!")
            self.userIDedit.setText("")
            self.passwordedit.setText("")
        
class DashBoard_Prof(QMainWindow):
    def __init__(self, cursor):
        global action
        super(DashBoard_Prof, self).__init__()
        uic.loadUi("dashboard_prof.ui", self)
        self.show()
        self.namelabel.setText(f"Hello! {name.title()}")
        self.rolelabel.setText(f"{role.title()}")
        self.maillabel.setText(mail)
        self.actionClose.triggered.connect(exit)
        self.toEdit = None
        self.radioButton_name.toggled.connect(self.nameselected)
        self.radioButton_mail.toggled.connect(self.mailselected)
        self.radioButton_userid.toggled.connect(self.useridselected)
        self.radioButton_password.toggled.connect(self.passwordselected)
        self.editbtn.clicked.connect(lambda: self.editdetails(cursor))
        
        self.projectbtn.clicked.connect(lambda: self.nextAction("project"))
        # self.teambtn.clicked.connect(lambda: self.nextAction("project"))
        self.submissionbtn.clicked.connect(lambda: self.nextAction("submission"))
        
        
        try:
            cursor.execute("select * from project;")
            cursor.fetchall()
            self.projectcount.setText(f'{cursor.rowcount}')
            cursor.execute("select * from team;")
            cursor.fetchall()
            self.teamcount.setText(f'{cursor.rowcount}')
            cursor.execute("select * from submission where status = 'rejected';")
            cursor.fetchall()
            self.submissionpendingcount.setText(f'{cursor.rowcount}')
            cursor.execute("select * from submission where status = 'accepted';")
            cursor.fetchall()
            self.submissioncompletedcount.setText(f'{cursor.rowcount}')
            cursor.execute("select * from submission;")
            cursor.fetchall()
            self.totalsubmissioncount.setText(f'{cursor.rowcount}')
        except Exception as e:
            csv_writer.writerow([f'{e}'])
    
    def nextAction(self, val):
        global action
        action = val
        self.close()
        
    def editdetails(self, cursor):
        edittable = pag.prompt(f"Enter the Editted {self.toEdit.title()}", "Edit Details")
        if self.toEdit != "userid":
            edittable = f"'{edittable}'"
        try:
            cursor.execute(f"update users set {self.toEdit} = {edittable} where userid = {userid};")
            conn.commit();
        except Exception as e:
            csv_writer.writerow([f'{e}'])
        
    def nameselected(self, selected):
        if selected:
            self.toEdit = "name"
            print(name)
    def passwordselected(self, selected):
        if selected:
            self.toEdit = "password"
            print(password)
    def useridselected(self, selected):
        if selected:
            self.toEdit = "userid"
            print(userid)
    def mailselected(self, selected):
        if selected:
            self.toEdit = "email"
            print(mail)

class Project(QMainWindow):
    def __init__(self, cursor):
        global action
        super(Project, self).__init__()
        uic.loadUi("project.ui", self)
        self.project_table.setColumnWidth(1,250)
        self.load(cursor)
        self.show()
        self.deleteprojectbtn.clicked.connect(lambda : self.deleteproject(cursor))
        self.addprojectbtn.clicked.connect(lambda : self.addproject(cursor))
        self.openprojectbtn.clicked.connect(lambda: self.openproject(cursor))
    
    def openproject(self, cursor):
        global PID, action
        try:
            val = int(pag.prompt("Enter the Project ID, which is to be Opened"))
            cursor.execute(f"select * from project where pid = {val}")
            cursor.fetchall()
            if (cursor.rowcount <= 0):
                pag.alert("Invalid Project ID!\nTry Again")
            else:
                PID = str(val)
                action = "openproject"
                self.close()
        except Exception as e:
            csv_writer.writerow([f'{e}'])
            print(e)
            pag.alert("An Error Occured.\nTry Again!")
    
    def addproject(self, cursor):
        temp_pid = self.projectidedit.text()
        temp_start_date = self.startdateedit.date().toString("yyyy-MM-dd")
        temp_end_date = self.enddateedit.date().toString("yyyy-MM-dd")
        temp_title = self.titleedit.toPlainText()
        temp_desc = self.descedit.toPlainText()
        try:
            if pag.confirm("Are You sure you want to add a new project?", buttons=["Yes","No"], title="New Project") == "Yes":
                cursor.execute(
                    f"insert into project values({temp_pid}, '{temp_title}', 'ongoing', '{temp_desc}', '{temp_start_date}','{temp_end_date}');"
                )
                conn.commit()
                
        except Exception as e:
            csv_writer.writerow([f'{e}'])
            print(e)
            pag.alert("An Error Occured.\nTry Again!")
        self.load(cursor)
    
    def deleteproject(self, cursor):
        try:
            X = int(pag.prompt("Enter Project ID to be deleted"))
            if pag.confirm("Are you sure you want to delete",title="Confirmation", buttons=["Yes", "No"]) == "Yes":
                cursor.execute(f"delete from submission where pid = {X}")
                conn.commit()
                cursor.execute(f"delete from project where pid = {X}")
                conn.commit()
                
        except Exception as e:
            csv_writer.writerow([f'{e}'])
            pag.alert("An Error Occured.\nTry Again!")
        self.load(cursor)
    
    def load(self,cursor):
        cursor.execute("select pid, title, status, enddate from project;")
        rec = cursor.fetchall()
        self.project_table.setRowCount(len(rec))
        for i in range(len(rec)):
            self.project_table.setItem(i,0,QtWidgets.QTableWidgetItem(f'{rec[i][0]}'))
            self.project_table.setItem(i,1,QtWidgets.QTableWidgetItem(rec[i][1]))
            self.project_table.setItem(i,2,QtWidgets.QTableWidgetItem(rec[i][2]))
            self.project_table.setItem(i,3,QtWidgets.QTableWidgetItem(f'{rec[i][3]}'))
                  
class TeamAndTask(QMainWindow):
    def __init__(self,cursor, PID):
        super(TeamAndTask, self).__init__()
        global status
        status = None
        uic.loadUi("teamANDtask.ui", self)
        self.team_table.setColumnWidth(2,160)
        self.team_table.setColumnWidth(1,80)
        self.team_table.setColumnWidth(0,80)
        self.task_table.setColumnWidth(0,80)
        self.task_table.setColumnWidth(1,80)
        self.task_table.setColumnWidth(2,200)
        self.task_table.setColumnWidth(3,120)
        self.load(cursor,PID)
        self.deletememberbtn.clicked.connect(lambda: self.delete_member(cursor, PID))
        self.addmemberbtn.clicked.connect(lambda: self.add_member(cursor, PID))
        self.deletetaskbtn.clicked.connect(lambda: self.delete_task(cursor, PID))
        self.addtaskbtn.clicked.connect(lambda: self.add_task(cursor, PID))
        self.changetaskstatusbtn.clicked.connect(lambda:self.change_task_status(cursor, PID))
        self.radioButton_completed.toggled.connect(self.completedselected)
        self.radioButton_ongoing.toggled.connect(self.ongoingselected)
        self.show()
        
    def completedselected(self):
        global status
        status = "Completed"
    
    def ongoingselected(self):
        global status
        status = "Ongoing"
    
    def change_task_status(self,cursor, PID):
        taskid = self.taskidedit.text()
        if taskid == '' :
            pag.alert("Enter the Task ID for Tasks whose status is to be changed") 
        elif status == None:
            pag.alert("Select the Status of the Task") 
        else:
            try:
                if pag.confirm("Are you sure you want to Change Task Status?", buttons=["Yes", "No"]) == "Yes":
                    cursor.execute(f"update task set status = '{status}' where taskid = {taskid};")
                    conn.commit()
            except Exception as e:
                print(e)
                pag.alert("An Error Occured.\nTry Again!")
        self.load(cursor, PID=PID)
        
        
    def add_task(self, cursor, PID):
        taskid = self.taskidedit.text()
        taskdesc = self.taskdescedit.toPlainText()
        title = self.titleedit.toPlainText()
        enddate = self.enddateedit.date().toString("yyyy-MM-dd")
        try:
            userid = pag.prompt("Enter the User ID you want the task to be added", title="User ID Input")
            if userid == '':
                pag.alert("Invalid User ID!\nTry Again.")
            else:
                cursor.execute(f"select name from users where userid = {userid};")
                x = cursor.fetchall()
                if cursor.rowcount <= 0:
                    pag.alert("Invalid User ID!\nTry Agian.")
                else:
                    x = x[0][0]
                    cursor.execute(f"insert into task values({taskid},{userid}, '{title}', '{taskdesc}','{x}','Ongoing','{enddate}');")
                    conn.commit()
        except Exception as e:
            print(e)
        self.load(cursor, PID)
        
    def delete_task(self, cursor, PID):
        taskid = self.taskidedit.text()
        if taskid == '' :
            pag.alert("Enter the Task ID for Tasks to be Deleted") 
        else:
            try:
                if pag.confirm("Are you sure you want to Delete the Task?", buttons=["Yes", "No"]) == "Yes":
                    cursor.execute(f"delete from task where taskid = {taskid};")
                    conn.commit()
            except Exception as e:
                print(e)
                pag.alert("An Error Occured.\nTry Again!")
        self.load(cursor, PID=PID)
    
    def add_member(self, cursor, PID):
        teamid = self.newteamidedit.text()
        userid = self.newuseridedit.text()
        if teamid == '' or userid == '':
            pag.alert("Enter the User ID and Team ID for members to be Added to the Team") 
        else:
            try:
                cursor.execute(f"insert into team values({teamid}, {userid}, {PID}, 1);")
                conn.commit()
            except Exception as e:
                print(e)
                pag.alert("An Error Occured.\nTry Again!")
        self.load(cursor, PID=PID)
        
    def delete_member(self, cursor, PID):
        teamid = self.newteamidedit.text()
        userid = self.newuseridedit.text()
        if teamid == '' and userid == '':
            pag.alert("Enter the User ID or Team ID for members to be Deleted from the Team") 
        else:
            try:
                if pag.confirm("Are you sure you want to Delete Team Member?", buttons=["Yes", "No"]) == "Yes":
                    if userid == '':
                        userid = 0
                    elif taskid == '':
                        taskid = 0
                    cursor.execute(f"delete from team where teamid = {teamid} or userid = {userid};")
                    conn.commit()
            except Exception as e:
                print(e)
                pag.alert("An Error Occured.\nTry Again!")
        self.load(cursor, PID=PID)
        
    def load(self, cursor,PID):
        self.pidlabel.setText(PID)
        try:
            cursor.execute(f"select TeamId, userid, name from team join users using(userid) where pid={PID};")
            rec = cursor.fetchall()
            self.team_table.setRowCount(len(rec))
            for i in range(len(rec)):
                self.team_table.setItem(i,0,QtWidgets.QTableWidgetItem(f'{rec[i][0]}'))
                self.team_table.setItem(i,1,QtWidgets.QTableWidgetItem(f'{rec[i][1]}'))
                self.team_table.setItem(i,2,QtWidgets.QTableWidgetItem(rec[i][2]))
            
            cursor.execute(f"select taskid, userid, title, status from task join team using(userid) where pid = {PID};")
            rec = cursor.fetchall()
            self.task_table.setRowCount(len(rec))
            for i in range(len(rec)):
                self.task_table.setItem(i,0,QtWidgets.QTableWidgetItem(f'{rec[i][0]}'))
                self.task_table.setItem(i,1,QtWidgets.QTableWidgetItem(f'{rec[i][1]}'))
                self.task_table.setItem(i,2,QtWidgets.QTableWidgetItem(rec[i][2]))
                self.task_table.setItem(i,3,QtWidgets.QTableWidgetItem(rec[i][3]))
        except Exception as e:
            print(e)

class Submission(QMainWindow):
    def __init__(self, cursor=None):
        super(Submission, self).__init__()
        uic.loadUi("submission.ui", self)
        self.load(cursor)
        global temp_status 
        temp_status = None
        self.addsubmissionbtn.clicked.connect(lambda: self.add_submission(cursor))
        self.deletesubmissionbtn.clicked.connect(lambda: self.delete_submission(cursor))
        self.changestatusbtn.clicked.connect(lambda: self.change_status(cursor))
        self.radioButton_accepted.toggled.connect(self.acceptedselected)
        self.radioButton_rejected.toggled.connect(self.rejectedselected)
        self.show()
    
    def acceptedselected(self):
        global temp_status
        temp_status = 'accepted'
        
    def rejectedselected(self):
        global temp_status
        temp_status = 'rejected'
    
    def add_submission(self,cursor):
        subid = self.subidedit.text()
        pid = self.pidedit.text()
        duedate = self.duedateedit.date().toString("yyyy-MM-dd")
        if subid == '' or pid == '':
            pag.alert("Enter the Submission ID and Project ID for the Submission to be Added") 
        else:
            try:
                cursor.execute(f"insert into submission values({subid},{pid},'accepted','{duedate}');")
                conn.commit()
            except Exception as e:
                print(e)
                pag.alert("An Error Occured.\nTry Again!")
        self.load(cursor)
        
    def delete_submission(self,cursor):
        subid = self.subidedit.text()
        pid = self.pidedit.text()
        if subid == '' and pid == '':
            pag.alert("Enter the Submission ID or Project ID for members to be Deleted from the Submissions") 
        else:
            try:
                if pag.confirm("Are you sure you want to Delete this Submission?", buttons=["Yes", "No"]) == "Yes":
                    if pid == '':
                        pid = 0
                    elif subid == '':
                        subid = 0
                    cursor.execute(f"delete from submission where subid = {subid} or pid = {pid};")
                    conn.commit()
            except Exception as e:
                print(e)
                pag.alert("An Error Occured.\nTry Again!")
        self.load(cursor)
        
    def change_status(self,cursor):
        global temp_status
        print(temp_status)
        subid = self.subidedit.text()
        if subid == '' :
            pag.alert("Enter the Submission ID for Tasks whose status is to be changed") 
        elif temp_status == None:
            pag.alert("Select the Status of the Task") 
        else:
            try:
                if pag.confirm("Are you sure you want to Change Submission Status?", buttons=["Yes", "No"]) == "Yes":
                    cursor.execute(f"update submission set status = '{temp_status}' where subid = {subid};")
                    conn.commit()
            except Exception as e:
                print(e)
                pag.alert("An Error Occured.\nTry Again!")
        self.load(cursor)
    
    def load(self,cursor):
        try:
            cursor.execute("select SubID, PID, title, submission.status, Duedate from submission join project using(pid);")
            rec = cursor.fetchall()
            self.submission_table.setRowCount(len(rec))   
            for i in range(len(rec)):
                self.submission_table.setItem(i,0,QtWidgets.QTableWidgetItem(f'{rec[i][0]}'))
                self.submission_table.setItem(i,1,QtWidgets.QTableWidgetItem(f'{rec[i][1]}'))
                self.submission_table.setItem(i,2,QtWidgets.QTableWidgetItem(rec[i][2]))
                self.submission_table.setItem(i,3,QtWidgets.QTableWidgetItem(rec[i][3].title()))
                self.submission_table.setItem(i,4,QtWidgets.QTableWidgetItem(rec[i][4].isoformat()))
        except Exception as e:
            print(e)   
    
    
class Student(QMainWindow):
    def __init__(self, cursor):
        super(Student, self).__init__()
        uic.loadUi("student.ui", self)
        self.load(cursor)
        self.task_table.setColumnWidth(0,80)
        self.task_table.setColumnWidth(1,160)
        self.task_table.setColumnWidth(2,200)
        self.completetaskbtn.clicked.connect(lambda: self.complete_task(cursor))
        self.changepasswordbtn.clicked.connect(lambda: self.change_password(cursor))
        self.actionClose.triggered.connect(exit)
        self.show()
    
    def change_password(self,cursor):
        temp_password = pag.password("Enter your new password", title="Write your password")
        temp_password2 = pag.password("Confirm your new password", title="Confirm your password")
        if temp_password == temp_password2:
            try:
                cursor.execute(f"update users set password = '{temp_password}' where userid = {userid}")
                conn.commit()
                pag.alert("Password Changed Successfully!")
            except Exception as e:
                print(e)
                pag.alert("An Error Occured.\nTry Again!")
    
    def complete_task(self,cursor):
        taskid = self.taskidedit.text()
        if taskid == '':
            pag.alert("Enter the Task ID whose \nstatus is to be marked Completed") 
        else:
            try:
                if pag.confirm("Are you sure you want to Mark Task as Completed?", buttons=["Yes","No"]) == "Yes":
                    cursor.execute(f"update task set status = 'Completed' where taskid = {taskid};");
                    conn.commit()
            except Exception as e:
                print(e)
                pag.alert("An Error Occured.\nTry Again!")
        self.load(cursor)
            
    
    def load(self,cursor):
        userid, name, role, password, mail
        self.namelabel.setText(name.title())
        self.sid.setText(f'{userid}')
        self.maillabel.setText(mail)
        
        try:
            cursor.execute(f"select taskid, title, description, duedate from task where userid = {userid} and status = 'Ongoing';")
            rec = cursor.fetchall()
            self.task_table.setRowCount(len(rec))
            for i in range(len(rec)):
                self.task_table.setItem(i,0,QtWidgets.QTableWidgetItem(f'{rec[i][0]}'))
                self.task_table.setItem(i,1,QtWidgets.QTableWidgetItem(rec[i][1]))
                self.task_table.setItem(i,2,QtWidgets.QTableWidgetItem(rec[i][2]))
                self.task_table.setItem(i,3,QtWidgets.QTableWidgetItem(rec[i][3].isoformat()))
        except Exception as e:
            print(e)
        
        
def starterrorlog():
    global csv_writer
    f = open("errorlog.csv","w",newline="")
    csv_writer = csv.writer(f)
    
def connect_and_cursor(password):
    global conn
    try:
        conn = mysql.connector.connect(host="localhost",user="root",password=f"{password}", database="flowdata")
        print("Connection succesful")
        return conn.cursor()
    except Exception as e:
        csv_writer.writerow([f"{e}"])
        return None
    

def login(cursor):
    login = QApplication([])
    window = Login(cursor)
    login.exec_()
    
def dashboard_prof(cursor):
    dashboard_prof = QApplication([])
    window = DashBoard_Prof(cursor)
    dashboard_prof.exec_()

def project(cursor):
    project = QApplication([])
    window = Project(cursor)
    project.exec_()

def teamANDtask(cursor, PID):
    teamANDtask = QApplication([])
    window = TeamAndTask(cursor, PID)
    teamANDtask.exec_()

def submission(cursor):
    submission = QApplication([])
    window = Submission(cursor)
    submission.exec_()

def student(cursor):
    student = QApplication([])
    window = Student(cursor)
    student.exec_()

def initialize():
    return pag.password("Enter the Authentication Key Below", "Boot Auth")

def backups():
    print("Backing up database")

def main():
    starterrorlog()
    cursor = None
    attempt = 3
    while (cursor is None and attempt != 0):
        print("Authentication Attempt")
        cursor = connect_and_cursor(initialize())
        attempt-=1
        if attempt == 0:    
            csv_writer.writerow(['Exceeded Authentication Attempts, Exit'])
            exit()
    login(cursor)
    # flow starts here
    if role.lower() == 'professor':
        dashboard_prof(cursor)
        if action == "project":
            project(cursor)
            if action == "openproject":
                teamANDtask(cursor, PID=PID)
        elif action == "submission":
            submission(cursor)
        else:
            exit()
    else:
        student(cursor)
    


if __name__ == "__main__":
    main()