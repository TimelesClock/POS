import replit
import re #re module provides support for regular expressions


def cls(): #Clear Screen Function
    replit.clear()

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$' #A regular expression for validating an email

def check(email):  
  
    # pass the regular expression 
    # and the string in search() method 
    if(re.search(regex,email)):  
        return("Valid")  
          
    else:  
        return("Invalid")