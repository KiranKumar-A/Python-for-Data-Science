"""
Front-End of TDS Database Application

"""

############ Library Import #############
from tkinter import *
from tkinter import ttk
import pandas as pd
from tkinter.messagebox import showinfo
import os
#os.chdir(R'C:\Users\1011597\Desktop\Rakesh Acharya\Data Analysis\SQL\Build a Desktop Database Application - PostgreSQL')
cwd = os.getcwd()
sys.getrecursionlimit()

############ Import Backend.py #############
import Backend

############ FUNCTION ##############

#Function used to clear data from the textboxs and dropdowns
def clear_data():
    var0.set("")
    var11.set("")
    e1.delete(0,END)
    e2.delete(0,END)
    e3.delete(0,END)
    var1.set("")
    var2.set("")
    e4.delete(0,END)
    e5.delete(0,END)
    e6.delete(0,END)
    e7.delete(0,END)
    e8.delete(0,END)
    e9.delete(0,END)

#Function used get data from the textboxs and dropdowns
def getdata():
    if len(var0.get()) == 0:
        dd0=None
    else:
        dd0=var0.get()
    
    if len(var11.get()) == 0:
        dd11=None
    else:
        dd11=var11.get()
    
    if len(TDS_text.get()) == 0:
        text1=None
    else:
        text1=TDS_text.get()
    
    if len(start_text.get()) == 0:
        text2=None
    else:
        text2=start_text.get()
    
    if len(end_text.get()) == 0:
        text3=None
    else:
        text3=end_text.get()
    
    if len(var1.get()) == 0:
        dd1=None
    else:
        dd1=var1.get()
    
    if len(var2.get()) == 0:
        dd2=None
    else:
        dd2=var2.get()
    
    if len(nonexp_text.get()) == 0:
        text4=None
    else:
        text4=nonexp_text.get()
    
    if len(Onexp_text.get()) == 0:
        text5=None
    else:
        text5=Onexp_text.get()
    
    if len(Offexp_text.get()) == 0:
        text6=None
    else:
        text6=Offexp_text.get()
    
    if len(Offper_text.get()) == 0:
        text7=None
    else:
        text7=Offper_text.get()
    
    if len(TarOffper_text.get()) == 0:
        text8=None
    else:
        text8=TarOffper_text.get()
    
    if len(remarks_text.get()) == 0:
        text9=None
    else:
        text9=remarks_text.get()
    
    return (dd0, dd11, text1, text2, text3, dd1, dd2, text4, text5, text6, text7, text8, text9)

#Function used to show the pop-up msgs
def popupmsg(title, msg):
    popup = Tk()
    popup.wm_title(title)
    label = Label(popup, text=msg)
    label.pack()
    popup.mainloop()

def usermsg(msg,fontground):
    
    l100['text'] = msg
    l100['fg'] = fontground


#Function to view all the data in the database
def view_command():
    try:
        list1.delete(*list1.get_children())
    except:
        pass

    myList = Backend.view()
    for row in range(len(myList)):
        list1.insert("" , "end", values=(myList[row][3],myList[row][4],myList[row][5],myList[row][6],myList[row][7],myList[row][8],myList[row][9],myList[row][10],myList[row][11],myList[row][12],myList[row][13]))
    
    usermsg("","Green")
    
#Function to filter-out the data in the database
def search_command():
    try:
        list1.delete(*list1.get_children())
    except:
        pass
    
    dd0, dd11, text1, text2, text3, dd1, dd2, text4, text5, text6, text7, text8, text9 = getdata()
    tdsno=""
    myList = Backend.search(var0.get(), TDS_text.get(), var11.get(), tdsno, text2, text3, dd1, dd2,text4, text5, text6, text7, text8, text9)
    
    for row in range(len(myList)):
        list1.insert("" , "end", values=(myList[row][3],myList[row][4],myList[row][5],myList[row][6],myList[row][7],myList[row][8],myList[row][9],myList[row][10],myList[row][11],myList[row][12],myList[row][13]))
        
    usermsg("","Green")
    
