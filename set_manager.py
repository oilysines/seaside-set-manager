import os
import re
import json
import random
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

path = os.getcwd()

#extracting stagelist data
stagelist = open(r'%s/Stagelist.txt' % path)

starters = []
counterpicks = []

stagefix = ','.join(stagelist)

try:
    starter1 = re.findall(r'(?<=Starters:\W)[\s\S]+(?=\W\WCounterpicks:)',stagefix)[0]
except:
    print('no starter data')
    starter1 = ''
try:
    counterpick1 = re.findall(r'(?<=Counterpicks:\W)[\s\S]+(?=\W\W,DSR:)',stagefix)[0]
except:
    print('no counterpick data')
    counterpick1 = ''
try:
    dsr = re.findall(r'(?<=DSR:[\s\S],)[\s\S]*',stagefix)[0]
except:
    dsr = 'none'

starter1 = starter1.replace(r',','')
counterpick1 = counterpick1.replace(r',','')

starters = starter1.split('\n')
starters = list(filter(None, starters))
counterpicks = counterpick1.split('\n')
counterpicks = list(filter(None,counterpicks))

startercount = len(starters)
counterpickcount = len(counterpicks)

totalcount = startercount + counterpickcount

stagelist.close()
def imagepath(stage):
    f = open(r'%s\StageImages\_filenames.json' % path)
    data = json.load(f)
    for i in data['stages']:
        if i['name'] == stage:
            return i['path']

    f.close()

def incompletestagelist():
    print('Not enough data')
    print('Closing...')
    print('Press ENTER to exit')
    input('')
    exit()

if startercount < 1 or counterpickcount < 1:
    incompletestagelist()

#starter counterpick dsr print
print('Starters:')
print(*starters,sep='\n')
print('\nCounterpicks:')
print(*counterpicks,sep='\n')
print('\nDSR: '+dsr+'\n')

#ban patterns
def pattern(x):
    file = open(r'%s\banpattern.json' % path)
    data = json.load(file)
    for i in data['bans']:
        if i['count'] == x:
            return i['pattern']

    file.close()

banpatt = pattern(startercount)
# counterpick values
_2co = 1
_3co = 1
_4co = 1
_5co = 1
_6co = 1
_7co = 2
_8co = 2
_9co = 2
_10co = 2
_11co = 3
_12co = 3
c_val = globals()[f'_{totalcount}co']

#set up tkinter
w = 960
h = 540
root = tk.Tk()
root.iconbitmap(r'%s\cosmetic\ssbmbf.ico' % path)
root.title('Seaside Set Manager')
root.geometry(str(w)+'x'+str(h))
root.resizable(False,False)

p1= tk.StringVar()
p1.set("")
p2 = tk.StringVar()
p2.set("")

settingsframe = Frame(root, width = h/3, height = h/5)
settingsframe.pack(side = TOP, anchor = NE)

topframe = Frame(root, width = w, height = h/20)
topframe.pack(side = TOP, anchor = N)
topframe.columnconfigure((0,2),weight=1)

centerframe = Frame(root, width = w, height = h/2)
centerframe.place(relx=0.5,rely=0.5,anchor=CENTER)

bottomframe = Frame(root, width = w, height = h/4)
bottomframe.pack(side = BOTTOM)

for i in range(5,13):
    bottomframe.grid_columnconfigure((i), weight = 1)
bottomframe.grid_rowconfigure(1,weight = 1)

#Starter Coinflip
flipwinner = ''
flip = random.randint(0,1)
if flip == 0:
    flipwinner = 'Player 1'
elif flip == 1:
    flipwinner = 'Player 2'
turn = str(flipwinner)
pnameturn = str(turn)

#settings widgets
settings = Label(settingsframe, width = int(h/28), text = 'Settings', font = ('bahnschrift',16))
bo3 = Label(settingsframe, text = 'bo3', font = ('bahnschrift',10))
bo5 = Label(settingsframe, text = 'bo5', font = ('bahnschrift',10))

toggleleft = Image.open(r'%s\cosmetic\toggleleft.png' % path)
toggleleft = toggleleft.resize((35,14))
toggleleft = ImageTk.PhotoImage(toggleleft)

toggleright = Image.open(r'%s\cosmetic\toggleright.png' % path)
toggleright = toggleright.resize((35,14))
toggleright = ImageTk.PhotoImage(toggleright)

tval = 0
winval = 2

def toggle():
    global tval, winval
    if startvar == 0:
        if tval == 0:
             tval = 1
             winval = 3
             settoggle.config(image = toggleright)
        elif tval == 1:
            tval = 0
            winval = 2
            settoggle.config(image = toggleleft)
settoggle = Button(settingsframe, command = toggle, image = toggleleft, relief = FLAT)

