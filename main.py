import os

from UI import *
import sqlite3
from Utility_Functions import *
from MASTER import *
from prettytable import from_db_cursor
#from Inventory import *
Logged_In = False
conn = sqlite3.connect("POS.db")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS Accounts (\
	Account_name TEXT PRIMARY KEY,\
	Password TEXT,\
	Account_level INTEGER\
)")

cur.execute("INSERT OR IGNORE INTO Accounts(account_name, password, account_level) VALUES('admin',?,1)",(encrypt('test'),))



cur.execute("CREATE TABLE IF NOT EXISTS Inventory (\
	Item_Name TEXT PRIMARY KEY,\
	Price INTEGER,\
	Stocks INTEGER,\
  Active TEXT\
)")

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

cur.execute("CREATE TABLE IF NOT EXISTS Temp_Order_History (\
	ID INTEGER PRIMARYKEY,\
  Customer_Name TEXT,\
	Customer_Email TEXT,\
  Added_Items TEXT,\
  Subtotal INTEGER\
)")
cur.execute("SELECT * FROM Temp_Order_History WHERE ID = 0")
Exist = cur.fetchone()
if Exist is None:
  cur.execute("INSERT OR IGNORE INTO Temp_Order_History (ID,Customer_Name,Customer_Email,Added_Items,Subtotal) VALUES (?,?,?,?,?)",(0,"","","",0,))

cur.execute("CREATE TABLE IF NOT EXISTS Stocks_Changes (\
	ID INTEGER PRIMARYKEY,\
  Item_Name TEXT,\
	Changes TEXT,\
  Date TEXT,\
  Time TEXT\
)")

cur.execute("CREATE TABLE IF NOT EXISTS Temp_Stocks_Changes (\
  Item_Name TEXT,\
	Changes TEXT\
)")


cur.execute("CREATE TABLE IF NOT EXISTS Promo_Codes (\
	ID INTEGER PRIMARYKEY,\
  Promo_Code TEXT,\
	Expiry_Date TEXT,\
  Date_Added TEXT,\
  Active TEXT\
)")

conn.commit()

Login()

#TO READ https://stackoverflow.com/questions/51183321/how-to-use-paging-with-sqlite

# TO READ https://www.sqlitetutorial.net/sqlite-limit/


# CHANGELOGS: Even more Bug fixes
# CHANGELOGS: Changed how order_history represented data
# CHANGELOGS: Date Time for oder_History



#TODO ***DATA VALIDATION***

#TODO *** SLIDES ***

#TODO LIST SORTING

#TODO REMOVE ITEM FROM BASKET **

#TODO PROMO CODE **

#TODO GRAND TOTAL[New Order] **




#TODO E Receipt System(Not impt)

#Last Updated 10.58pm 7/28/2020

#Backuped to drive Not


"""
<<<<<<<<<<<<>>>>>>>>>>>
[1] Inventory List      
[2] Add New Item
[3] Delete Item
[4] Add Inventory
[5] Delete Inventory
[6] Back
<<<<<<<<<<<<>>>>>>>>>>>

"""
