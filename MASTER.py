#from Inventory import *
from UI import *
import math
from Utility_Functions import *
import sqlite3
import hashlib, binascii, os
from prettytable import from_db_cursor
import datetime
import pytz

Logged_In = False
conn = sqlite3.connect("POS.db")
# Open a cursor to perform database operations
cur = conn.cursor()

#<<<LINE NUMBERS>>>#

#<<< Password Functions >>>#

#encrypt() = Line 46
#decrypt() = Line 55

#<<< On Start >>>#

#Login() = Line 68

#<<< UI Code >>>#

#Manage_Inventory() = Line 95
#Start() = Line 143
#Login() = Line 169

#<<<Account Management>>>#

#Password_Change() = Line 234
#User_List() = Line 360
#Add_User() = Line 371
#Delete_User() = Line 508

#<<<Inventory>>>#

#Inventory_List() = Line 586
#Add_Item() = Line 601
#Delete_Item() = Line 632
#Add_Removeq_Stocks() = Line 662


#<<<<<<<<<<< Password Functions >>>>>>>>>>>>>>#

def encrypt(password):

  """Hash a password for storing."""
  salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
  pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
  salt, 100000)
  pwdhash = binascii.hexlify(pwdhash)
  return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):

  """Verify a stored password against one provided by user"""
  salt = stored_password[:64]
  stored_password = stored_password[64:]
  pwdhash = hashlib.pbkdf2_hmac('sha512',
  provided_password.encode('utf-8'),
  salt.encode('ascii'),
  100000)
  pwdhash = binascii.hexlify(pwdhash).decode('ascii')
  return pwdhash == stored_password

#<<<<<<<<<<< On Start >>>>>>>>>>>>>>#

def Login():
    conn = sqlite3.connect("POS.db")
    cur = conn.cursor()
    global Account_Level
    global Account_Name
    global Logged_In
    Logged_In = False
    while Logged_In == False:
        print(LoginUI)
        print("Username: admin Password: test")
        Account_Name = str(input("Enter Username: "))
        Account_Password = str(input("Enter Password: "))
        if Account_Name == "RESET" and Account_Password == "RESET":
          cur.execute("DROP TABLE Order_History")
          cur.execute("CREATE TABLE IF NOT EXISTS Order_History (\
          ID INTEGER PRIMARY KEY,\
          Customer_Name TEXT,\
          Customer_Email TEXT,\
          Items TEXT,\
          Subtotal INTEGER,\
          Grandtotal INTEGER,\
          PromoCode TEXT,\
          Cashier_Name TEXT,\
          Date_Time\
          )")
          conn.commit()
          cls()
          Login()
        cur.execute("SELECT * FROM Accounts")
        record = cur.fetchall()
        for row in record:
            if Account_Name == row[0]:
                if verify_password(row[1], Account_Password):
                    Account_Level = row[2]
                    cls()
                    print("Login Successful!")
                    Logged_In = True
                    Start()
                    return
        cls()
        print("Login Unsuccessful!")



#<<<<<<<<<<< UI CODE >>>>>>>>>>>#


def Manage_Inventory():
  global Logged_In
  if Logged_In == False:
    print("You Cannot Run this function without logging in beforehand")
    quit()
    
  global Account_Level
  if Account_Level == 1 or Account_Level == 2:
        print(Inventory_Admin)
        Account_Menu = str(input("Input option: "))
        if Account_Menu == '1':
            cls()
            Inventory_List()
        elif Account_Menu == '2':
            cls()
            Add_Item()
        elif Account_Menu == '3':
            cls()
            Delete_Item()
        elif Account_Menu == '4':
            cls()
            Add_Remove_Stocks()
        elif Account_Menu == '5':
            cls()
            Activate_Deactivate()
        elif Account_Menu == '6':
          cls()
          Start()
        else:
            cls()
            print("Invalid Option!")
            Manage_Inventory()
  elif Account_Level == 3:
    print(Inventory_Normal)
    Account_Menu = str(input("Input option: "))
    if Account_Menu == '1':
      cls()
      Inventory_List()
    elif Account_Menu == '2':
      cls()
      Start()
    else:
      cls()
      print("Invalid Option!")
      Manage_Inventory()
  else:
    cls()
    print("ERROR: Cant get User Account Level")
    Start()


def Start():
    global Logged_In
    if Logged_In == False:
      print("You Cannot Run this function without logging in beforehand")
      quit()
    
    print(Startup)
    Start_menu = str(input("Input option: "))
    if Start_menu == '1':
        cls()
        New_Order_Start()

    elif Start_menu == '2':
        cls()
        Order_History()

    elif Start_menu == '3':
        cls()
        Manage_Inventory()
    elif Start_menu == '4':
        cls()
        Account_Management_Menu()
    elif Start_menu == '5':
        cls()
        print("Logout Successfully!")
        Login()
    else:
        cls()
        print("Invalid Option!")
        Start()


