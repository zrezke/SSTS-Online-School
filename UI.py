'''
This file is made to work inside of Scraper.py. 
It just gets login info from the user, to pass it on to Selenium.
'''

from tkinter import *
import os


#  make a tkinter window
root = Tk()
root.geometry("360x100")
root.title("Arnes AAI")
root.resizable(0, 0)
root.configure(bg="#333")

#  some labels
signIn = Label(root, fg="#fff", bg="#333", text="Sign in: ", font=("Times", 16))
signIn.grid(row=1, ipady=2, ipadx=2)

usernameStringVar = StringVar()
passwordStringVar = StringVar()

signInEntry = Entry(root, font=("Times", 16), textvariable=usernameStringVar)
passwordEntry = Entry(root, font=("Times", 16), show="*", textvariable=passwordStringVar)

#  checkes for remembered login info and inserts it
rememberMe = open(r"rememberMe.txt", "r")
firstReadLine = rememberMe.readline(1)
if firstReadLine == "1":
    rememberMe.readline()
    usernameStringVar = rememberMe.readline()
    passwordStringVar = rememberMe.readline()
    signInEntry.insert(0, usernameStringVar)
    passwordEntry.insert(0, passwordStringVar)
    rememberMe.close()

#  some more labels and adding stuff to grid
signInEntry.grid(row=1, column=1)
passwordLabel = Label(root, fg="#fff", bg="#333", text="Password: ", font=("Times", 16))
passwordLabel.grid(row=2, column=0, padx=10)
passwordEntry.grid(row=2, column=1)


#  if checkBox is checked get_checkbox_val() will write sign in info into rememberMe.txt
def get_checkbox_val():
    textFile = open(r"rememberMe.txt", "r+")
    firstLine = textFile.readline()
    secondLine = textFile.readline()

    if secondLine == "":
        data = checkBoxSelect.get()
        textFile.seek(0)
        textFile.write(str(data)+ "\r")
        textFile.write(str(usernameStringVar.get()) + "\r")
        textFile.write(str(passwordStringVar.get()))
        textFile.close()
        sys.exit()
    else:
        sys.exit()


checkBoxSelect = IntVar()
checkBox = Checkbutton(root, text="Remember me", bg="#333", fg="#0fff00", variable=checkBoxSelect, onvalue=1, offvalue=0)
checkBox.deselect()
checkBox.grid(row=3, column=1, sticky=W)
signInBtn = Button(root, bg="#333", fg="#00ff00", text="Sign in", 
    command=lambda: get_checkbox_val())
signInBtn.grid(row=3, column=0)
root.mainloop()