#Function to add data in to the database and the previous issue data will be move to bakeup datatable
def add_command():
    try:
        list1.delete(*list1.get_children())
    except:
        pass
    Backend.connect1()
    Backend.connect2()
    
    dd0, dd11, text1, text2, text3, dd1, dd2, text4, text5, text6, text7, text8, text9 = getdata()
    
    if dd0!="" or dd11!="" or text1!="":
        tdsno = dd0+"_"+text1+"_"+dd11
    
    myList = Backend.backup1("%"+dd0+"_"+text1+"%")

    err = Backend.insert(var0.get(), TDS_text.get(), var11.get(), tdsno, text2, text3, dd1, dd2,text4, text5, text6, text7, text8, text9)
    
    if err=="22007" or err=="22P02" or err=="23502":
        usermsg("Error Possibilities:\n 1. All entries are mandatory \n 2. Data format error","Red")
        #popupmsg("ERROR", "Error Possibilities:\n 1. All entries are mandatory \n 2. Data format error")
    elif err=="22008":
        usermsg("Date format entered seems to be incorrect","Red")
        #popupmsg("ERROR", "Date format entered seems to be incorrect")
    elif err=="23505":
        usermsg("There is already data with the given TDS No.\n TDS No. should be unique.","Red")
        #popupmsg("ERROR", "There is already data with the given TDS No.\n TDS No. should be unique.")
    else:
        usermsg("Data successfully added to the database","Green")
        for row in range(len(myList)):
            Backend.backup2(myList[row][0],myList[row][1],myList[row][2],myList[row][3],myList[row][4],myList[row][5],myList[row][6],myList[row][7],myList[row][8],myList[row][9],myList[row][10],myList[row][11],myList[row][12],myList[row][13])
            Backend.backup3(myList[row][3])
        
        list1.insert("" , "end", values= (tdsno, start_text.get(), end_text.get(), var1.get(), var2.get(),nonexp_text.get(), Onexp_text.get(), Offexp_text.get(), Offper_text.get(), TarOffper_text.get(), remarks_text.get()))
        clear_data()

#Function to delete data from the database
def delete_command():
   
    dd0, dd11, text1, text2, text3, dd1, dd2, text4, text5, text6, text7, text8, text9 = getdata()
    
    if dd0!="" or dd11=="" or text1=="":
        tdsno = dd0+"_"+text1+"_"+dd11

    Backend.delete(tdsno)
    view_command()
    usermsg("Data successfully deleted from the database","Green")

#Function to update data in the database
def update_command():
    
    dd0, dd11, text1, text2, text3, dd1, dd2, text4, text5, text6, text7, text8, text9 = getdata()
    
    if dd0!="" or dd11=="" or text1=="":
        tdsno = dd0+"_"+text1+"_"+dd11
    
    Backend.update(tdsno,text2, text3, dd1, dd2, text4, text5, text6, text7, text8, text9)
    view_command()
    usermsg("Data successfully updated in the database","Green")

#Function to export data to excel from the database
def export_data():
    
    myList = Backend.exportdata("Current Data")
    df = pd.DataFrame(myList, columns=['Statement of Requirement (SoR)', 'Task Definition Sheet (TDS)', 'Issue', 'Task Definition Sheet (TDS) no.', 'StartDate', 'EndDate', 'Geography', 'Status', 'NonExpHrs', 'OnExpHrs', 'OffExpHrs', 'OffPerHrs', 'TarPerHrs', 'Remarks'])
    writer = pd.ExcelWriter('TDS_Data.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Data')
    writer.save()
    usermsg("The exported file is save in: " + cwd + "\TDS_Data.xlsx","Green")
    #popupmsg("INFO", "The exported file is save in: " + cwd + "\TDS_Data.xlsx")