def Account_Management_Menu():
    global Logged_In
    
    if Logged_In == False:
      print("You Cannot Run this function without logging in beforehand")
      quit()
    

    if Account_Level == 1:
        print(Account_Management_Owner)
        Account_Menu = str(input("Input option: "))
        if Account_Menu == '1':
            cls()
            Password_Change()
        elif Account_Menu == '2':
            cls()
            User_List()
        elif Account_Menu == '3':
            cls()
            Add_User()
        elif Account_Menu == '4':
            cls()
            Delete_User()
        elif Account_Menu == '5':
            cls()
            Start()
        else:
            cls()
            print("Invalid Option!")
            Account_Management_Menu()
    elif Account_Level == 2:
        print(Account_Management_Admin)
        Account_Menu = str(input("Input option: "))
        if Account_Menu == '1':
            cls()
            Password_Change()
        elif Account_Menu == '2':
            cls()
            User_List()
        elif Account_Menu == '3':
            cls()
            Add_User()
        elif Account_Menu == '4':
            Delete_User()
        elif Account_Menu == '5':
            cls()
            Start()
        else:
            cls()
            print("Invalid Option!")
            Account_Management_Menu()
    elif Account_Level == 3:
        print(Account_Management_Normal)
        Account_Menu = str(input("Input option: "))
        if Account_Menu == '1':
            cls()
            Password_Change()
        elif Account_Menu == '2':
            cls()
            Start()
        else:
            cls()
            print("Invalid Option!")
            Account_Management_Menu()
    else:
        print("ERROR: Cant get User Account Level")
        exit()


#<<<<<<<<<<<ACCOUNT MANAGEMENT >>>>>>>>>>>>>>>#



def Password_Change():
    global Logged_In
    if Logged_In == False:
      print("You Cannot Run this function without logging in beforehand")
      quit()
    
    if Account_Level == 1:
        print(Password_Change_Owner)
        Password_Change_Menu = str(input("Input Option: "))
        if Password_Change_Menu == '1':
            Admin_Password = str(input("Key in Admin Password: "))
            cur.execute("SELECT * FROM Accounts;")
            record2 = cur.fetchall()
            for row in record2:
                if Account_Name == row[0]:
                    if verify_password(row[1], Admin_Password):
                        User = str(input("Input User for Password Change: "))
                        if not User.isalnum():
                          cls()
                          print("Username should only contain letters or numbers, No spacing")
                          Account_Management_Menu()
                        for row2 in record2:
                            if User == row2[0]:
                                New_Password = str(input("Type in your new password : "))
                                Retype = str(input("Retype your new password : "))
                                if New_Password != Retype:
                                    cls()
                                    print("New password does not match!")
                                    Password_Change()
                                else:
                                    New_Pass = encrypt(New_Password)
                                    cur.execute("UPDATE Accounts SET password = ? WHERE account_name = ?",
                                                (New_Pass, User))
                                    conn.commit()
                                    cls()
                                    print("Password Successfully Changed!")
                                    Password_Change()

                    else:
                        cls()
                        print("Invalid Admin Password!")
                        Password_Change()
            cls()
            print("Invalid User!")
            Password_Change()
        elif Password_Change_Menu == '3':
            cls()
            Account_Management_Menu()
        elif Password_Change_Menu != '2':
            cls()
            print("Invalid Option!")
            Password_Change()
    elif Account_Level == 2:
        print(Password_Change_Admin)
        Password_Change_Menu = str(input("Input Option: "))
        if Password_Change_Menu == '1':
            Admin_Password = str(input("Key in Admin Password: "))
            cur.execute("SELECT * FROM Accounts;")
            record2 = cur.fetchall()
            for row in record2:
                if Account_Name == row[0]:
                    if verify_password(row[1], Admin_Password):
                        User = str(input("Input User for Password Change: "))
                        for row2 in record2:
                            if User == row2[0]:
                                if row2[2] >= 3:

                                    New_Password = str(input("Type in your new password : "))
                                    Retype = str(input("Retype your new password : "))
                                    if New_Password != Retype:
                                        cls()
                                        print("New password does not match!")
                                        Password_Change()
                                    else:
                                        New_Pass = encrypt(New_Password)
                                        cur.execute("UPDATE Accounts SET password = ? WHERE account_name = ?",
                                                    (New_Pass, User))
                                        conn.commit()
                                        cls()
                                        print("Password Successfully Changed!")
                                        Password_Change()
                                else:
                                    cls()
                                    print("You do not have enough permission to change this user's password!")
                                    Password_Change()
                    else:
                        cls()
                        print("Invalid Admin Password!")
                        Password_Change()
            cls()
            print("Invalid User!")
            Password_Change()

        elif Password_Change_Menu == '3':
            cls()
            Account_Management_Menu()

        elif Password_Change_Menu != '2':
            cls()
            print("Invalid Option!")
            Password_Change()
    print("Do you want to change your password? (Y/N)")
    Password_Change_Option = str(input())
    if Password_Change_Option == "N":
        cls()
        Account_Management_Menu()
    elif Password_Change_Option != "Y":
        cls()
        print("Invalid Option!")
        Password_Change()
    Old_Password = str(input("Key in your old password : "))
    New_Password = str(input("Type in your new password : "))
    Retype = str(input("Retype your new password : "))
    cur.execute("SELECT * FROM Accounts;")
    record3 = cur.fetchall()
    for row in record3:
        if Account_Name == row[0]:
            if verify_password(row[1], Old_Password) == False:
                cls()
                print("Old Password Is Incorrect!")
                Account_Management_Menu()
            elif New_Password != Retype:
                cls()
                print("New password does not match!")
                Account_Management_Menu()
            else:
                New_Pass = encrypt(New_Password)
                cur.execute("UPDATE Accounts SET password = ? WHERE account_name = ?",(New_Pass, Account_Name))
                conn.commit()
                cls()
                print("Password Updated Successfully!")
                Account_Management_Menu()


