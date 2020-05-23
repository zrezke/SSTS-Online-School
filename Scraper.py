import selenium
from selenium import webdriver
from tkinter import *
import os
import threading


#  login tkinter ------------------------------------------------------------------------------------------------
for i in range(1):
    #  make a tkinter window
    root = Tk()
    xCoordinate = root.winfo_screenwidth()/2 - 180
    yCoordinate = root.winfo_screenheight()/2 - 50
    root.geometry("%dx%d+%d+%d" % (360, 100, xCoordinate, yCoordinate))
    root.title("Arnes AAI")
    root.resizable(0, 0)
    root.configure(bg="#333")

    #  protocol on exit
    root.protocol("WM_DELETE_WINDOW", sys.exit)
        
    #  some labels
    signIn = Label(root, fg="#fff", bg="#333", text="Sign in: ", font=("Times", 16))
    signIn.grid(row=1, ipady=2, ipadx=2)

    usernameStringVar = StringVar()
    passwordStringVar = StringVar()
    checkBoxSelect = IntVar()

    signInEntry = Entry(root, font=("Times", 16), textvariable=usernameStringVar)
    passwordEntry = Entry(root, font=("Times", 16), show="*", textvariable=passwordStringVar)

    #  checkes for remembered login info and inserts it
    def remember_insert():
        rememberMe = open(r"rememberMe.txt", "r")
        firstReadLine = rememberMe.readline(1)
        if firstReadLine == "1" and checkBoxSelect.get() == 0:
            rememberMe.readline()
            usernameStringVar = rememberMe.readline()
            passwordStringVar = rememberMe.readline()
            signInEntry.insert(0, usernameStringVar)
            passwordEntry.insert(0, passwordStringVar)
        rememberMe.close()

    #  using threading to continiously check for new rememberMe value
    threading.Thread(None, remember_insert())
    
    #  some more labels and adding stuff to grid
    signInEntry.grid(row=1, column=1)
    passwordLabel = Label(root, fg="#fff", bg="#333", text="Password: ", font=("Times", 16))
    passwordLabel.grid(row=2, column=0, padx=10)
    passwordEntry.grid(row=2, column=1)


    #  if checkBox is checked get_checkbox_val() will write sign in info into rememberMe.txt
    def get_checkbox_val():
        textFile = open(r"rememberMe.txt", "r+")
        firstLine = textFile.readline()

        if checkBoxSelect.get() == 1:
            textFile.seek(0)
            textFile.truncate()
            data = checkBoxSelect.get()
            textFile.seek(0)
            textFile.write(str(data)+ "\r")
            textFile.write(str(usernameStringVar.get())+ "\r")
            textFile.seek(1+len(usernameStringVar.get())+2)
            textFile.write(str(passwordStringVar.get()))
            textFile.close()
            root.destroy()
        else:
            root.destroy()
    checkBox = Checkbutton(root, text="Remember me", bg="#333", fg="#0fff00", variable=checkBoxSelect,
        onvalue=1, offvalue=0)
    checkBox.deselect()
    checkBox.grid(row=3, column=1, sticky=W)
    signInBtn = Button(root, bg="#333", fg="#00ff00", text="Sign in", 
        command=lambda: get_checkbox_val())
    signInBtn.grid(row=3, column=0)
    root.mainloop()
#  end of login tkinter ------------------------------------------------------------------------------------------------

#  loading tkinter
loading = Tk()
loading.title("ArnesAAI")
xCoordinate = loading.winfo_screenwidth()/2 - 180
yCoordinate = loading.winfo_screenheight()/2 - 50
loading.geometry("%dx%d+%d+%d" % (360, 180, xCoordinate, yCoordinate) )
loading.resizable(0, 0)
loading.configure(bg="#333")
Label(loading, fg="#f4f4f4", bg="#333", text="Connecting to ArnesAAI,\
please wait...").place(relx=0.5, rely=0.5, anchor=CENTER)
loading.update()
loading.protocol("WM_DELETE_WINDOW", sys.exit)

#  scraper-------------------------------------------------------------------------------------------------------------

browser = webdriver.Chrome(executable_path=r"chromedriver_8.exe")

browser.get(r"https://idp.aai.arnes.si/simplesaml/module.php/core/loginuserpassorg.php?AuthState=_17002482a9e0221a5509337e838f5379a02475dbb0%3Ahttps%3A%2F%2Fidp.aai.arnes.si%2Fsimplesaml%2Fsaml2%2Fidp%2FSSOService.php%3Fspentityid%3Dhttps%253A%252F%252Faai.arnes.si%252Fsp%252F20140414%26RelayState%3Dcookie%253A1584394960_14fe%26cookieTime%3D1584394960")

