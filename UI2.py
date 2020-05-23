'''
This file is meant to work inside of Scraper.py.
It represents the UI of the Application.
'''


from tkinter import *
import threading

main = Tk()
main.title("ArnesAAI")
xCoordinate = main.winfo_screenwidth()/2 - 360
yCoordinate = main.winfo_screenheight()/2 - 250
main.geometry("%dx%d+%d+%d" % (720, 500, xCoordinate, yCoordinate))
main.configure(bg="#e7e7e7")
main.resizable(0, 0)


menu = Frame(main, width=main.winfo_screenwidth(), height=36, bg="#fff").place(relx=0.5, anchor=N)

btnColor = "#fff"

buttons = {
    1:"homeBtn",
    2:"novoBtn",
    3:"gradivoBtn",
    4:"nalogeBtn",
    5:"oddanoBtn"
}

#  had to take the button in as a string, otherwise it is considered unasigned
def on_widget_color(buttonNameAsString):
    for i in buttons:
        setToFFF = eval(buttons[i])
        setToFFF.configure(bg="#fff")

    button = eval(buttonNameAsString)
    btnColor = "#f4f4f4"
    button.configure(bg=btnColor)

homeBtn = Button(menu,
            bg=btnColor,
            fg="#333", 
            text="Home", 
            font=("Times", 16), 
            border=0, 
            height=0, 
            command=lambda: on_widget_color(buttons[1]))

novoBtn = Button(menu,
            bg=btnColor,
            fg="#333",
            font=("Times", 16),
            border=0,
            height=0,
            text="Novo",
            padx=10,
            command=lambda: on_widget_color(buttons[2]))

gradivoBtn = Button(menu,
            bg=btnColor,
            fg="#333", 
            text="Gradivo", 
            font=("Times", 16), 
            border=0, 
            height=0, 
            command=lambda: on_widget_color(buttons[3]))

nalogeBtn = Button(menu,
            bg=btnColor,
            fg="#333", 
            text="Naloge", 
            font=("Times", 16), 
            border=0, 
            height=0, 
            command=lambda: on_widget_color(buttons[4]))

oddanoBtn = Button(menu,
            bg=btnColor,
            fg="#333", 
            text="Oddano", 
            font=("Times", 16), 
            border=0, 
            height=0, 
            command=lambda: on_widget_color(buttons[5]))

homeBtn.grid(row=0, column=1, padx=35, sticky=W)
novoBtn.grid(row=0, column=2, padx=35, sticky=W)
gradivoBtn.grid(row=0, column=3, padx=35, sticky=W)
nalogeBtn.grid(row=0, column=4, padx=35, sticky=W)
oddanoBtn.grid(row=0, column=5, padx=35, sticky=W)

universalFrame = Frame(main, bg="#333", width=720, height=464)
universalFrame.place(relx=0, rely=0.072)
var="Hello user!"
helloUserLabel = Label(universalFrame,
                        bg="#e7e7e7",
                        fg="#333",
                        text=var,
                        font=("Times", 15))

helloUserLabel.grid(row=0, column=0, padx=(360-(0.3528*15*len(var))))
main.mainloop()