def User_List():
    global Logged_In
    conn = sqlite3.connect("POS.db")
    cur = conn.cursor()
    if Logged_In == False:
      print("You Cannot Run this function without logging in beforehand")
      quit()
      
    cur.execute("SELECT account_name,account_level FROM Accounts")
    Table = from_db_cursor(cur)
    print(Table)
    Next = str(input("Key in any character to go back: "))
    cls()
    Account_Management_Menu()

def Add_User():
    global Logged_In
    conn = sqlite3.connect("POS.db")
    cur = conn.cursor()
    if Logged_In == False:
      print("You Cannot Run this function without logging in beforehand")
      quit()
    
    if Account_Level == 1:
        print("\n<User Add Console>")
        print(User_Add_Owner)
        Add_User_Option = str(input("Input: "))
        if Add_User_Option == "1":
            print("Input \"Q\" to quit adding Admin")

            Own_Password = str(input("\nKey in your own Password: "))
            if Own_Password == "Q":
                    cls()
                    Add_User()
            for row in record:
                    if Account_Name == row[0]:
                        if verify_password(row[1], Own_Password):
                            Add_Name = str(input("\nInput Admin Username: "))
                            Add_Password = str(input("\nInput Admin Password: "))
                            Retype = str(input("\nRetype Password: "))
                            if Add_Password != Retype:
                                cls()
                                print("Password does not match!")
                                Add_User()
                            else:
                                try:
                                  cur = conn.cursor()
                                  cur.execute("INSERT INTO Accounts (account_name, password, account_level) VALUES (?, ?, ?)",
                                 (Add_Name, encrypt(Add_Password), 2))
                                  conn.commit()
                                  cls()
                                  print("Admin Added Successfully!")
                                  Add_User()
                                except sqlite3.IntegrityError:
                                  cls()
                                  print("User Already Exists!")
                                  Add_User()
                        else:
                            cls()
                            print("Wrong Password!")
                            Add_User()


        elif Add_User_Option == "2":
                print("\nInput \"Q\" to quit adding User")

                Own_Password = str(input("\nKey in your own Password: "))
                if Own_Password == "Q":
                        cls()
                        Add_User()
                for row in record:
                        if Account_Name == row[0]:
                            if verify_password(row[1], Own_Password):
                                Add_Name = str(input("\nInput User Username: "))
                                Add_Password = str(input("\nInput User Password: "))
                                Retype = str(input("\nRetype Password: "))
                                if Add_Password != Retype:
                                    cls()
                                    print("Password does not match!")
                                    Add_User()
                                else:
                                  try:  
                                    cur = conn.cursor()
                                    cur.execute(
                                        "INSERT INTO Accounts (account_name, password, account_level) VALUES (?, ?, ?)",
                                        (Add_Name, encrypt(Add_Password), 3))
                                    conn.commit()
                                    cls()
                                    print("User Added Successfully!")
                                    Add_User()
                                  except sqlite3.IntegrityError:
                                    cls()
                                    print("User Already Exist!")
                                    Add_User()
                            else:
                                cls()
                                print("Wrong Password!")
                                Add_User()


        elif Add_User_Option == "3":
            cls()
            Account_Management_Menu()
        else:
            cls()
            print("Invalid Option!")
            Add_User()
    elif Account_Level == 2:
        print("<User Add Console>")
        print(User_Add_Admin)
        Add_User_Option = str(input("Input: "))
        if Add_User_Option == "1":
                print("\nInput \"Q\" to quit adding User")
                try:
                    Own_Password = str(input("\nKey in your own Password: "))
                    if Own_Password == "Q":
                        cls()
                        Add_User()
                    for row in record:
                        if Account_Name == row[0]:
                            if verify_password(row[1], Own_Password):
                                Add_Name = str(input("\nInput User Username: "))
                                Add_Password = str(input("\nInput User Password: "))
                                Retype = str(input("\nRetype Password: "))
                                if Add_Password != Retype:
                                    cls()
                                    print("Password does not match!")
                                    Add_User()
                                else:
                                    try:
                                      cur = conn.cursor()
                                      cur.execute(
                                        "INSERT INTO Accounts (account_name, password, account_level) VALUES (?, ?, ?)",
                                        (Add_Name, encrypt(Add_Password), 3))
                                      conn.commit()
                                      cls()
                                      print("User Added Successfully!")
                                      Add_User()
                                    except sqlite3.IntegrityError:
                                      cls()
                                      print("User Already Exist!")
                                      Add_User() 
                            else:
                                cls()
                                print("Wrong Password!")
                                Add_User()

                except:
                    cls()
                    print("Something went wrong....")
                    Add_User()
        elif Add_User_Option == "2":
            cls()
            Account_Management_Menu()
        else:
            cls()
            print("Invalid Option!")
            Add_User()