#  input username and password
username = browser.find_element_by_id("username")
username.clear()
password = browser.find_element_by_id("user_pass")
password.clear()
password.send_keys(passwordStringVar.get())
username.send_keys(usernameStringVar.get())
try:
    loginBtn = browser.find_element_by_id("wp-submit")
    loginBtn.click()
except:
    pass

elementVisible = False
while not elementVisible:
    try:
        yesContinueBtn = browser.find_element_by_name("yes")
        elementVisible = True
    except:
        continue

if elementVisible:
    yesContinueBtn.click()

elementVisible = False
while not elementVisible:
    try:
        prijavaDropdown = browser.find_element_by_xpath("/html/body/div[1]/div/div[2]/ul[2]/li/a")
        izberiBtn = browser.find_element_by_xpath("/html/body/div[1]/div/div[2]/ul[2]/li/ul/div/form/fieldset/p/span/span[1]/span/span[1]")
        elementVisible = True
    except:
        continue
if elementVisible:
    prijavaDropdown.click()
    izberiBtn.click()
    searchBar = browser.find_element_by_xpath("/html/body/span/span/span[1]/input")
    searchBar.send_keys("Srednja sola tehniskih strok")
    ssts = browser.find_element_by_xpath("/html/body/span/span/span[2]/ul/li")
    ssts.click()
    submit = browser.find_element_by_xpath("//*[@id='right column']/form/fieldset/button")
    submit.click()
elementVisible = False
while not elementVisible:
    try:
        yesContinueBtn = browser.find_element_by_name("yes")
        elementVisible = True
    except:
        continue

yesContinueBtn.click()

elementVisible = False
while not elementVisible:
    try:
        arnesUcilnice = browser.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div/h4/a")
        elementVisible = True
    except:
        continue

windowBefore = browser.window_handles[0]
arnesUcilnice.click()
windowAfter = browser.window_handles[1]
browser.close()
browser.switch_to.window(windowAfter)

elementVisible = False
while not elementVisible:
    try:
        organizacijaDropdown = browser.find_element_by_id("s2id_dropdownlist")
        elementVisible = True
    except:
        continue

organizacijaDropdown.click()
searchBar = browser.find_element_by_xpath("//*[@id='select2-drop']/div/input")
searchBar.send_keys("Srednja sola teh")
ssts = browser.find_element_by_xpath("/html/body/div[4]/ul/li/div")
ssts.click()
submit = browser.find_element_by_xpath("//*[@id='page-top']/header/div/div/div[2]/form/p/input[2]")
submit.click()

elementVisible = False
while not elementVisible:
    try:
        yesContinueBtn = browser.find_element_by_name("yes")
        elementVisible = True
    except:
        continue
    yesContinueBtn.click()

loading.destroy()
loading.mainloop()


#  Main UI --------------------------------------------------------------------------------------------------


main = Tk()
main.title("ArnesAAI")
xCoordinate = main.winfo_screenwidth()/2 - 360
yCoordinate = main.winfo_screenheight()/2 - 250
main.geometry("%dx%d+%d+%d" % (720, 500, xCoordinate, yCoordinate))
main.configure(bg="#e7e7e7")
main.protocol("WM_DELETE_WINDOW", sys.exit)
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



onWidget = ["homeBtn"]
#  had to take the button in as a string, otherwise it is considered unasigned
def on_widget_color(buttonNameAsString):
    for i in buttons:
        setToFFF = eval(buttons[i])
        setToFFF.configure(bg="#fff")

    button = eval(buttonNameAsString)
    btnColor = "#f4f4f4"
    button.configure(bg=btnColor)
    onWidget.clear()
    onWidget.append(buttonNameAsString)
    WidgetObj = Widgets(buttonNameAsString)
    WidgetObj.determain_widget()


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


elementVisible = False
while not elementVisible:
    try:
        usersName = browser.find_element_by_xpath("//*[@id='dropdown-1']/span/span[1]")
        usersNameStr = usersName.text
        elementVisible = True
    except:
        usersNameStr = "Filip Jeretina"
        break
lastCalledWidget = [] 

