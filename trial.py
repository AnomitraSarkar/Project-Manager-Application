import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5 import uic

def main():
    global db
    db = mysql.connector.connect(host="localhost",user="root",password=f"root", database="flowdata")
        
    cursor = db.cursor()
    return cursor



c = main()

class Project(QMainWindow):
    def __init__(self, cursor):
        global action
        super(Project, self).__init__()
        uic.loadUi("project.ui", self)
        self.show()