def Delete_User():
  global Logged_In
  if Logged_In == False:
    print("You Cannot Run this function without logging in beforehand")
    quit()
    
  cls()
  print("<<<<<<<<<<<User Delete Console>>>>>>>>>>>>")
  User_To_Delete = str(input("\nInput Username of User to delete: "))
  if Account_Level == 1:
    Own_Password = str(input("\nKey in your own Password: "))
    for row in record:
      if Account_Name == row[0]:
        if verify_password(row[1], Own_Password):
          for row2 in record:
            if row2[0] == User_To_Delete:
              if Account_Name != User_To_Delete:
                print("\nYou are about to delete the User",User_To_Delete,"Type CONFIRM to confirm delete, Type in any character to stop deleting User")
                User_Confirmation = str(input("\nInput: "))
                if User_Confirmation == "CONFIRM":
                  sql = 'DELETE FROM Accounts WHERE account_name=?'
                  cur.execute(sql, (User_To_Delete,))
                  conn.commit()
                  cls()
                  print("Account Deleted!")
                  Account_Management_Menu()
                else:
                  cls()
                  Account_Management_Menu()
              else:
                cls()
                print("You cant delete your own account!")
                Account_Management_Menu()          
          cls()
          print("User Not Found!")
          Account_Management_Menu()
        else:
          cls()
          print("Wrong Password!")
          Account_Management_Menu()
  
  elif Account_Level == 2:
    Own_Password = str(input("\nKey in your own Password: "))
    for row in record:
      if Account_Name == row[0]:
        if verify_password(row[1], Own_Password):
          for row2 in record:
            if row2[0] == User_To_Delete:
              if Account_Name != User_To_Delete:
                if row2[2] >= 3:
                  print("\nYou are about to delete the User",User_To_Delete,"Type CONFIRM to confirm delete, Type in any character to stop deleting User")
                  User_Confirmation = str(input("\nInput: "))
                  if User_Confirmation == "CONFIRM":
                    sql = 'DELETE FROM Accounts WHERE account_name=?'
                    cur.execute(sql, (User_To_Delete,))
                    conn.commit()
                    cls()
                    print("Account Deleted!")
                    Account_Management_Menu()
                  else:
                    cls()
                    Account_Management_Menu()
                else:
                  cls()
                  print("You do not have enough permissions to delete this account.")
                  Account_Management_Menu()          
              else:
                cls()
                print("You cant delete your own Account!.")
                Account_Management_Menu()
          
          cls()
          print("User not Found!")
          Account_Management_Menu()
        else:
          cls()
          print("Wrong Password!")
          Account_Management_Menu()
          


#<<<<<<<<<<<<<<<<<<<<INVENTORY>>>>>>>>>>>>>>>>>>>>>>>>

def Inventory_List():
  global Logged_In
  if Logged_In == False:
    print("You Cannot Run this function without logging in beforehand")
    quit()
    
  
  conn = sqlite3.connect("POS.db")
  cur = conn.cursor()
  cur.execute("SELECT * FROM Inventory")

    
  Table = from_db_cursor(cur)
  print(Table)
  
  User_Input = str(input("Enter any character to exit: "))
  cls()
  Manage_Inventory()

def Add_Item():
  global Logged_In
  if Logged_In == False:
    print("You Cannot Run this function without logging in beforehand")
    quit()
    
  conn = sqlite3.connect("POS.db")
  cur = conn.cursor()
  Active = "False"
  Item_To_Add = str(input("\nInput name of Item to add: "))
  cur.execute("SELECT * FROM Inventory")
  records = cur.fetchall()
  for row in records:
    if row[0] == Item_To_Add:
      cls()
      print("Item already exists!")
      Manage_Inventory()
  Item_Price = str(input("\nInput Price of Item:$ "))
  Item_Stock = str(input("\nInput Stock of Item: "))
  
  if not Item_Price.isdigit() or not Item_Stock.isdigit():
    cls()
    print("Fields is/are empty")
    Manage_Inventory()

  try:
    Item_Price = float(Item_Price)
    Item_Price = float(Item_Price)
  except:
    cls()
    print("Item Price/Stocks Must be a number")
  cur.execute("INSERT INTO Inventory (Item_Name, Price, Stocks, Active) VALUES (?, ?, ?, ?)",(Item_To_Add,Item_Price,Item_Stock,Active))
  conn.commit()
  cls()
  print("Item Added!")
  Manage_Inventory()

