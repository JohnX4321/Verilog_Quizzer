# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# -*- coding: utf-8 -*-

import datetime, os
import logging
from tkinter.filedialog import *
from tkinter.messagebox import *
import configparser, base64
from ttkbootstrap import *

currQues = ""
currFile = None
orFileContents = None

questions = ["Design a Verilog code to simulate Full Adder Circuit"]
currIndex = 0
workDir = os.getcwd() + "\\data\\"
configKey = str(base64.b64encode("CurrentQuestionIndex".encode('utf-8')).decode('utf-8')).lower()

saved=False;
def createConfig():
    global configKey, currIndex
    config = configparser.ConfigParser()
    # config['SETTINGS'] = {configKey: str(base64.b64encode(str(currIndex).encode("ascii")))}
    config['SETTINGS'] = {
        "cqi": str(base64.b64encode(str(currIndex).encode('utf-8')).decode('utf-8'))}  # ,"First": "true","USN": "NA"}
    config['ABOUT'] = {"version": "1.0", "channel": "public", "requires": "python3,icarus-verilog", "os":"windows","for": "ece-dsce",
                       "published": "2021", "loglevel": "release","license": "apache-license-2.0","uwp": "no","cred": "b5a8doe0"}
    config['WARNING'] = {
        "value": "DO NOT MODIFY THIS FILE. DOING SO MAY BREAK THE SOFTWARE."}
    with open('config.tsif', 'w') as cf:
        config.write(cf)


def readConfig():
    global currIndex, configKey
    if not os.path.isfile('config.tsif'):
        createConfig()
    else:
        config = configparser.ConfigParser()
        config.read('config.tsif')
        # for key in config['SETTINGS']:
        #    print(bytes(key))
        # print(config['SETTINGS'][configKey])
        # currIndex = int(base64.b64decode(str(config['SETTINGS'][configKey])))
        currIndex = int(base64.b64decode(config['SETTINGS']['cqi']).decode('utf-8'))


def compileIVerilog():
    global saved
    if not saved:
        showwarning("Save","Please Save the file from File->Save and then press submit")
        return
    os.chdir(workDir)
    cmd = os.system(str('cmd.exe /c iverilog -o adder soln.v tb_adder.v\n'))
    cmd = os.system('cmd.exe /c vvp adder\n')
    if cmd != 0:
        print("Error")
        showerror("Error", "Iverilog not installed\n or Error In Code")
        return
    print("done")
    f = open('output.txt', 'r')
    c = ""
    for x in f:
        c += x
    showinfo("Output", c)


