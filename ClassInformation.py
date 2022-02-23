from tkinter import *
import tkinter.messagebox
from tkinter import ttk
from DataBase import getclassCount
from DataBase import connectDB
from DataBase import closeDB
from DataBase import getTeacherTable
from DataBase import getClassTable
from DataBase import addclass
from DataBase import deleteclass
from DataBase import pd
import datetime

def clear(tree):
    x=tree.get_children()
    for item in x:
        tree.delete(item)
    
def refresh(root1,treeview1):
    clear(treeview1)
    db=connectDB()
    table=getClassTable(db)
    for row in table:
        info = []
        info.append(row[0])
        info.append(row[1])
        info.append(row[2])
        info.append(row[3])
        info.append(row[4])
        treeview1.insert('',END,values=info)

    s="记录总数："+str(getclassCount(db))
    lb1 = Label(root1, text=s) 
    lb1.place(relx=0.3, rely=0.0225, relwidth=0.25, relheight=0.1)
    
    closeDB(db)
    
def newadd(treeview1,s1,s2,s3,s4,s5,root1):
    db=connectDB()
    num=pd(db,s5)
    if(num==0):
        tkinter.messagebox.showinfo(message='添加信息失败！教师号不存在！')
        closeDB(db)
    else:
        try:
            addclass(db,s1,s2,s3,s4,s5)
            tkinter.messagebox.showinfo(message='添加信息成功！')
        except:
            tkinter.messagebox.showinfo(message='添加信息失败！此课程号已存在！')
        closeDB(db)
        refresh(root1,treeview1)
        
    
def newdelete(treeview1,cno,root1):
    if(tkinter.messagebox.askyesno(message='删除信息不可恢复！\n确定是否删除该信息！')):
        db=connectDB()
        pre=getclassCount(db)
        deleteclass(db,cno)
        cur=getclassCount(db)
        closeDB(db)
        if(pre!=cur):
            tkinter.messagebox.showinfo(message='删除信息成功！')
        else:
            tkinter.messagebox.showinfo(message='删除信息失败！此课程号不存在！')
        refresh(root1,treeview1)
    

def add(root,treeview1):
    root1 = Toplevel(root)
    root1.geometry('400x300')
    root1.title('添加信息')
    
    lb1 = Label(root1, text='请输入课程号：')
    lb1.place(relx=0.025, rely=0.1, relwidth=0.3, relheight=0.1)
    inp1 = Entry(root1)
    inp1.place(relx=0.3, rely=0.1, relwidth=0.3, relheight=0.1)
    lb2 = Label(root1, text='请输入课程名：')
    lb2.place(relx=0.025, rely=0.2, relwidth=0.3, relheight=0.1)
    inp2 = Entry(root1)
    inp2.place(relx=0.3, rely=0.2, relwidth=0.3, relheight=0.1)
    lb3 = Label(root1, text='请输入学分：')
    lb3.place(relx=0.025, rely=0.3, relwidth=0.3, relheight=0.1)
    inp3 = Entry(root1)
    inp3.place(relx=0.3, rely=0.3, relwidth=0.1, relheight=0.1)
    lb4 = Label(root1, text='请输入开课系：')
    lb4.place(relx=0.025, rely=0.4, relwidth=0.3, relheight=0.1)
    inp4= Entry(root1)
    inp4.place(relx=0.3, rely=0.4, relwidth=0.4, relheight=0.1)
    lb6 = Label(root1, text='请输入任课教师：')
    lb6.place(relx=0.025, rely=0.5, relwidth=0.3, relheight=0.1)
    inp6 = Entry(root1)
    inp6.place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.1)

    
    btn1 = Button(root1, text='添加信息',command=lambda:newadd(treeview1,inp1.get(),inp2.get(),inp3.get(),inp4.get(),inp6.get(),root))
    btn1.place(relx=0.4,rely=0.85,relwidth=0.2, relheight=0.1)
    
    
    inp1.delete(0, 'end')
    inp2.delete(0, 'end')
    inp3.delete(0, 'end')
    inp4.delete(0, 'end')
    inp6.delete(0, 'end')
    
    
    root1.mainloop()
    sys.exit()
    