def Delete_Item():
  global Logged_In
  if Logged_In == False:
    print("You Cannot Run this function without logging in beforehand")
    quit()
    
  conn = sqlite3.connect("POS.db")
  cur = conn.cursor()
  cur.execute("SELECT * FROM Inventory")
  
  Table = from_db_cursor(cur)
  print(Table)

  Item_To_Delete = str(input("\nInput name of Item to delete: "))
  cur.execute("SELECT * FROM Inventory")
  records = cur.fetchall()
  for row in records:
    if row[0] == Item_To_Delete:
      Confirmation = str(input("This item will be deleted, Enter CONFIRM to Confirm: "))
      if Confirmation == "CONFIRM":
        sql = 'DELETE FROM Inventory WHERE Item_Name=?'
        cur.execute(sql, (Item_To_Delete,))
        conn.commit()
        cls()
        print("Item Deleted.")
        Manage_Inventory()
      else:
        cls()
        print("Item Deletion Cancelled.")
        Manage_Inventory()
  cls()
  print("Item Not Found")
  Manage_Inventory()

def Add_Remove_Stocks():
  global Logged_In
  if Logged_In == False:
    print("You Cannot Run this function without logging in beforehand")
    quit()
    
  conn = sqlite3.connect("POS.db")
  cur = conn.cursor()
  cur.execute("SELECT * FROM Inventory")
  records = cur.fetchall()
  Item_Name = str(input("\nInput Name of Item: "))
  Stocks_To_Add = str(input("\nInput number of stocks to add,Input negative number to remove: "))
  try:
    Stocks_To_Add = int(Stocks_To_Add)
  except:
    cls()
    print("Stocks to add must be an integer!")
    Manage_Inventory()
  for row in records:
    if row[0] == Item_Name:
      Number = row[2] + Stocks_To_Add
      cur.execute("UPDATE Inventory SET Stocks = ? WHERE Item_Name = ? ",(Number,Item_Name))
      conn.commit()
      cls()
      print("Stocks added/removed succesfully!")
      Manage_Inventory()
  cls()
  print("Item not found!")
  Manage_Inventory()

def Activate_Deactivate():
  global Logged_In
  if Logged_In == False:
    print("You Cannot Run this function without logging in beforehand")
    quit()
    
  conn = sqlite3.connect("POS.db")
  cur = conn.cursor()
  cur.execute("SELECT * FROM Inventory")
  Table = from_db_cursor(cur)
  print(Table)
  cur.execute("SELECT * FROM Inventory")
  records = cur.fetchall()
  Item_Name = str(input("Input Item Name to Activate/Deactivate: "))
  for row in records:
    if row[0] == Item_Name:
      Option = str(input("Input 1 to Activate and 2 to Deactivate: "))

      
      while True:
        if Option == "1" or Option == "2":
          break
        else:
          print("\nInvalid Input!")
          Option = str(input("Input 1 to Activate and 2 to Deactivate"))
      
      if Option == "1":
        cur.execute("UPDATE Inventory SET Active = ? WHERE Item_Name = ?",("True",Item_Name))
        conn.commit()
        cls()
        print("Item Activated")
        Manage_Inventory()
      elif Option == "2":
        cur.execute("UPDATE Inventory SET Active = ? WHERE Item_Name = ?",("False",Item_Name))
        conn.commit()
        cls()
        print("Item Deactivated.")
        Manage_Inventory()
      else:
        print("Invalid Input,Wait if you got here data validation failed.")
  cls()
  print("Item Not found!")
  Manage_Inventory()
        

