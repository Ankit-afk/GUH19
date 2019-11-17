#GUH2019 'Moodyfy'

import os
import random
from tkinter.filedialog import askdirectory
from face import Mood

import pygame
from mutagen.id3 import ID3
from tkinter import *


randno = -1




listofsongs = []
realnames = []



flag = True
index = 0

def main():
    root = Tk()
    root.minsize(300,300)
    print("Moodyfing... Please wait...")
    test_list = Mood()
    test = test_list[1]
    print("Emotion: "+ test_list[0])
    print("Music mood: "+ test)
    print(test)
    v = StringVar()
    songlabel = Label(root,textvariable=v,width=35)
    
    mixsong = 0
    def directorychooser():

        #directory = askdirectory()
        directory = os.getcwd()
        directory= directory + "/" + test
        os.chdir(directory)

        for files in os.listdir(directory):
            if files.endswith(".mp3"):
                global randno
                randno+=1
                realdir = os.path.realpath(files)
                print(randno)


                listofsongs.append(files)

        
        global mixsong
        mixsong = random.randint(0,randno)
        print(mixsong,"--after random no.")
        pygame.mixer.init(44100, 16, 2, 1024, allowedchanges=0 )
        while True:
            try:
                print(mixsong,"--try block")
                pygame.mixer.music.load(listofsongs[mixsong])
                break
            except:
                if mixsong == -1:
                    print(mixsong,"--except if block")
                    mixsong = randno
                elif mixsong == randno + 1:
                    mixsong = 0 
                    print(mixsong)
        #pygame.mixer.music.play()
        
    directorychooser()

    def updatelabel():
        global index
        global mixsong
        global flag
        if flag:
            index = mixsong
            print(index,"--mix to index (updatelabel)")
            flag = False
        global songname
        v.set(listofsongs[index])
        #return songname
    updatelabel()

    def nextsong(event):
        global index
        index += 1
        print(index,"--nextsong")
        while True:
            try:
                print(index,"--nextsong try")
                pygame.mixer.music.load(listofsongs[index])
                break
            except:
                if index == -1:
                    print(index,"--nextsong except if")
                    index = randno
                    print(index,"-1 to last")
                elif index == randno+1:
                    print(index,"--nextsong except if")
                    index = 0 
                    print(index,"last+1 to 0")
        pygame.mixer.music.play()
        updatelabel()
    ''' # previous song function can be implemented.
    def prevsong(event):
        global index
        index -= 1
        print(index)
        #while True:
            #try:
            # print(index,"--prevsong try before load")
        pygame.mixer.music.load(listofsongs[index])
                #print(index,"--prevsong try")
                #break
            #except:
                #if index == -1:
                    #print(index,"--prevsong except->if")
                    #index = randno
                    #print(index,"-1 to last ")
                #elif index == randno+1:
                    #print(index,"--prevsong except->elif")
                
                    #index = 0 
                    #print(index,"last+1 to 0")
        pygame.mixer.music.play()
        updatelabel()
    '''

    def stopsong(event):
        pygame.mixer.music.stop()
        v.set("")
        #return songname


    label = Label(root,text='Music Player')
    label.pack()

    listbox = Listbox(root)
    listbox.pack()

    #listofsongs.reverse()
    listofsongs.reverse()

    for items in listofsongs:
        listbox.insert(0,items)

    pygame.mixer.music.play()

    nextbutton = Button(root,text = 'Next Song')
    nextbutton.pack()

    #previousbutton = Button(root,text = 'Previous Song')
    #previousbutton.pack()

    stopbutton = Button(root,text='Stop Music')
    stopbutton.pack()

    nextbutton.bind("<Button-1>",nextsong)
    #previousbutton.bind("<Button-1>",prevsong)
    stopbutton.bind("<Button-1>",stopsong)

    songlabel.pack()

    root.mainloop()
