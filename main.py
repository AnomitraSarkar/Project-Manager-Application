import csv
import time
import tabulate
import mysql.connector
import pyautogui as pag
from tkinter import *
import customtkinter
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
        elif action == "submission":
            print("Starting Submission Panel")
        else:
            exit()
    


if __name__ == "__main__":
    main()