def New_Order_Start():
    global Account_Name
    conn = sqlite3.connect("POS.db")
    cur = conn.cursor()    
    
    cur.execute("SELECT * FROM Temp_Order_History WHERE Account_Name = ?",(Account_Name,))
    Exist = cur.fetchone()
    if Exist is None:
      cur.execute("INSERT OR IGNORE INTO Temp_Order_History (Account_Name,Customer_Name,Customer_Email,Added_Items,Subtotal) VALUES (?,?,?,?,?)",(Account_Name,"","","",0,))
      conn.commit()
    cur.execute("SELECT * FROM Temp_Order_History WHERE Account_Name = ?",(Account_Name,))
    records = cur.fetchall()
    if records[0][1] == "":
      Done1 = "✖"
    else:
      Done1 = "✓"
    if records[0][2] == "":
      Done2 = "✖"
    else:
      Done2 = "✓"
    if records[0][3] == "":
      Done3 = "✖"
    else:
      Done3 = "✓"
    print("<<<<<<<<<<<>>>>>>>>>>>>")
    print("[1] Input Customer Name(Optional)","[",Done1,"]")
    print("[2] Input Customer Email(Optional)","[",Done2,"]")
    print("[3] Input Items","[",Done3,"]")
    print("[4] Checkout")
    print("[5] Clear Inputs")
    print("[6] Back")
    print("<<<<<<<<<<<>>>>>>>>>>>>")
    Option = str(input("Input Option: "))
    if Option == "1":
      cls()
      Input_Customer_Name()
    elif Option == "2":
      cls()
      Input_Customer_Email()
    elif Option == "3":
      cls()
      Input_Items()
    elif Option == "4":
      cls()
      Checkout()
    elif Option == "5":
      cls()
      Clear_Inputs()
    elif Option == "6":
      cls()
      Start()
    else:
      cls()
      print("Invalid Input!")
      New_Order_Start()
  
def Input_Customer_Name():
    global Account_Name
    conn = sqlite3.connect("POS.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Temp_Order_History")
    records = cur.fetchall()
    print("Inputed Customer Name:",records[0][1])
    Customer_Name = str(input("Input Customer Name, Leave blank to exit: "))
    if not Customer_Name == "":
      cur.execute("UPDATE Temp_Order_History SET Customer_Name = ? WHERE Account_Name = ?",(Customer_Name,Account_Name,))
      conn.commit()

    cls()
    New_Order_Start()

def Input_Customer_Email():
    global Account_Name
    conn = sqlite3.connect("POS.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Temp_Order_History")
    records = cur.fetchall()
    print("Inputed Customer Email:",records[0][2])
    Customer_Email = str(input("Input Customer Email, Leave blank to exit: "))
    
    if check(Customer_Email) == "Invalid":
      Customer_Email = ""
      cur.execute("UPDATE Temp_Order_History SET Customer_Email = ? WHERE Account_Name = ?",(Customer_Email,Account_Name,))
      
      conn.commit()
      cls()
      print("Invalid Email!")
      New_Order_Start()
    elif not Customer_Email == "":
      cur.execute("UPDATE Temp_Order_History SET Customer_Email = ? WHERE Account_Name = ?",(Customer_Email,Account_Name,))
      conn.commit()
    
    cls()
    New_Order_Start()

