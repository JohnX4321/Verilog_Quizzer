
# -*- coding: utf-8 -*-

import datetime,os
import logging
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import *

from ttkbootstrap import *

currQues = ""
currFile = None
orFileContents = None
#names=["Select Question","tb1.v","tb2.v","tb3.v","tb4.v","tb5.v","tb6.v","tb7.v","tb8.v","tb9.v","tb10.v","tb11.v","tb12.v",
#       "tb13.v","tb14.v","tb15.v","tb16.v","tb17.v","tb18.v","tb19.v","tb20.v","tb21.v","tb22.v","tb23.v","tb24.v",
#       "tb25.v"]

currIndex = 0
workDir = os.getcwd() + "\\data\\"


saved=False

def showTB(fn):
    master=Tk()
    f=open(workDir+fn)
    msg = Message(master, text=str(f.read()))
    msg.config(bg='lightgreen', font=('times', 24, 'italic'))
    msg.pack()


def compileIVerilog(ques):
    global saved
    if not saved:
        showwarning("Save","Please Save the file from File->Save and then press submit")
        return
    if ques==str("Select"):
        showwarning("Question","Choose question from the dropdown")
        return
    qname=str("tb"+ques+".v")
    os.chdir(workDir)
    cmd = os.system(str('cmd.exe /c iverilog -o comres soln.v '+qname+'\n'))
    cmd = os.system('cmd.exe /c vvp comres\n')
    if cmd != 0:
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
    title.set("Verilog Evaluator")
    root.title(title.get())
    icon = PhotoImage(file="icon.png")
    root.iconphoto(False,icon)
    # root.attributes('-fullscreen',True)

    root.geometry("600x600")
    # sb = StringVar()
    # sb.set("Ln")
    # statusbar = Label(root, textvariable=sb, relief=SUNKEN, bd=1, anchor="w")
    textArea = Text(root, undo=True, wrap=None, height=root.winfo_height(), width=root.winfo_width(),font=("Times New Roman",15))
    textArea.grid(row=0, sticky=N + E + S + W)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    scrollbarV = Scrollbar(textArea, command=textArea.yview)
    textArea.config(yscrollcommand=scrollbarV.set)
    scrollbarV.pack(side=RIGHT, fill=Y)



    fr_buttons = Frame(root)
    btn_Submit = Button(fr_buttons, text='Submit', command=lambda: compileIVerilog(cbt.get()),font=("Times New Roman",15))
    btn_Submit.place(x=10, y=5, width=80, height=30)

    def showTB2():
        f=open(workDir+'tb1.v')
        showinfo("TestBench",str(f.read()))

    cbt=StringVar()
    Label(fr_buttons, text="Select Question",
               foreground="yellow",
              font=("Times New Roman", 15)).place(x=5,y=60,width=140,height=20)
    questionBox=ttk.Combobox(fr_buttons,width=20,textvariable=cbt,background="white")
    questionBox['values']=('Select','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25')
    questionBox.place(x=10,y=95,width=100,height=30)
    questionBox.set("Select")
    showtb=Button(fr_buttons,text="Show Testbench",command=lambda: showTB)
    showtb.place(x=19,y=150,width=40,height=20)
    #root.bind('<<ComboboxSelected>>',combochange)
    cq = StringVar()
    cq.set("Select")
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
        showinfo("Help", "Enter the code or open file.\nSave the file.\nPress the submit button and wait. \n Results will be displayed.")

    def openFile():
        global currFile, orFileContents

        currFile=workDir+"soln.v"
        try:
            textArea.delete(1.0, END)
            file = open(currFile, "r")
            textArea.insert(1.0, file.read())
            orFileContents = file.read()
            file.close()
        except IOError:
            showerror("Error", "No file found to be restored. You may not have saved the file")

    def saveFile(*args):
        global currFile, orFileContents,saved
        saved=True
        if currFile is None:
            saveAsFile()
        else:
            file = open(str(currFile), "w")
            orFileContents = textArea.get(1.0, END)
            file.write(orFileContents)
            file.close()
            showinfo("Save Success", "All changes Saved")

    def saveAsFile(*args):
        global currFile, workDir,saved
        if not saved:
            saved=True
        #workDir = os.getcwd()
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
        showinfo("About Verilog Evaluator",
                 "A text editor/application \n to submit code for given question and score the same.\n » "
                 "ECE Dept, DSCE -- 2021. \n » Icon by Darius Dan (flaticon.com) \n» Contact Teacher for any issues")

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
    s1.add_command(label="Restore (Ctrl+O)", command=openFile)
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
splash_root.title("Verilog Evaluator Application")
# Adjust size
splash_root.geometry("400x200")
splashText = StringVar()
splashText.set("Loading...\n\n This software uses Icarus \n Verilog for its execution.\n If you saved the file and closed application you \n can get back the text by File->Restore")
icon = PhotoImage(file="icon.png")
splash_root.iconphoto(False,icon)
#readConfig()
# Set Label
splash_label = Label(splash_root, textvariable=splashText, font=18)
splash_label.pack()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    def switch():
        splash_root.destroy()
        editorPage()


    splash_root.after(4000, lambda: switch())
    try:
        mainloop()
    except Exception as e:
        logging.exception("App Crashed. Error: %s", e)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