#Function to export backup data to excel from the database
def export_backupdata():
    
    myList = Backend.exportdata("Backup Data")
    df = pd.DataFrame(myList, columns=['Statement of Requirement (SoR)', 'Task Definition Sheet (TDS)', 'Issue', 'Task Definition Sheet (TDS) no.', 'StartDate', 'EndDate', 'Geography', 'Status', 'NonExpHrs', 'OnExpHrs', 'OffExpHrs', 'OffPerHrs', 'TarPerHrs', 'Remarks'])
    writer = pd.ExcelWriter('TDS_Backup_Data.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='BackupData')
    writer.save()
    usermsg("The exported file is save in: " + cwd + "\TDS_Backup_Data.xlsx","Green")
    #popupmsg("INFO", "The exported file is save in: " + cwd + "\TDS_Backup_Data.xlsx")
    
#Function to fill the textboxs and dropdowns with the data selected from the database
def get_selected_row(event):
    global selected_tuple
    try:
        for item in list1.selection():
            selected_tuple = list1.item(item,"values")
            
            tdsdata=selected_tuple[0].split("_")
            
            var0.set(tdsdata[0])
            var11.set(tdsdata[2])
            e1.delete(0,END)
            e1.insert(END,tdsdata[1])
            e2.delete(0,END)
            e2.insert(END,selected_tuple[1])
            e3.delete(0,END)
            e3.insert(END,selected_tuple[2])
            var1.set(selected_tuple[3])
            var2.set(selected_tuple[4])
            e4.delete(0,END)
            e4.insert(END,selected_tuple[5])
            e5.delete(0,END)
            e5.insert(END,selected_tuple[6])
            e6.delete(0,END)
            e6.insert(END,selected_tuple[7])
            e7.delete(0,END)
            e7.insert(END,selected_tuple[8])
            e8.delete(0,END)
            e8.insert(END,selected_tuple[9])
            e9.delete(0,END)
            e9.insert(END,selected_tuple[10])
    except IndexError:
        pass

#Function to fill 'TarOffper_text' textbox based on 'SOR' dropdown
def fill_TPOHrs(self):
    
    if var0.get()=="Compressors":
        TarOffper_text.set(80)
    elif var0.get()=="EFS - Cost & Sampling":
        TarOffper_text.set(94)
    elif var0.get()=="EFS - FAIR & CM":
        TarOffper_text.set(88)
    elif var0.get()=="EFS - LCE":
        TarOffper_text.set(93)
    elif var0.get()=="EFS - Repair":
        TarOffper_text.set(95)
    elif var0.get()=="EFS - TV":
        TarOffper_text.set(91)
    elif var0.get()=="Externals":
        TarOffper_text.set(84)
    elif var0.get()=="Materials":
        TarOffper_text.set(89)
    elif var0.get()=="ME - A & T":
        TarOffper_text.set(66)
    elif var0.get()=="ME - Central":
        TarOffper_text.set(72)
    elif var0.get()=="ME - Compressors":
        TarOffper_text.set(79)
    elif var0.get()=="ME - Defence":
        TarOffper_text.set(75)
    elif var0.get()=="ME - Installations":
        TarOffper_text.set(81)
    elif var0.get()=="ME - Rotatives":
        TarOffper_text.set(83)
    elif var0.get()=="ME - S & T":
        TarOffper_text.set(80)
    elif var0.get()=="ME- Turbines":
        TarOffper_text.set(79)
    elif var0.get()=="Rotatives":
        TarOffper_text.set(80)
    elif var0.get()=="S & T":
        TarOffper_text.set(87)
    elif var0.get()=="S E & D":
        TarOffper_text.set(86)
    elif var0.get()=="System Design - Config":
        TarOffper_text.set(83)
    elif var0.get()=="System Design - Performance":
        TarOffper_text.set(83)
    elif var0.get()=="T & M":
        TarOffper_text.set(88)
    elif var0.get()=="Turbines":
        TarOffper_text.set(70)
    elif var0.get()=="RRC - Design Services":
        TarOffper_text.set(52)
    elif var0.get()=="RRC - EFS":
        TarOffper_text.set(83)

#Function to fill 'Offper_text' textbox based on 'Offexp_text' and 'Offexp_text' textbox
def fill_POHrs(self):
    if Offexp_text.get() != 0 or Offexp_text.get() != "":
        Offper_text.set(float(Offexp_text.get())/(float(Onexp_text.get())+float(Offexp_text.get()))*100)


############ DESIGN ##############

############ WINDOW ##############
window = Tk()
window.geometry("1900x730")
window.title("TDS Database (RR Account)")

############ LABEL ##############
l00 = Label(window, text = "TDS Database",bd=10, font='Aerial 20 bold')
l00.grid(row=0, column=0, columnspan=4)

l10 = Label(window, text = "SOR",bd=5)
l10.grid(row=1, column=0)

l20 = Label(window, text = "TDS No.",bd=5)
l20.grid(row=2, column=0)

l22 = Label(window, text = "Issue",bd=5)
l22.grid(row=2, column=2)

l30 = Label(window, text = "Start Date (yyyy-mm-dd)",bd=5)
l30.grid(row=3, column=0)

l32 = Label(window, text = "End Date (yyyy-mm-dd)",bd=5)
l32.grid(row=3, column=2)

l40 = Label(window, text = "Geography",bd=5)
l40.grid(row=4, column=0)

l42 = Label(window, text = "Status",bd=5)
l42.grid(row=4, column=2)

l50 = Label(window, text = "Non-Exportable Hrs.",bd=5)
l50.grid(row=5, column=0)

l60 = Label(window, text = "Exportable Hrs. (Onsite)",bd=5)
l60.grid(row=6, column=0)

l70 = Label(window, text = "Exportable Hrs. (Offshore)",bd=5)
l70.grid(row=7, column=0)

l80 = Label(window, text = "Percentage Offshoring Hrs (%)",bd=5)
l80.grid(row=8, column=0)

l82 = Label(window, text = "Target Percentage Offshoring Hrs (%)",bd=5)
l82.grid(row=8, column=2)

l90 = Label(window, text = "Remarks/Comments:",bd=5)
l90.grid(row=9, column=0)

l100 = Label(window, text = "", bd=5, font='Aerial 14 bold')
l100.grid(row=32, column=0, columnspan=4)


############ TEXTBOX ##############
TDS_text = StringVar()
e1 = Entry(window, textvariable=TDS_text, width=40)
e1.grid(row=2, column=1)

start_text = StringVar()
e2 = Entry(window, textvariable=start_text, width=40)
e2.grid(row=3, column=1)

end_text = StringVar()
e3 = Entry(window, textvariable=end_text, width=40)
e3.grid(row=3, column=3)

nonexp_text = StringVar()
e4 = Entry(window, textvariable=nonexp_text, width=40)
e4.grid(row=5, column=1)

Onexp_text = StringVar()
e5 = Entry(window, textvariable=Onexp_text, width=40)
e5.bind("<Key>", fill_POHrs)
e5.grid(row=6, column=1)

Offexp_text = StringVar()
e6 = Entry(window, textvariable=Offexp_text, width=40)
e6.bind("<Key>", fill_POHrs)
e6.grid(row=7, column=1)

Offper_text = StringVar()
e7 = Entry(window, textvariable=Offper_text, width=40)
e7.bind("<Key>", fill_POHrs)
e7.grid(row=8, column=1)

TarOffper_text = StringVar()
e8 = Entry(window, textvariable=TarOffper_text, width=40)
e8.grid(row=8, column=3)

remarks_text = StringVar()
e9 = Entry(window, textvariable=remarks_text, width=40)
e9.grid(row=9, column = 1, columnspan=3, sticky=W+E)

############ DROPDOWN / OPTION MENU ##############

var0 = StringVar(window)
var0.set("") # initial value
option0 = OptionMenu(window, var0, "", "Compressors", "EFS - Cost & Sampling", "EFS - FAIR & CM", "EFS - LCE",
                     "EFS - Repair", "EFS - TV", "Externals", "Materials", "ME - A & T", "ME - Central",
                     "ME - Compressors", "ME - Defence", "ME - Installations", "ME - Rotatives",
                     "ME - S & T", "ME- Turbines", "Rotatives", "S & T", "S E & D", "System Design - Config",
                     "System Design - Performance", "T & M", "Turbines", "RRC - Design Services",
                     "RRC - EFS", "RRC - ME", "RRC - Producibility", command=fill_TPOHrs)
option0.grid(row=1, column=1)

var11 = StringVar(window)
var11.set("") # initial value
option11 = OptionMenu(window, var11, "", "Iss1", "Iss2", "Iss3", "Iss4", "Iss5", "Iss6", "Iss7",
                      "Iss8", "Iss9", "Iss10", "Iss11", "Iss12", "Iss13", "Iss14", "Iss15")
option11.grid(row=2, column=3)

var1 = StringVar(window)
var1.set("") # initial value
option1 = OptionMenu(window, var1, "", "UK", "Germany", "USA")
option1.grid(row=4, column=1)

var2 = StringVar(window)
var2.set("")    # initial value
option2 = OptionMenu(window, var2, "", "Submitted", "Active", "Hold")
option2.grid(row=4, column=3)


############ BUTTONS ##############
b1=Button(window, text="Add Entry", width=40,command = add_command,bd=5)
b1.grid(row=10, column=1)

b2=Button(window, text="Update Entry", width=40,command = update_command,bd=5)
b2.grid(row=10, column=2)

b3=Button(window, text="Get Data", width=40,command = view_command,bd=5)
b3.grid(row=10, column=3)

b4=Button(window, text="Search Entry", width=40,command = search_command,bd=5)
b4.grid(row=11, column=1)

b5=Button(window, text="Delete Entry", width=40,command = delete_command,bd=5)
b5.grid(row=11, column=2)

b6=Button(window, text="Clear Entry", width=40,command = clear_data,bd=5)
b6.grid(row=11, column=3)

b7=Button(window, text="Export Data", width=40,command = export_data,bd=5)
b7.grid(row=30, column=1)

b8=Button(window, text="Export Backup Data", width=40,command = export_backupdata,bd=5)
b8.grid(row=30, column=2)

b9=Button(window, text="Quit", width=40,command = window.destroy,bd=5)
b9.grid(row=30, column=3)

############# Treeview ##############
cols = ('TDS no.', 'Start Date', 'End Date', 'Geography', 'Status', 'Non-Exportable Hrs.','Exportable Hrs. (Onsite)', 'Exportable Hrs. (Offshore)', 'Percentage Offshoring Hrs.','Target Percentage Offshoring Hrs.', 'Remarks/Comments')
list1 = ttk.Treeview(window, columns=cols, show='headings')

for col in cols:
    list1.heading(col, text=col)
    list1.column(col, width=150)


list1.grid(row=12, column=0, rowspan=15, columnspan=4)
#
############# SCROLLBAR ##############
sb1 = Scrollbar(window)
sb1.grid(row=12,column=4, rowspan=15)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.bind('<<TreeviewSelect>>',get_selected_row)


window.mainloop()