def Input_Items():
    global Account_Name
    conn = sqlite3.connect("POS.db")
    cur = conn.cursor()
    cur.execute("SELECT Added_Items FROM Temp_Order_History WHERE Account_Name = ?",(Account_Name,))
    print(from_db_cursor(cur))
    print(Input_Item_UI)
    Option = str(input("Input: "))
    if Option == "1":
      cls()
      cur.execute("SELECT Item_Name,Price FROM Inventory WHERE Active = 'True'")
      print(from_db_cursor(cur))
      Item_To_Add = str(input("Input Item to add: "))
      Quantity = str(input("Input Quantity: "))
      cur.execute("SELECT * FROM Inventory")
      records = cur.fetchall()
      for row in records:
        if Quantity.isnumeric() and int(Quantity) > 0:
          if row[0] == Item_To_Add:
            
            cur.execute("SELECT Stocks FROM Inventory WHERE Item_Name = ?",(Item_To_Add,))
            
            Stocks = cur.fetchall()
            
            cur.execute("SELECT Active FROM Inventory WHERE Item_Name = ?",(Item_To_Add,))
            
            Active = cur.fetchall()
            if Active[0][0] == "False":
              cls()
              print("Item is not Activated!")
              Input_Items()
            elif int(Stocks[0][0]) - int(Quantity) >= 0:
              cur.execute("SELECT Changes FROM Temp_Stocks_Changes WHERE Item_Name = ? AND Account_Name = ?",(Item_To_Add,Account_Name,))
              
              record = cur.fetchall()
              
              Temp_Change = 0
              
              for row2 in record:
                Temp_Change -= int(row2[1])
              
              print("\n",Item_To_Add,"has",int(Stocks[0][0]) - int(Quantity) - Temp_Change,"Stocks left")
              
              cur.execute("INSERT INTO Temp_Stocks_Changes (Account_Name,Item_Name,Changes) VALUES (?,?,?)",(Account_Name,Item_To_Add,"-"+Quantity))

              cur.execute("SELECT Added_Items FROM Temp_Order_History WHERE Account_Name = ?",(Account_Name,))
              
              record = cur.fetchall()
              
              Items = record[0][0]
              
              cur.execute("SELECT DISTINCT Item_Name FROM Temp_Stocks_Changes WHERE Account_Name = ?",(Account_Name,))
              
              Unique_Items = cur.fetchall()
              Item_To_DB = ""
              for Item in Unique_Items:
                cur.execute("SELECT * FROM Temp_Stocks_Changes WHERE Item_Name = ? AND Account_Name = ?",(Item[0],Account_Name,))
                
                record3 = cur.fetchall()
                
                Quantity1 = 0
                
                for row3 in record3:
                
                  Quantity1 -= int(row3[2])
                
                Item_To_DB += Item[0] + " " + str(Quantity1) + "x\n"
              
              cur.execute("UPDATE Temp_Order_History SET Added_Items = ? WHERE Account_Name = ?",(Item_To_DB,Account_Name,))

              Price = int(row[1])*int(Quantity)
              
              cur.execute("UPDATE Temp_Order_History SET Subtotal = Subtotal + ? WHERE Account_Name = ?",(Price,Account_Name,))
              
              conn.commit()
              Next = str(input("\nInput any character to continue: "))
              cls()
              Input_Items()
            else:
              print("There isn't enough stocks for this item! Add Anyways?")
              while True:
                Next = str(input("Y/N: "))
                if Next == "Y":
                  cur.execute("SELECT Changes FROM Temp_Stocks_Changes WHERE Item_Name = ? AND Account_Name = ?",(Item_To_Add,Account_Name,))
              
                  record = cur.fetchall()
              
                  Temp_Change = 0
              
                  for row2 in record:
                    Temp_Change -= int(row2[1])
              
                  print("\n",Item_To_Add,"has",int(Stocks[0][0]) - int(Quantity) - Temp_Change,"Stocks left")
                  
                  cur.execute("SELECT Added_Items FROM Temp_Order_History WHERE Account_Name = ?",(Account_Name,))

                  record = cur.fetchall()
                  
                  Items = record[0][0]
                  

              

              
                  cur.execute("INSERT INTO Temp_Stocks_Changes (Account_Name,Item_Name,Changes) VALUES (?,?,?)",(Account_Name,Item_To_Add,"-"+Quantity))
              
                  cur.execute("SELECT DISTINCT Item_Name FROM Temp_Stocks_Changes WHERE Account_Name = ?",(Account_Name,))
              
                  Unique_Items = cur.fetchall()
                  Item_To_DB = ""
                  for Item in Unique_Items:
                    cur.execute("SELECT * FROM Temp_Stocks_Changes WHERE Item_Name = ? AND Account_Name = ?",(Item[0],Account_Name,))
                    
                    record3 = cur.fetchall()
                    
                    Quantity1 = 0
                    
                    for row3 in record3:
                    
                      Quantity1 -= int(row3[2])
                    
                    Item_To_DB += Item[0] + " " + str(Quantity1) + "x\n"
              
                  cur.execute("UPDATE Temp_Order_History SET Added_Items = ? WHERE Account_Name = ?",(Item_To_DB,Account_Name,))
                  
                  Price = int(row[1])*int(Quantity)
              
                  cur.execute("UPDATE Temp_Order_History SET Subtotal = Subtotal + ? WHERE Account_Name = ?",(Price,Account_Name,))
              
                  conn.commit()
                  
                  Next = str(input("\nInput any character to continue: "))
                  
                  cls()
                  Input_Items()
                elif Next == "N":
                  cls()
                  Input_Items()
                  break
                else:
                  cls()
                  print("Invalid Input!")
        else:
          cls()
          print("Quantity must be a positive Integer!")
          Input_Items()       
      cur.execute("SELECT * FROM Inventory WHERE Active = \"True\" AND Item_Name LIKE ? ",('%'+Item_To_Add+'%',))
      records = cur.fetchall()
      print("No such item, Did you mean")
      for row in records:
        print(row[0])
      Next = str(input("Input any chracter to continue: "))
      cls()
      Input_Items()
    elif Option == "2":
      cls()
      cur.execute("SELECT Added_Items FROM Temp_Order_History WHERE Account_Name = ?",(Account_Name,))
      print(from_db_cursor(cur))
      Item_To_Remove = str(input("Input Name Of Item To Remove: "))
      cur.execute("SELECT DISTINCT Item_Name FROM Temp_Stocks_Changes WHERE Account_Name = ?",(Account_Name,))
      records = cur.fetchall()
      for row in records:
        if row[0] == Item_To_Remove:
          cur.execute("SELECT Changes FROM Temp_Stocks_Changes WHERE Item_Name = ? AND Account_Name = ?",(Item_To_Remove,Account_Name,))
          record2 = cur.fetchall()
          num = 0
          for row2 in record2:
            num -= int(row2[1])
          if num != 0:
            Quantity = str(input("Input Number Of Items to Remove: "))
            if Quantity.isnumeric() and int(Quantity) > 0:
              cur.execute("INSERT INTO Temp_Stocks_Changes (Account_Name,Item_Name,Changes) VALUES (?,?,?)",(Account_Name,Item_To_Remove,Quantity,))
              conn.commit()
              Item_To_DB = ""
              for Item in records:
                cur.execute("SELECT * FROM Temp_Stocks_Changes WHERE Item_Name = ? AND Account_Name = ?",(Item[0],Account_Name,))
                      
                record3 = cur.fetchall()
                      
                Quantity1 = 0
                      
                for row3 in record3:      
                  Quantity1 -= int(row3[2])
                if Quantity1 == 0:
                  Item_To_DB += ""
                else:
                  Item_To_DB += Item[0] + " " + str(Quantity1) + "x\n"
                
              cur.execute("UPDATE Temp_Order_History SET Added_Items = ? WHERE Account_Name = ?",(Item_To_DB,Account_Name,))
              conn.commit()
              cls()
              Input_Items()
            else:
              cls()
              print("Quantity must be a positive Integer!")
              Input_Items()
          else:
            cls()
            print("Item does not exist!")
            Input_Items()
      cls()
      print("Item does not exist!")
      Input_Items()  
    elif Option == "3":
      cls()
      New_Order_Start()
    else:
      cls()
      print("Invalid Input")
      Input_Items()