p1t = Label(settingsframe, text = 'Player 1', font = ('bahnschrift',10), padx = 5, pady = 5)
p1e = Entry(settingsframe, textvariable = p1)

p2t = Label(settingsframe, text = 'Player 2', font = ('bahnschrift',10), padx = 5, pady = 5)
p2e = Entry(settingsframe, textvariable = p2)

#positioning settings widgets
settingsframe.grid_columnconfigure((0,1,2),weight = 1)
settingsframe.grid_rowconfigure(0,weight = 1)
settings.grid(row = 0, column = 0, columnspan = 3, sticky = "e")


bo3.grid(row = 1, column = 0, sticky = "ew")
settoggle.grid(row = 1, column = 1, sticky = "ew")
bo5.grid(row = 1, column = 2, sticky = "ew")

p1t.grid(row = 2, column = 0, sticky = "ew", padx = 0, pady = 0)
p1e.grid(row = 2, column = 1, columnspan = 2, sticky = "ew", padx = 20)
p2t.grid(row = 3, column = 0, sticky = "ew", padx = 0, pady = 0)
p2e.grid(row = 3, column = 1, columnspan = 2, sticky = "ew", padx = 20)

#striking
labelname = ''

x1 = Image.open(r'%s\StageImages\x.png' % path)
x1r = x1.resize((128,112))
x1p = ImageTk.PhotoImage(x1r)

strikelist = list(starters)
strikevar = 0
strikestep = 0
#some commands are related variables
p1_winlist = []
p2_winlist = []

player1 = ''
player2 = ''

winbutton_p1 = Button(bottomframe, font = ('bahnschrift', 10))
winbutton_p2 = Button(bottomframe, font = ('bahnschrift', 10))
gwinl = Label(bottomframe, text = 'Game Winner', font = ('bahnschrift', 12))

active_alt = Label(root, text = '', font = ('bahnschrift', 20), justify = CENTER)
active_alt.place(relx=0.5, rely = 0.2, anchor = CENTER)
def midgame_checkup():
    global p1_winlist, p2_winlist, actp, maxg, winval, strikevar, strikestep, active_alt, strikelist, g_no
    if len(p1_winlist) == winval:
        active_alt.config(text = player1+' wins the set '+str(len(p1_winlist))+'-'+str(len(p2_winlist)))
    elif len(p2_winlist) == winval:
        active_alt.config(text = player2+' wins the set '+str(len(p2_winlist))+'-'+str(len(p1_winlist)))
    else:
        strikelist = list(starters)
        strikelist.extend(counterpicks)
        strikevar = 0
        strikestep = 0
        game(g_no)

def stageshred():
    for i in range(0,startercount):
        try:
            globals()[f's{i}label'].destroy()
        except:
            pass
    for i in range(0, counterpickcount):
        try:
            globals()[f'c{i}label'].destroy()
        except:
            pass
    print('Player 1 Wins:',*p1_winlist, sep = '\n')
    print('Player 2 Wins:',*p2_winlist, sep = '\n')
    midgame_checkup()

def p1win():
    global p1_winlist, p2_winlist, winbutton_p1, winbutton_p2, gwinl, actp, turn
    p1_winlist.append(globals()[f'stage{g_no}'])
    winbutton_p1.grid_forget()
    winbutton_p2.grid_forget()
    gwinl.grid_forget()
    turn = 'Player 1'
    globals()[f'g{g_no}winner'] = 'p1'
    active_alt.config(text = player1+"'s Ban")
    if g_no == 1:
        actp.destroy()
    stageshred()

def p2win():
    global p1_winlist, p2_winlist, winbutton_p1, winbutton_p2, gwinl, actp, turn
    p2_winlist.append(globals()[f'stage{g_no}'])
    winbutton_p1.grid_forget()
    winbutton_p2.grid_forget()
    gwinl.grid_forget()
    turn = 'Player 2'
    globals()[f'g{g_no}winner'] = 'p2'
    active_alt.config(text = player2+"'s Ban")
    if g_no == 1:
        actp.destroy()
    stageshred()

def promptwinner():
    global player1, player2
    winbutton_p1.config(command = p1win, text = player1+' Win')
    winbutton_p2.config(command = p2win, text = player2+' Win')
    winbutton_p1.grid(row = 1, rowspan = 3, column = 0, columnspan = 3, padx = 20, pady = 5, sticky = 'nsew')
    gwinl.grid(row = 1, column = 3, sticky = 'ew')
    winbutton_p2.grid(row = 1, rowspan = 4, column = 5, columnspan = 3, padx = 20, pady = 5, sticky = 'nsew')