def editorPage():
    style=Style(theme='cyborg')
    root = style.master
    title = StringVar()
    title.set("FPGA Quiz")
    root.title(title.get())
    icon = PhotoImage(file="icon.png")
    root.iconphoto(False,icon)
    # root.attributes('-fullscreen',True)

    root.geometry("600x600")
    # sb = StringVar()
    # sb.set("Ln")
    # statusbar = Label(root, textvariable=sb, relief=SUNKEN, bd=1, anchor="w")
    textArea = Text(root, undo=True, wrap=None, height=root.winfo_height(), width=root.winfo_width())
    textArea.grid(row=0, sticky=N + E + S + W)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    scrollbarV = Scrollbar(textArea, command=textArea.yview)
    textArea.config(yscrollcommand=scrollbarV.set)
    scrollbarV.pack(side=RIGHT, fill=Y)
    currQues = questions[currIndex]
    cQ = StringVar()
    cQ.set(currQues)
    fr_buttons = Frame(root)
    btn_Submit = Button(fr_buttons, text='Submit', command=compileIVerilog)
    btn_Submit.place(x=10, y=5, width=80, height=25)
    quesLabel = Label(fr_buttons, textvariable=cQ, wraplength=80, font=(30))
    quesLabel.place(x=0, y=40, width=100)
    # fr_buttons.grid(row=0, column=0, sticky="ns")
    fr_buttons.place(x=0, y=0, width=150, height=root.winfo_screenheight())
    # textArea.grid(row=0, column=1, sticky="nsew")
    textArea.place(x=152, y=0, width=root.winfo_screenwidth() - 160, height=root.winfo_screenheight())

    # showinfo("Today's Question",cQ.get())

    def createFile():
        global currFile,saved
        saved=False
        currFile = None
        title.set("New File")
        textArea.delete(1.0, END)

    def helpMenu():
        showinfo("Help", "Enter the code or open file.\n Save the file.\n Press the submit button and wait. \n  "
                         "Results will be displayed.")

    def openFile():
        global currFile, orFileContents

        currFile = askopenfilename(defaultextension=".v",
                                   filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"),
                                              ("Verilog files", "*.v")])
        if currFile == "":
            currFile = None
            orFileContents = None
        else:
            try:
                title.set(os.path.basename(currFile))
                textArea.delete(1.0, END)
                file = open(currFile, "r")
                textArea.insert(1.0, file.read())
                orFileContents = file.read()
                file.close()
            except:
                title.set("NewText")
                showerror("Error", str("Unable to open " + currFile + "\n Not a readable file"))

    def saveFile(*args):
        global currFile, orFileContents,saved
        saved=True
        if currFile is None:
            saveAsFile()
        else:
            file = open(str(currFile), "w")
            orFileContents = textArea.get(1.0, END)
            file.write(textArea.get(1.0, END))
            file.close()
            showinfo("Save Success", "All changes Saved")

    def saveAsFile(*args):
        global currFile, workDir,saved
        if not saved:
            saved=True
        workDir = os.getcwd()
        currFile = workDir + "soln.v"  # asksaveasfilename(defaultextension=".v",
        # filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt"),
        #          ("Verilog Files", "*.v")])
        if currFile == "":
            currFile = None
        else:
            file = open(currFile, "w")
            file.write(textArea.get(1.0, END))
            file.close()
            showinfo("Save Success", str("File " + currFile + " saved"))

    def datetimefunc():
        textArea.insert(END, str(datetime.datetime.now()))

    def cutText():
        textArea.event_generate("<<Cut>>")

    def copyText():
        textArea.event_generate("<<Copy>>")

    def pasteText():
        textArea.event_generate("<<Paste>>")

    def deleteText():
        r = textArea.tag_ranges(SEL)
        textArea.delete(*r)

    def about():
        showinfo("About FPGA Quiz",
                 "A text editor/application \n to submit code for given question and score the same.\n » Developed "
                 "for ECE Dept, DSCE -- 2021. \n » Contact Teacher for any issues")

    def exitApp():
        root.quit()

    def selectAll():
        textArea.event_generate("<<SelectAll>>")

    def undo():
        try:
            textArea.edit_undo()
        except:
            pass

    def redo():
        try:
            textArea.edit_redo()
        except:
            pass

    def lineCount():
        if textArea.compare("end-ic", "!=", "1.0"):
            s3 = str(str(int(textArea.index("end").split('.')[0]) - 1)) + " Ln"

    def wordCount():
        if textArea.compare("end-1c", "!=", "1.0"):
            s5 = str(str(len(textArea.get(0.0, END).replace("\n", " ").split(" ")) - 1) + " Words")

    def noSaveExit():
        global currFile
        if currFile is not None:
            if orFileContents == textArea.get(1.0, END):
                pass
            else:
                exitApp()
        res = askquestion(title="Exit", message=str("Do you want to save changes?"), icon="warning")
        if res == "yes":
            saveFile()
        else:
            exitApp()

    textArea.bind("<F5>", datetimefunc)
    textArea.bind("<Control-n>", createFile)
    textArea.bind("<Control-s>", saveFile)
    #textArea.bind("<Control-o>", openFile)
    menu = Menu(root)
    root.config(menu=menu)
    s1 = Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=s1)
    s1.add_command(label="New (Ctrl+N)", command=createFile)
    #s1.add_command(label="Open (Ctrl+O)", command=openFile)
    s1.add_command(label="Save (Ctrl+S)", command=saveFile)
    s1.add_command(label="Save As", command=saveAsFile)
    s1.add_separator()
    s1.add_command(label="Exit", command=noSaveExit)
    s2 = Menu(menu, tearoff=0)
    menu.add_cascade(label="Edit", menu=s2)
    s2.add_command(label="Undo (Ctrl+Z)", command=undo)
    s2.add_command(label="Redo (Ctrl+Y)", command=redo)
    s2.add_command(label="Cut (Ctrl+X)", command=cutText)
    s2.add_command(label="Copy (Ctrl+Y)", command=copyText)
    s2.add_command(label="Paste (Ctrl+V)", command=pasteText)
    s2.add_separator()
    s2.add_command(label="Select All (Ctrl+A)", command=selectAll)
    s2.add_command(label="Add timeStamp (F5)", command=datetimefunc)
    menu.add_command(label="About", command=about)
    menu.add_command(label="Help", command=helpMenu)


splash_root = Tk()
splash_root.title("FPGA Quiz Application")
# Adjust size
splash_root.geometry("400x200")
splashText = StringVar()
splashText.set("Loading...\n\n Please install Icarus verilog before \n submission and add to system path.\n Executable is provided with this app")
readConfig()
# Set Label
splash_label = Label(splash_root, textvariable=splashText, font=18)
splash_label.pack()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    def switch():
        # or question greater than 15
        if currIndex is not None:
            splash_root.destroy()
            editorPage()
        else:
            splashText.set("Unable to read settings file. Exiting..")
            splash_root.after(2500, lambda: quit())


    splash_root.after(5000, lambda: switch())
    try:
        mainloop()
    except Exception as e:
        logging.exception("App Crashed. Error: %s", e)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