def Checkout():
    global Account_Name
    cur.execute("SELECT * FROM Temp_Order_History WHERE Account_Name = ?",(Account_Name,))
    records = cur.fetchall()
    if records[0][3] == "":
      cls()
      print("No Items To Checkout!")
      New_Order_Start()
    
    
    cur.execute("SELECT Subtotal FROM Temp_Order_History WHERE Account_Name = ?",(Account_Name,))
    Subtotal = cur.fetchall()
    Subtotal = Subtotal[0][0]
    Item_To_DB = ""
    print("Subtotal:$",int(Subtotal))
    #Promo_Option = str(input("Have a Promo Code?[Y/N]: "))
    #if Promo_Option == "Y":
    #  print("TBC")
    #else:
    #  Grand_Total = Subtotal
    
    #<Receipt goes here>#
    
    
    Confirmation = str(input("Type in CONFIRM to Checkout: "))
    if Confirmation == "CONFIRM":
      
      cur.execute("SELECT * FROM Temp_Order_History WHERE Account_Name = ?",(Account_Name,))
      
      records = cur.fetchall()
      
      sgt = pytz.timezone('Asia/Singapore')
      
      time = datetime.datetime.now(tz=sgt)
      cur.execute("SELECT DISTINCT Item_Name FROM Temp_Stocks_Changes WHERE Account_Name = ?",(Account_Name,))
      Unique_Items = cur.fetchall()
      for Item in Unique_Items:
        cur.execute("SELECT * FROM Temp_Stocks_Changes WHERE Item_Name = ? AND Account_Name = ?",(Item[0],Account_Name,))
        record3 = cur.fetchall()
        Quantity = 0
        for row3 in record3:
          Quantity -= int(row3[2])
        Item_To_DB += Item[0] + " " + str(Quantity) + "x\n"
            
      cur.execute("INSERT INTO Order_History (Customer_Name,Customer_Email,Items,Subtotal,Grandtotal,PromoCode,Cashier_Name,Date_Time) VALUES (?,?,?,?,?,?,?,?)",(records[0][1],records[0][2],Item_To_DB,Subtotal,Subtotal,"test",Account_Name,str(time)[:16],))

      
      cur.execute("SELECT * FROM Temp_Stocks_Changes WHERE Account_Name = ?",(Account_Name,))
        
      record2 = cur.fetchall()
        
      Change = 0
              
      for row2 in record2:
        Change -= int(row2[2])
        cur.execute("UPDATE Inventory SET Stocks = Stocks - ? WHERE Item_Name = ?",(Change,row2[0],))
        Change = 0
      

      
      cur.execute("DELETE FROM Temp_Order_History WHERE Account_Name = ?",(Account_Name,))
      
      cur.execute("DELETE FROM Temp_Stocks_Changes WHERE Account_Name = ?",(Account_Name,))

      conn.commit()
      
      cls()
      
      print("Order Checked Out!")
      
      New_Order_Start()
    else:
      New_Order_Start()
#UPDATE (table) SET (column = ) WHERE (column = )

def Order_History():
  cur.execute("SELECT * FROM Order_History")
  print(from_db_cursor(cur))
  Next = str(input("Input any chracter to continue: "))
  cls()
  Start()

def Clear_Inputs():
  global Account_Name
  confirm = str(input("Type CONFIRM to clear all inputs: "))
  if confirm == "CONFIRM":
    cur.execute("DELETE FROM Temp_Order_History WHERE Account_Name = ?",(Account_Name,))
      
    cur.execute("DELETE FROM Temp_Stocks_Changes WHERE Account_Name = ?",(Account_Name,))
    conn.commit()
    
    conn.commit()
    cls()
    print("Inputs Cleared!")
    New_Order_Start()
  else:
    cls()
    print("Inputs Clearing Not Confirmed, Returning...")
    New_Order_Start()






'''
sgt = pytz.timezone('Asia/Singapore')
time = datetime.datetime.now(tz=sgt)
current_day = str(time)[8:10]
print(str(time)[:16])f
'''