def switch():
    global turn, pnameturn
    if turn == 'Player 1':
        turn = 'Player 2'
        if p2.get() != '':
            pnameturn = p2.get()
        else:
            pnameturn = str(turn)
    elif turn == 'Player 2':
        turn = 'Player 1'
        if p1.get() != '':
            pnameturn = p1.get()
        else:
            pnameturn = str(turn)
    if len(strikelist) > 1 and g_no == 1:
        actp.config(text = pnameturn+"'s Ban")
    elif g_no >= 2 and len(strikelist) == totalcount - c_val:
        active_alt.config(text = pnameturn+"'s *Choice*")
    elif g_no > 1:
        active_alt.config(text = pnameturn+"'s Ban")

def null():
    pass

def widgetnull():
    for i in range(0,startercount):
        globals()[f's{i}label'].config(command = null)
    for n in range(0, counterpickcount):
        globals()[f'c{n}label'].config(command = null)

correspond = ''
chooselist = []
returnlist = []
stage1 = ''
stage2 = ''
stage3 = ''
stage4 = ''
stage5 = ''
def strike(labelname, stagetype, mode):
    global strikelist, starters, activep, listno, strikevar, strikestep
    global totalcount, correspond, g_no, c_val, chooselist, dsr, returnlist
    listno = int(re.findall(r'\d',labelname)[0])
    if stagetype == 'starter':
        correspond = str(starters[listno])
    if stagetype =='counterpick':
        correspond = str(counterpicks[listno])
    if mode == 'strike' and not len(strikelist) == 1:
        globals()[labelname].config(image = x1p)
        try:
            if stagetype == 'starter':
                strikelist.remove(starters[listno])
            elif stagetype == 'counterpick':
                strikelist.remove(counterpicks[listno])
        except:
            f2c = re.findall(r'.\d',labelname)[0]
            globals()[labelname].config(image = globals()[f'{f2c}photo'])
            strikelist.append(correspond)
            strikevar += -1

            if g_no == 1:
                if len(strikelist) <= startercount - sum(banpatt[:strikestep-1]):
                    switch()
                    strikestep += -1
            elif g_no > 1:
                switch()
                for stage in strikelist:
                    for ele in starters:
                        if stage == ele:
                            returnlist.append('s'+str(starters.index(stage))+'label')
                    for ele in counterpicks:
                        if stage == ele:
                            returnlist.append('c'+str(counterpicks.index(stage))+'label')
                for label in returnlist:
                    if label[0] == 's':
                        globals()[label].config(command = lambda labelname = label, stagetype = 'starter', mode = 'strike': strike(labelname, stagetype, mode))
                    elif label[0] == 'c':
                        globals()[label].config(command = lambda labelname = label, stagetype = 'counterpick', mode = 'strike': strike(labelname, stagetype, mode))
                returnlist.clear()
        if g_no == 1:
            if len(strikelist) == startercount - sum(banpatt[:strikestep+1]):
                switch()
                strikestep += 1
        elif g_no > 1:
            if len(strikelist) == totalcount - c_val:
                chooselist.clear()
                for stage in strikelist:
                    for ele in starters:
                        if stage == ele:
                            chooselist.append('s'+str(starters.index(stage))+'label')
                    for ele in counterpicks:
                        if stage == ele:
                            chooselist.append('c'+str(counterpicks.index(stage))+'label')
                for label in chooselist:
                    if label[0] == 's':
                        globals()[label].config(command = lambda labelname = label, stagetype = 'starter', mode = 'choose': strike(labelname, stagetype, mode))
                    elif label[0] == 'c':
                        globals()[label].config(command = lambda labelname = label, stagetype = 'counterpick', mode = 'choose': strike(labelname, stagetype, mode))
                chooselist.clear()
                switch()
        if len(strikelist) == 1:
            globals()[f'stage{g_no}'] = strikelist[0].replace('Ã©','é')
            print('Game',g_no,'Stage: '+globals()[f'stage{g_no}'])
            actp.config(text = 'Game '+str(g_no)+': '+globals()[f'stage{g_no}'])
            promptwinner()
        
    elif mode == 'choose':
        f2c = re.findall(r'.\d',labelname)[0]
        if f2c[0] == 's':
            globals()[f'stage{g_no}'] = starters[int(f2c[1])].replace('Ã©','é')
            print('Game ',g_no,'Stage: '+globals()[f'stage{g_no}'])
        if f2c[0] == 'c':
            globals()[f'stage{g_no}'] = counterpicks[int(f2c[1])].replace('Ã©','é')
            print('Game',g_no,'Stage: '+globals()[f'stage{g_no}'])
        active_alt.config(text = 'Game '+str(g_no)+' Stage: '+globals()[f'stage{g_no}'])
        widgetnull()
        promptwinner()
    else:
        pass

