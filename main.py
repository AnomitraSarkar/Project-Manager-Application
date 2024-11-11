import csv
import time
import tabulate
import mysql.connector
import pyautogui
from tkinter import *
import customtkinter

def connect_and_cursor(password):
    conn = mysql.connector.connect(host="localhost",user="root",password=f"{password}")
    if(conn):
        print("Connection succesful")
    else:   
        print("Connection failed")
    return conn.cursor

def app():
    print("Running application")

def initialize():
    print("Enter password")

def backups():
    print("Backing up database")

def main():
    connect_and_cursor("root")
    app()


if __name__ == "__main__":
    main()