def delete(root,treeview1):
    root1 = Toplevel(root)
    root1.geometry('400x250')
    root1.title('删除信息')
    
    lb1 = Label(root1, text='请输入要删除的课程号：')
    lb1.place(relx=0.25, rely=0.1, relwidth=0.4, relheight=0.1)
    inp1 = Entry(root1)
    inp1.place(relx=0.25, rely=0.3, relwidth=0.4, relheight=0.2)
   
    btn1 = Button(root1, text='删除信息',command=lambda:newdelete(treeview1,inp1.get(),root))
    btn1.place(relx=0.3,rely=0.7,relwidth=0.3, relheight=0.2)
    
    
    inp1.delete(0, 'end')
    
    
    root1.mainloop()
    sys.exit()
    
def maintainClassInfomation(root):
    root1 = Toplevel(root)
    root1.geometry('800x600')
    root1.title('课程信息管理')
    
    db=connectDB()
    s="记录总数："+str(getclassCount(db))
    lb1 = Label(root1, text=s) 
    lb1.place(relx=0.3, rely=0.01, relwidth=0.25, relheight=0.2)
    closeDB(db)
    
    columns1 = ("教师号", "教师名","所在系","类别")
    treeview1 = ttk.Treeview(root1, height=100, show="headings", columns=columns1)
    treeview1.column("教师号", width=20, anchor='center') 
    treeview1.column("教师名", width=30, anchor='center') 
    treeview1.column("所在系", width=40, anchor='center')
    treeview1.column("类别", width=30, anchor='center')  
    treeview1.heading("教师号", text="教师号")
    treeview1.heading("教师名", text="教师名")
    treeview1.heading("所在系", text="所在系")
    treeview1.heading("类别", text="类别")
    treeview1.pack(side=LEFT, fill=BOTH)
    treeview1.place(relx=0.45, rely=0.15, relwidth=0.3, relheight=0.7)
    
    columns2 = ("课程号", "课程名","学分","开课系","任课教师")
    treeview2 = ttk.Treeview(root1, height=100, show="headings", columns=columns2)
    treeview2.column("课程号", width=30, anchor='center') 
    treeview2.column("课程名", width=30, anchor='center') 
    treeview2.column("学分", width=30, anchor='center')
    treeview2.column("开课系", width=40, anchor='center')
    treeview2.column("任课教师", width=20, anchor='center')
    treeview2.heading("课程号", text="课程号")
    treeview2.heading("课程名", text="课程名")
    treeview2.heading("学分", text="学分")
    treeview2.heading("开课系", text="开课系")
    treeview2.heading("任课教师", text="任课教师")
    treeview2.pack(side=LEFT, fill=BOTH)
    treeview2.place(relx=0.035, rely=0.15, relwidth=0.4, relheight=0.7)

    
    btn1 = Button(root1, text='新增', command=lambda:add(root1,treeview2))
    btn1.place(relx=0.8,rely=0.3,relwidth=0.15, relheight=0.1)
    btn3 = Button(root1, text='删除', command=lambda:delete(root1,treeview2))
    btn3.place(relx=0.8,rely=0.45,relwidth=0.15, relheight=0.1)
    btn4 = Button(root1, text='关闭', command=root1.destroy)
    btn4.place(relx=0.8,rely=0.6,relwidth=0.15, relheight=0.1)
    
    db=connectDB()
    table1=getTeacherTable(db)
    table2=getClassTable(db)
    for row in table1:
        info = []
        info.append(row[0])
        info.append(row[1])
        info.append(row[2])
        info.append(row[3])
        treeview1.insert('',END,values=info)
        
    for row in table2:
        info = []
        info.append(row[0])
        info.append(row[1])
        info.append(row[2])
        info.append(row[3])
        info.append(row[4])
        treeview2.insert('',END,values=info)
    
    closeDB(db)
    
    root1.mainloop()
    sys.exit()
    