def starter_labelmake():
    for i in range(0,startercount):
        globals()[f's{i}file'] = Image.open(r'%s\StageImages\%s' % (path, imagepath(starters[i])))
        globals()[f's{i}resize'] = globals()[f's{i}file'].resize((128,112))
        globals()[f's{i}photo'] = ImageTk.PhotoImage(globals()[f's{i}resize'])
        globals()[f's{i}label'] = Button(centerframe, image=globals()[f's{i}photo'])
        globals()[f's{i}label'].config(command = lambda labelname = f's{i}label', stagetype = 'starter', mode = 'strike': strike(labelname, stagetype, mode))

def counterpick_labelmake():
    for n in range(0,counterpickcount):
        globals()[f'c{n}file'] = Image.open(r'%s\StageImages\%s' % (path, imagepath(counterpicks[n])))
        globals()[f'c{n}resize'] = globals()[f'c{n}file'].resize((128,112))
        globals()[f'c{n}photo'] = ImageTk.PhotoImage(globals()[f'c{n}resize'])
        globals()[f'c{n}label'] = Button(centerframe, image=globals()[f'c{n}photo'])
        globals()[f'c{n}label'].config(command = lambda labelname = f'c{n}label', stagetype = 'counterpick', mode = 'strike': strike(labelname, stagetype, mode))

dsr1file = Image.open(r'%s\StageImages\x1dsr.png' % path)
dsr1resize = dsr1file.resize((128,112))
dsr1photo = ImageTk.PhotoImage(dsr1resize)

dsr2file = Image.open(r'%s\StageImages\x2dsr.png' % path)
dsr2resize = dsr2file.resize((128,112))
dsr2photo = ImageTk.PhotoImage(dsr2resize)

g_no = 0
def game(g_num):
    global actp, strikelist, active_alt, pnameturn, g_no, chooselist
    chooselist.clear()
    g_no = g_num+1
    if g_no == 1:
        for i in range(0,startercount):
            globals()[f's{i}label'].grid(row = 0, column = 2*i, columnspan = 2, padx = 10, pady = 10)
    if g_no == 2:
        starter_labelmake()
        counterpick_labelmake()
        for i in range(0,startercount):
            globals()[f's{i}label'].grid(row = 0, column = 2*i, columnspan = 2, padx = 10, pady = 10)
        for i in range(0, counterpickcount):
            globals()[f'c{i}label'].grid(row = 3, column = 2*i+1, columnspan = 2, padx = 10, pady = 10)
    if g_no >= 3:
        starter_labelmake()
        counterpick_labelmake()
        if dsr == 'on':
            for stage in p1_winlist:
                for ele in starters:
                    if stage == ele:
                        print('s'+str(starters.index(stage))+'label')
                        chooselist.append('s'+str(starters.index(stage))+'label')
                for ele in counterpicks:
                    if stage == ele:
                        print('c'+str(counterpicks.index(stage))+'label')
                        chooselist.append('c'+str(counterpicks.index(stage))+'label')
            for label in chooselist:
                globals()[label].config(command = null, image = dsr1photo)
            chooselist.clear()
            for stage in p2_winlist:
                for ele in starters:
                    if stage == ele:
                        print('s'+str(starters.index(stage))+'label')
                        chooselist.append('s'+str(starters.index(stage))+'label')
                for ele in counterpicks:
                    if stage == ele:
                        print('c'+str(counterpicks.index(stage))+'label')
                        chooselist.append('c'+str(counterpicks.index(stage))+'label')
            for label in chooselist:
                globals()[label].config(command = null, image = dsr2photo)
            chooselist.clear()

        for i in range(0,startercount):
            globals()[f's{i}label'].grid(row = 0, column = 2*i, columnspan = 2, padx = 10, pady = 10)
        for i in range(0, counterpickcount):
            globals()[f'c{i}label'].grid(row = 3, column = 2*i+1, columnspan = 2, padx = 10, pady = 10)

startvar = 0
def start():
    global startvar, actp, game, turn, g_no
    global p1, p2, player1, player2, turn, pnameturn
    if startvar == 0:
        startvar += 1
        starter_labelmake()
        if not p1.get() == '':
            player1 = p1.get()
            if turn == 'Player 1':
                pnameturn = p1.get()
        elif p1.get() == '':
            player1 = 'Player 1'
        if not p2.get() == '':
            player2 = p2.get()
            if turn == 'Player 2':
                pnameturn = p2.get()
        elif p2.get() == '':
            player2 = 'Player 2'
        actp = Label(topframe, text = pnameturn+"'s Ban", font = ('bahnschrift', 24), justify = 'center')
        actp.grid(column = 1, columnspan = 3)
        game(0)

start = Button(root, text = 'Start', command = start, font = ('bahnschrift', 12), bg = 'white', padx = 5, pady = 5)
start.place(relx = 0, rely = 0)

root.mainloop()
