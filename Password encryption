" Password validity check maybe convert this program into a password storage system"
" Password should contain [a-z],[0-9],[A-Z] and [!@#$%&]"

from Crypto import Random
from Crypto.Random import random
from Crypto.PublicKey import ElGamal
from Crypto.Util.number import GCD
from Crypto.Hash import SHA

import string

#print ("Enter password that contains atleast [a-z],[0-9],[A-Z] and [!@#$%&]")
#password = input(" Enter password : ")

lower_case = list(string.ascii_lowercase)
upper_case = list(string.ascii_uppercase)
digits = list(string.digits)
special_characters = list(string.punctuation)
the_list = ["Ale","Bale","Cale","Comale","Pale","Xale"]
design ={}

def password_cycle(the_list):
    for word in range(len(the_list)):
        print (f"Enter password for {the_list[word]} that contains atleast [a-z],[0-9],[A-Z] and [!@#$%&]")
        password = input(" Enter password : ")
        check_validity(password)
        design[the_list[word]] = password

def check_validity(password):
    lower_char = 0
    upper_char = 0
    digit_count = 0
    special_count = 0
    if len(password)<6 or len(password)>12:
        print(f"Current password length {len(password)}")
        print("Password length should be between 6 to 12 characters")
        password = input("Enter password : ")
        check_validity(password)
    for i in range(len(password)):
        if password[i] in lower_case:
            lower_char = lower_char+1
        elif password[i] in upper_case:
            upper_char = upper_char+1
        elif password[i].isdigit():
            digit_count = digit_count+1
        elif password[i] in special_characters:
            special_count = special_count+1
    if lower_char !=0 and upper_char !=0 and digit_count !=0 and special_count !=0:
        print (" Password is good")
    elif  lower_char ==0:
        print ("Password doesnt contain [a..z] character")
        password = input("Enter password : ")
        check_validity(password)
    elif upper_char ==0:
        print ("Password doesnt contain [A..Z] character")
        password = input("Enter password : ")
        check_validity(password)
    elif digit_count ==0:
        print ("Password doesnt contain [0-9] character")
        password = input("Enter password : ")
        check_validity(password)
    elif special_count ==0:
        print ("Password doesnt contain special character")
        password = input("Enter password : ")
        check_validity(password)

#check_validity(password)
password_cycle(the_list)