pointWidth = 0.3528
class Widgets(object):
    def __init__(self, widget):
        self.widget = widget

    def determain_widget(self):
        if len(lastCalledWidget) == 1:
            lastCalledWidget[0].destroy()

        widget = self.widget
        splitPoint = [splitPoint for splitPoint in self.widget if splitPoint.isupper()]
        self.widget = self.widget[:self.widget.index(splitPoint[0])]
        self.widget = ("Widgets.%s_%s(%s)" % (self.widget, "widget", widget))
        eval(self.widget)
        
    def get_event_info(self, eventName, widgetName):
            masterDiv = browser.find_element_by_class_name("eventlist.my-1")
 
            numberOfEvents = len(masterDiv.find_elements_by_xpath("./div"))
            for element in masterDiv.find_elements_by_xpath("./div"):
                if element.get_attribute("data-event-title") == eventName:
                    try:
                        content = element.find_element_by_class_name("description-content.col-xs-11")
                        content = content.text.encode("utf-8")
                        pojdiNaAktivnost = element.find_element_by_class_name("card-link")
                        pojdiNaAktivnost = pojdiNaAktivnost.get_attribute("href")
                        browser.get(pojdiNaAktivnost)
                        contentIsReady = True
                        break

                    except:
                        pojdiNaAktivnost = element.find_element_by_class_name("card-link")
                        pojdiNaAktivnost = pojdiNaAktivnost.get_attribute("href") 
                        browser.get(pojdiNaAktivnost)
                        elementVisible = False
                        while not elementVisible:
                            try:
                                content = browser.find_element_by_class_name("no-overflow")
                                content = content.text.encode("utf-8")
                                contentIsReady = True
                                elementVisible = True
                            except:
                                continue
                        break
            if contentIsReady:
                contentLabel = Label(widgetName,
                                    text=content,
                                    font=("Times", 12),
                                    fg="#fff",
                                    bg="#444",
                                    wraplength=300)
                contentLabel.grid()

            
    def home_widget(self):
        lastCalledWidget.clear()
        
        browser.get("https://ucilnice.arnes.si/my/")
        
        homeWidget = Frame(main, bg="#e7e7e7", width=main.winfo_screenwidth(), height=464)
        homeWidget.place(relx=0, rely=0.072)
        lastCalledWidget.append(homeWidget)
        helloUserLabel = Label(homeWidget,
                            bg="#fff",
                            fg="#333",  
                            text=("Hello, " + usersNameStr + "!"),
                            font=("Times bold", 15))
        helloUserLabel.grid(row=0, column=0, padx=(360-(pointWidth*15*len(usersNameStr))))

        prihajajociDogodkiLabel = Label(homeWidget,
                                        bg="#333",
                                        fg="#f4f4f4",
                                        text="Prihajajoči dogodki",
                                        font=("Times bold", 15 ),
                                        width=20)
        prihajajociDogodkiLabel.grid(column=0, row=1, sticky=W, padx=10)
        
        prihajajociDogodki = browser.find_elements_by_css_selector("div.card-text.content.calendarwrapper a")
        
        allLinkList = []
        
        for element in prihajajociDogodki:
            oneLink = element.get_attribute("href")
            allLinkList.append(oneLink)
            allLinkList.append(element.text)
        
        upcommingEventsLinks = {}

        
        for link in allLinkList:
            if link.find("day&course") != -1:
                upcommingEventsLinks[allLinkList[allLinkList.index(link)+1]] = link
        
        
        
        def make_buttons(link):
            getEventInfo = Widgets(homeWidget)
            Button(homeWidget,
            bg="#444",
            fg="#fff",
            text=link,
            font=("Times", 15),
            border=0,
            command=lambda: [browser.get(upcommingEventsLinks[link]), getEventInfo.get_event_info(link, homeWidget)],
            cursor="hand2",
            width=20, wraplength=200).grid(sticky=W, padx=10)

        for links in upcommingEventsLinks:
            make_buttons(links)

    
    def novo_widget(self):
        lastCalledWidget.clear()
        novoWidget = Frame(main, bg="#e7e7e7", width=main.winfo_screenwidth(), height=464)
        novoWidget.place(relx=0, rely=0.072)
        lastCalledWidget.append(novoWidget)

    def gradivo_widget(self):
        lastCalledWidget.clear()
        gradivoWidget = Frame(main, bg="#e7e7e7", width=main.winfo_screenwidth(), height=464)
        gradivoWidget.place(relx=0, rely=0.072)
        lastCalledWidget.append(gradivoWidget)

    def naloge_widget(self):
        lastCalledWidget.clear()
        nalogeWidget = Frame(main, bg="#e7e7e7", width=main.winfo_screenwidth(), height=464)
        nalogeWidget.place(relx=0, rely=0.072)
        lastCalledWidget.append(nalogeWidget)
        nalogaLabel = Label(nalogeWidget,
                            bg="#e7e7e7",
                            fg="#333",
                            text="Naloga 3",
                            font=("Times", 15))
        nalogaLabel.grid(row=0, column=0, padx=(360-(0.3528*15*8)))
        

    def oddano_widget(self):
        lastCalledWidget.clear()
        oddanoWidget = Frame(main, bg="#e7e7e7", width=main.winfo_screenwidth(), height=464)
        oddanoWidget.place(relx=0, rely=0.072)
        lastCalledWidget.append(oddanoWidget)

main.mainloop()