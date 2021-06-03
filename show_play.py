#!/bin/python3

from tkinter import *
import pandas as pd
import time
import math
import sys
import pickle

# show_play.py play (only one argument)


"""       Functions            """

def paint_gridiron(canvas):
    canvas.create_rectangle(0,0,99,530,fill="blue")
    canvas.create_rectangle(1101,0,1200,530,fill="red")


    for i in range(100,1150,50):
        if i == 600:
            canvas.create_line(i, 0, i, 530,width=6,fill="white")
        elif (i - 50) % 100 == 50:
            canvas.create_line(i, 0, i, 530,width=3,fill="white")
        else:
            canvas.create_line(i, 0, i, 530,width=1,fill="white")
        
        if i != 100 and i != 1100:
            if i != 600:
                w=3
                d=5
            else:
                w=5
                d=8
            canvas.create_line(i-d,197,i+d,197,fill="white",width=w)
            canvas.create_line(i-d,333,i+d,333,fill="white",width=w)

    count = 1
    other_side = False
    for i in range(110,1000,100):
        canvas.create_text(i+80,510,fill="white",font=("Purisa",14),text=str(count))
        canvas.create_text(i+100,510,fill="white",font=("Purisa",14),text="0")
        
        canvas.create_text(i+80,20,fill="white",font=("Purisa",14),text="0",angle=180)
        canvas.create_text(i+100,20,fill="white",font=("Purisa",14),text=str(count),angle=180)
        
        if not other_side:
            count+=1
        else:
            count-=1
        
        if count == 5:
            other_side = True
    
    for i in range(100,1100,10):
        canvas.create_line(i,197,i,202,fill="white",width=1)
        canvas.create_line(i,327,i,333,fill="white",width=1)
        
    

def paint_los(canvas,x):
    canvas.create_line(x,0,x,530,fill="blue",width=3)#,dash=(4,2))
    
def paint_first_down_line(canvas,yardsToGo,los,direction):
    canvas.create_line(los+(yardsToGo*direction),0,los+(yardsToGo*direction),530,fill="yellow",width=3)
    
def print_lines(canvas):
    #obtain direction
    global playId
    global play
    global play_info
    
    if play["playDirection"].all() == "left":
        direction = -1
    else:
        direction = 1
    
    paint_first_down_line(canvas,int(play_info["yardsToGo"])*10,int(play_info["absoluteYardlineNumber"])*10,direction)
    paint_los(canvas,int(play_info["absoluteYardlineNumber"])*10)
    
def paint_football(canvas,x,y):
    x0 = x - 3
    y0 = y - 3
    x1 = x + 3
    y1 = y + 3
    canvas.create_oval(x0,y0,x1,y1,fill="brown")
    
def paint_player(canvas,x,y,pos,o):
    x0 = x - 6
    y0 = y - 6
    x1 = x + 6
    y1 = y + 6
    if pos == "offense":
        colour = "blue"
    elif pos == "defense":
        colour = "red"
    canvas.create_oval(x0,y0,x1,y1,fill=colour)
    
    #canvas.create_line(x,y,x+math.sin(o),y+math.cos(o),arrow=LAST)

def print_frame(canvas,frame):
    for index,row in frame.iterrows():
        if row["position"] in ['QB', 'WR', 'RB', 'TE', 'FB', 'HB', 'P', 'LS', 'K']:
            pos = "offense"
            paint_player(canvas,int(row["x"])*10,530-int(row["y"])*10,pos,row["o"])
            canvas.create_text(int(row["x"])*10,530-int(row["y"])*10,font=("Purisa",5),fill="white",text=int(row["jerseyNumber"]))
        elif row["position"] in ['SS','FS','MLB','CB','LB','OLB','ILB','DL','DB','NT','S','DT']: 
            pos = "defense"
            paint_player(canvas,int(row["x"])*10,530-int(row["y"])*10,pos,row["o"])
            canvas.create_text(int(row["x"])*10,530-int(row["y"])*10,font=("Purisa",5),fill="white",text=int(row["jerseyNumber"]))
        elif row["displayName"] == "Football":
            paint_football(canvas,int(row["x"])*10,530-int(row["y"])*10)
    
    print_lines(canvas)
    
def advance_play():
    canvas.delete("all")
    paint_gridiron(canvas)
    global frameId
    global play
    frameId+=1
    frame = play[play["frameId"]==frameId]
    print_frame(canvas,frame)
    return


def back_play():
    canvas.delete("all")
    paint_gridiron(canvas)
    global frameId
    frameId-=1
    frame = play[play["frameId"]==frameId]
    print_frame(canvas,frame)
    return


