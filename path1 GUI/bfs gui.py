from ast import Str
from cProfile import label
from cgitb import text
from logging import root
from random import choices
from secrets import choice
from select import select
from tkinter import *
from tkinter import ttk 
from tkinter import filedialog
from tkinter import font
from tkinter.font import BOLD
from unittest.util import _MAX_LENGTH
from pytube import YouTube 
import sys


import curses
from curses import wrapper
from queue import LifoQueue
import time


maze = [
    ["#","#","#","#","#","#","#","#"],
    ["#","A",".",".","#",".",".","#"],
    ["#",".","#",".","#",".","#","#"],
    ["#",".",".",".",".",".",".","#"],
    ["#","#","#",".","#","#",".","#"],
    ["#",".",".",".",".",".","B","#"],
    ["#","#","#","#","#","#","#","#"],
]

def find_start(maze , start):
    for i , row in enumerate(maze):
        for j , value in enumerate(row):
         if value == start:
          return i , j
    return None     

def find_path(maze , stdscr):
    start = "A"
    end = "B"
    start_pos = find_start(maze , start)
    
    q= LifoQueue()
    q.put((start_pos , [start_pos]))

    visited = set()

    while not q.empty():
        current_pos , path = q.get()
        row , col = current_pos
        
        stdscr.clear()
        print_maze(maze ,stdscr , path)
        time.sleep(0.0)
        stdscr.refresh()
         
        if maze[row][col]== end:
         return path

        nighbors = find_nighbors(maze , row , col)
        for nighbor in nighbors:
            if nighbor in visited:
             continue

            r , c = nighbor
            if maze[r][c]=="#":
                continue

            new_path = path+[nighbor]
            q.put((nighbor , new_path))
            visited.add(nighbor)

def find_nighbors(maze , row , col):
    nighbors = []
    if row >0: #up
        nighbors.append((row-1 , col))
    if row+1 < len(maze): #down
        nighbors.append((row+1 , col))
    if col >0: #left
        nighbors.append((row , col-1))
    if col+1 < len(maze[0]): #right
        nighbors.append((row , col+1)) 
    return nighbors    

def print_maze(maze,stdscr ,path=[]):
    BLUE =curses.color_pair(1)
    RED =curses.color_pair(2)
   
    for i , row in enumerate(maze):
        for j , value in enumerate(row):
            if (i , j) in path:
             stdscr.addstr(i,j*2,"♥" , RED)    
            else:    
             stdscr.addstr(i,j*2,value , BLUE) 

def main(stdscr):
    curses.init_pair(1 , curses.COLOR_BLUE ,curses.COLOR_BLACK)
    curses.init_pair(2 , curses.COLOR_RED ,curses.COLOR_BLACK)
    color1 =curses.color_pair(1)
    color1 =curses.color_pair(2)
    find_path(maze , stdscr)
    stdscr.getch()


#root = the view = المحيط اللى فيه الكلام 
root = Tk()
root.title("برنامج لتنزيل الفيديوهات والاغانى ")
root.geometry('700x450+320+20') #set window
root.resizable(False,False)
root.columnconfigure(0,weight=1) #set all content in center.
# f1=Frame(root,width=600,height=90,bg='red',bd=3,relief=GROOVE)
# f1.place(x=30,y=130)
f2=Frame(root,width=600,height=301,bg='brown',bd=3,relief=GROOVE)
f2.place(x=30,y=300)

#ytd link Lable 
t = Label ( root, text=' program for download video and audio', bg='green' ,fg='yellow',font=("Tajawal" , 17, BOLD))
t.pack(fill=X)
ytdLable = Label ( root, text=" : ادخل الرابط المراد تنزيله ",font=("Tajawal" , 16, BOLD))
ytdLable.pack()

#entery box
ytdEntryVar = StringVar()
ytdEntry = Entry(root,width=70,justify='center',font=("Tajawal" , 15),fg='olive' , textvariable=ytdEntryVar)
ytdEntry.pack()

#Error msg
ytdError = Label(root ,text=" ملاحظات التحميل " , fg="red" , font=("Tajawal" , 11 ))
ytdError.pack()

#ask save file lable
saveLable = Label(root , text=" : اختر مكان الحفظ ",  bg='white' , font=("Tajawal" , 14 , BOLD))
saveLable.place(x=400 , y=150)

#botton of save file 
saveEntry = Button (root , width=20 ,font=("Tajawal",14) , bg="green" ,fg="#b3abab" ,text=" مسار الحفظ " , command=openLocation )
saveEntry.place(x=390,y=140)

#Error msg 
locationError = Label (root , text  = " لم يتم اختيار مسار الحفظ " , fg="red" ,font=("Tajawal" , 14))
locationError.place (x=40 , y=180)

#download quality
ytdQuality = Label(root, text=" : اختر الجودة التى تريدها", bg="#b3abab" , font=("Tajawal" , 15 , BOLD))
ytdQuality.place(x=450 , y=230)

#combobox
choices = ["720px" , "480px" , "صوت فقط " ]
ytdchoices = ttk.Combobox (root , values = choices , width=12)
ytdchoices.place(x=300,y=235)

#download button
downloadbtn = Button(root, text="  .. ابدأ التحميل " , width=20 ,font=("Tajawal",14),bg="red" , fg="white" , command = Download_Video)
downloadbtn.place(x=30,y=230)

#devoleper lable 
developerlabel = Label(root , wrapper(main) , font=("Tajawal",12))
developerlabel.place(x=262,y=335)
# developerlabell = Label(root,  , font=("Tajawal" , 18))
# developerlabell.place(x=250,y=360)



root.mainloop()