def previous_play():
    global actualPlay
    global number_plays
    global play_info
    global play
    
    if actualPlay == number_plays - 1:
        next_play_button["state"] = NORMAL
        
    actualPlay-=1
    if actualPlay == 0:
        previous_play_button["state"] = DISABLED
    
    canvas.delete("all")
    paint_gridiron(canvas)
    global frameId
    frameId = 1
    
    actualPlayId = plays[actualPlay]
    
    idParts = actualPlayId.split(":")
    week = idParts[2]
    
    play = pd.read_csv(WEEKS_ROUTE.replace("@",week))
    play = play[play["id"]==actualPlayId]
    
    play_info = pd.read_csv(PLAYS_ROUTE)
    play_info = play_info[play_info["id"]==actualPlayId]
    
    frame = play[play["frameId"]==frameId]
    print_frame(canvas,frame)
    print("Estas viendo la jugada: ",actualPlayId)
    print_players_console()
    return
    
def next_play():
    global actualPlay
    global number_plays
    global play_info
    global play
    
    if actualPlay == 0:
        previous_play_button["state"] = NORMAL
        
    actualPlay+=1
    if actualPlay == number_plays -1:
        next_play_button["state"] = DISABLED
    
    canvas.delete("all")
    paint_gridiron(canvas)
    global frameId
    frameId = 1
    
    actualPlayId = plays[actualPlay]
    
    idParts = actualPlayId.split(":")
    week = idParts[2]
    
    play = pd.read_csv(WEEKS_ROUTE.replace("@",week))
    play = play[play["id"]==actualPlayId]
    
    play_info = pd.read_csv(PLAYS_ROUTE)
    play_info = play_info[play_info["id"]==actualPlayId]
    
    frame = play[play["frameId"]==frameId]
    print_frame(canvas,frame)
    print("Estas viendo la jugada: ",actualPlayId)
    print_players_console()
    return
    
def print_players_console():
    global show_defense
    global show_offense
    
    if show_offense:
        frame1 = play[play["frameId"]==1]
        print("OFFENSE TEAM")
        for index,row in frame1.iterrows():
            if row["position"] in ['QB', 'WR', 'RB', 'TE', 'FB', 'HB', 'P', 'LS', 'K']:
                print("{} {} {}".format(row["displayName"],row["jerseyNumber"],row["position"]))
        print()
    
    if show_defense:
        frame1 = play[play["frameId"]==1]
        print("DEFENSE TEAM")
        for index,row in frame1.iterrows():
            if row["position"] in ['SS','FS','MLB','CB','LB','OLB','ILB','DL','DB','NT','S','DT']:
                print("{} {} {}".format(row["displayName"],row["jerseyNumber"],row["position"]))
        print()
####################################

PLAYS_ROUTE = "processed_data/remove_st_nbt_spikes/plays.csv"
WEEKS_ROUTE = "processed_data/remove_st_nbt_spikes/week@.csv"


if len(sys.argv) == 1:
    play_info = pd.read_csv(PLAYS_ROUTE)
    unique_plays = play_info["id"].unique()
    for play in unique_plays:
        print(play)
    sys.exit(0)
    
show_offense = False
show_defense = False

frameId = 1

if sys.argv[1][len(sys.argv[1])-7:len(sys.argv[1])-1]:
    pickle_file = open(sys.argv[1],'rb')
    plays = pickle.load(pickle_file)
    print("Se han añadido ",len(plays)," jugadas.")
    print("Insertadas las jugadas:")
    cont = 0
    for play in plays:
        print("\t",cont,".- ",play)
        cont+=1
else:
    plays = sys.argv[1].split(",")
    
number_plays = len(plays)

actualPlay = 0
actualPlayId = plays[actualPlay]


idParts = actualPlayId.split(":")
week = idParts[2]

play = pd.read_csv(WEEKS_ROUTE.replace("@",week))
play = play[play["id"]==actualPlayId]

print("Estas viendo la jugada: ",actualPlayId)

play_info = pd.read_csv(PLAYS_ROUTE)
play_info = play_info[play_info["id"]==actualPlayId]

if len(sys.argv) > 2:
    if "o" in sys.argv[2]:
        show_offense = True
    if "d" in sys.argv[2]:
        show_defense = True

print_players_console()
    
ventana = Tk()

ventana.geometry("1200x640")

ventana .configure(bg="green")

ventana.title("GridIron")

canvas = Canvas(width=1200,height=530,bg="green")

back_button = Button(ventana,text="Back",command=back_play)
back_button.place(x=0,y=540)
#back_button["state"] = DISABLED

advance_button = Button(ventana,text="Advance",command=advance_play)
advance_button.place(x=70,y=540)

previous_play_button = Button(ventana,text="Previous play",command=previous_play)
previous_play_button.place(x=0,y=580)
previous_play_button["state"] = DISABLED

next_play_button = Button(ventana,text="Next play", command=next_play)
next_play_button.place(x=140,y=580)
if number_plays == 1:
    next_play_button["state"] = DISABLED

canvas.pack(expand=YES, fill=BOTH)
#canvas.bind('<Button-1>',clean_play)

paint_gridiron(canvas)


first_frame = play[play["frameId"]==1]
#frameId = 1

print_frame(canvas,first_frame)


ventana.mainloop()






