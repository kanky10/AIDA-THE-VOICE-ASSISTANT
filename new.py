import datetime,wikipedia,webbrowser,os,random,requests,pyautogui,playsound,subprocess,time
import urllib.request,bs4 as bs,sys,threading
import Annex, wolframalpha
from ttkthemes import themed_tk
from tkinter import ttk
import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageTk,Image
import sqlite3,pyjokes,pywhatkit
from functools import partial
import getpass,calendar

import keyboard
import winshell
import sys # we will use sys.exit to exit the program 
import pygame
from pygame.locals import * # basic pygame import




try:
    app=wolframalpha.Client("RW6QLR-PL7J46Q4Y4")  #API key for wolframalpha
except Exception as e:
    pass

#setting chrome path
chrome_path="C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"

def there_exists(terms,query):
    for term in terms:
        if term in query:
            return True

def CommandsList():
    '''show the command to which voice assistant is registered with'''
    os.startfile('Commands List.txt')

def clearScreen():
    ''' clear the scrollable text box'''
    SR.scrollable_text_clearing()

def greet():
    conn = sqlite3.connect('Aida.db')
    mycursor=conn.cursor()
    hour=int(datetime.datetime.now().hour)
    if hour>=4 and hour<12:
        mycursor.execute('select sentences from goodmorning')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    elif hour>=12 and hour<18:
        mycursor.execute('select sentences from goodafternoon')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    elif hour>=18 and hour<21:
        mycursor.execute('select sentences from goodevening')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    else:
        mycursor.execute('select sentences from night')
        result=mycursor.fetchall()
        SR.speak(random.choice(result)[0])
    conn.commit()
    conn.close()
    SR.speak("\nMyself AIDA. How may I help you?")

def flappybird():
#global variable for the game 
    FPS = 32
    SCREENWIDTH = 289 
    SCREENHEIGHT = 511
    SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
    GROUNDY = SCREENHEIGHT * 0.8 
    GAME_SPRITES = {}
    GAME_SOUNDS = {}
    PLAYER = 'gallery/sprites/bird.png'
    BACKGROUND = 'gallery/sprites/background.png'
    PIPE = 'gallery/sprites/pipe.png'

    def welcomeScreen():
        
        playerx = int(SCREENWIDTH/5)
        playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
        messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
        messagey = int(SCREENHEIGHT*0.13)
        basex = 0
        while True:
            for event in pygame.event.get():
                #if user clicks on cross button, close the game
                if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                    # if the user presses space or up key, start the game for them 
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    return
                else:
                    SCREEN.blit(GAME_SPRITES['background'], (0,0))
                    SCREEN.blit(GAME_SPRITES['player'], (playerx,playery))
                    SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey))
                    SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)

    def mainGame():
        score = 0
        playerx = int(SCREENWIDTH/5)
        playery = int(SCREENWIDTH/2)
        basex = 0

        #Create 2 pipes for blitting on the screen

        newPipe1 = getRandomPipe()
        newPipe2 = getRandomPipe()

        #my list of uper pipes
        upperPipes = [
            {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
            {'x': SCREENWIDTH+200 + (SCREENWIDTH/2), 'y':newPipe1[0]['y']},
        ]

        lowerPipes = [
            {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
            {'x': SCREENWIDTH+200 + (SCREENWIDTH/2), 'y':newPipe2[1]['y']},
        ]

        pipeVelX = -4

        playerVelY = -9
        playerMaxVelY = 10
        playerMinVelY = -8
        playerAccY = 1

        playerFlapAccv = -8 #Velocity while flapping 
        playerFlapped = False # It is true only when the bird is flapping 

        while True: 
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if playery > 0: 
                        playerVelY = playerFlapAccv
                        playerFlapped = True
                        GAME_SOUNDS['wing'].play()
            
            crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) 
            if crashTest:
                return
            
            playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
                if pipeMidPos<= playerMidPos < pipeMidPos +4: 
                    score +=1 
                    print(f"Your score is {score}")
                    GAME_SOUNDS['point'].play()

            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY
            
            if playerFlapped:
                playerFlapped = False
            playerHeight = GAME_SPRITES['player'].get_height()
            playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

            for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX
            
            if 0< upperPipes[0]['x']<5:
                newpipe = getRandomPipe()
                upperPipes.append(newpipe[0])
                lowerPipes.append(newpipe[1])

            if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)

            SCREEN.blit(GAME_SPRITES['background'], (0, 0))
            for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
                SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
                SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
    
            
            
            SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
            SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
            myDigits = [int(x) for x in list(str(score))]
            width = 0
            for digit in myDigits:
                width += GAME_SPRITES['numbers'][digit].get_width()
            Xoffset = (SCREENWIDTH - width)/2

            for digit in myDigits:
                SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
                Xoffset += GAME_SPRITES['numbers'][digit].get_width()

            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def isCollide(playerx, playery, upperPipes, lowerPipes):
        if playery > GROUNDY -25 or playery<0:
            GAME_SOUNDS['hit'].play()
            return True
        
        for pipe in upperPipes:
            pipeHeight = GAME_SPRITES['pipe'][0].get_height()
            if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x'])< GAME_SPRITES['pipe'][0].get_width()):
                GAME_SOUNDS['hit'].play()
                return True
        for pipe in lowerPipes:
            if (playery + GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerx - pipe['x'])< GAME_SPRITES['pipe'][0].get_width()):
                GAME_SOUNDS['hit'].play()
                return True
            


        return False


    def getRandomPipe():

        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        offset = SCREENHEIGHT/3
        y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() -1.2*offset))
        pipeX = SCREENWIDTH + 10
        y1 = pipeHeight - y2 + offset
        pipe = [
            {'x': pipeX, 'y': -y1}, #upper pipe 
            {'x': pipeX, 'y': y2} #lower pipe 

        ]
        return pipe 

    if __name__== "__main__":
        #this will the main function from where our game will start 
        pygame.init() #initiates all pygames modules
        FPSCLOCK = pygame.time.Clock()
        pygame.display.set_caption("Flappy Bird by Kanishk Dedhia")
        GAME_SPRITES['numbers'] = (
            pygame.image.load('gallery/sprites/0.png').convert_alpha(), 
            pygame.image.load('gallery/sprites/1.png').convert_alpha(),
            pygame.image.load('gallery/sprites/2.png').convert_alpha(),
            pygame.image.load('gallery/sprites/3.png').convert_alpha(),
            pygame.image.load('gallery/sprites/4.png').convert_alpha(),
            pygame.image.load('gallery/sprites/5.png').convert_alpha(),
            pygame.image.load('gallery/sprites/6.png').convert_alpha(),
            pygame.image.load('gallery/sprites/7.png').convert_alpha(),
            pygame.image.load('gallery/sprites/8.png').convert_alpha(),
            pygame.image.load('gallery/sprites/9.png').convert_alpha(),
        
        )

        GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
        GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
        GAME_SPRITES['pipe'] = (

        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
        )

    #Games sounds
        GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
        GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
        GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
        GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
        GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

        GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
        GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

        while True: 
            welcomeScreen() #Shows welcome screen to the user until the button is presses
            mainGame() # this is main game function


def mainframe():
    """Logic for execution task based on query"""
    SR.scrollable_text_clearing()
    greet()
    query_for_future=None
    try:
        while(True):
            query=SR.takeCommand().lower()          #converted the command in lower case of ease of matching

            #wikipedia search
            if there_exists(['search wikipedia for','from wikipedia'],query):
                SR.speak("Searching wikipedia...")
                if 'search wikipedia for' in query:
                    query=query.replace('search wikipedia for','')
                    results=wikipedia.summary(query,sentences=2)
                    SR.speak("According to wikipedia:\n")
                    SR.speak(results)
                elif 'from wikipedia' in query:
                    query=query.replace('from wikipedia','')
                    results=wikipedia.summary(query,sentences=2)
                    SR.speak("According to wikipedia:\n")
                    SR.speak(results)
            elif there_exists(['wikipedia'],query):
                SR.speak("Searching wikipedia....")
                query=query.replace("wikipedia","")
                results=wikipedia.summary(query,sentences=2)
                SR.speak("According to wikipedia:\n")
                SR.speak(results)

            #jokes
            elif there_exists(['tell me joke','tell me a joke','tell me some jokes','i would like to hear some jokes',"i'd like to hear some jokes",
                            'can you please tell me some jokes','i want to hear a joke','i want to hear some jokes','please tell me some jokes',
                            'would like to hear some jokes','tell me more jokes','can you tell me joke'],query):
                SR.speak(pyjokes.get_joke(language="en", category="all"))
                query_for_future=query
            elif there_exists(['one more','one more please','tell me more','i would like to hear more of them','once more','once again','more','again'],query) and (query_for_future is not None):
                SR.speak(pyjokes.get_joke(language="en", category="all"))

            #asking for name
            elif there_exists(["what is your name","what's your name","tell me your name",'who are you'],query):
                SR.speak("My name is Artifical Intelligent Digital Assistant but you can call me AIDA and I'm here to serve you.")
            #How are you
            elif there_exists(['how are you', 'how are you doing AIDA', 'how are you doing','how are you aida'],query):
                conn = sqlite3.connect('Aida.db')
                mycursor=conn.cursor()
                mycursor.execute('select sentences from howareyou')
                result=mycursor.fetchall()
                temporary_data=random.choice(result)[0]
                SR.updating_ST_No_newline(temporary_data+'😃\n')
                SR.nonPrintSpeak(temporary_data)
                conn.close()
            #what is my name
            elif there_exists(['what is my name','tell me my name',"i don't remember my name", "can you tell me my name","if you dont mind telling me my name"],query):
                SR.speak("Your name is "+str(getpass.getuser()))

            #calendar
            elif there_exists(['show me calendar','display calendar','show calendar','open calendar'],query):
                SR.updating_ST(calendar.calendar(2023))

            #google, youtube and location
            #playing on youtube
            elif there_exists(['open youtube and play','on youtube'],query):
                if 'on youtube' in query:
                    SR.speak("Opening youtube")
                    pywhatkit.playonyt(query.replace('on youtube',''))
                else:
                    SR.speak("Opening youtube")
                    pywhatkit.playonyt(query.replace('open youtube and play ',''))
                break
            elif there_exists(['play some songs on youtube','i would like to listen some music','i would like to listen some songs','play songs on youtube'],query):
                SR.speak("Opening youtube")
                pywhatkit.playonyt('play random songs')
                break
            elif there_exists(['open youtube','access youtube','open youtube for me','open youtube','can you open youtube', 'can you open youtube for me','if you dont mind opening youtube for me','please open open youtube if you dont mind','please open youtube for me', 'can you please open youtube for me','can you please open youtube','please open youtube'],query):
                SR.speak("Opening youtube")
                webbrowser.open("www.youtube.com")
                break
            elif there_exists(['open google and search','google and search'],query):
                url='https://google.com/search?q='+query[query.find('for')+4:]
                webbrowser.get(chrome_path).open(url)
                break
            #image search
            elif there_exists(['show me images of','images of','display images'],query):
                url="https://www.google.com/search?tbm=isch&q="+query[query.find('of')+3:]
                webbrowser.get(chrome_path).open(url)
                break
            elif there_exists(['search for','do a little searching for','show me results for','show me result for','start searching for'],query):
                SR.speak("Searching.....")
                if 'search for' in query:
                    SR.speak(f"Showing results for {query.replace('search for','')}")
                    pywhatkit.search(query.replace('search for',''))
                elif 'do a little searching for' in query:
                    SR.speak(f"Showing results for {query.replace('do a little searching for','')}")
                    pywhatkit.search(query.replace('do a little searching for',''))
                elif 'show me results for' in query:
                    SR.speak(f"Showing results for {query.replace('show me results for','')}")
                    pywhatkit(query.replace('show me results for',''))
                elif 'start searching for' in query:
                    SR.speak(f"Showing results for {query.replace('start searching for','')}")
                    pywhatkit(query.replace('start searching for',''))
                break

            elif there_exists(['open google'],query):
                SR.speak("Opening google")
                webbrowser.get(chrome_path).open("google.com")
                break
            elif there_exists(['find location of','show location of','find location for','show location for'],query):
                if 'of' in query:
                    url='https://google.nl/maps/place/'+query[query.find('of')+3:]+'/&amp'
                    webbrowser.get(chrome_path).open(url)
                    break
                elif 'for' in query:
                    url='https://google.nl/maps/place/'+query[query.find('for')+4:]+'/&amp'
                    webbrowser.get(chrome_path).open(url)
                    break
            elif there_exists(["what is my exact location","What is my location","my current location","exact current location"],query):
                url = "https://www.google.com/maps/search/Where+am+I+?/"
                webbrowser.get().open(url)
                SR.speak("Showing your current location on google maps...")
                break
            elif there_exists(["where am i"],query):
                Ip_info = requests.get('https://api.ipdata.co?api-key=test').json()
                loc = Ip_info['region']
                SR.speak(f"You must be somewhere in {loc}")

            #who is searcing mode
            elif there_exists(['who is','who the heck is','who the hell is','who is this'],query):
                query=query.replace("wikipedia","")
                results=wikipedia.summary(query,sentences=1)
                SR.speak("According to wikipdedia:  ")
                SR.speak(results)

            #play music
           

            # top 5 news
            elif there_exists(['top 5 news','top five news','listen some news','news of today','tell me top 5 news', 'tell me top five news', "today's top 5 news","today's top five news"],query):
                news=Annex.News(scrollable_text)
                news.show()

            #whatsapp message
            elif there_exists(['open whatsapp messeaging','send a whatsapp message','send whatsapp message','please send a whatsapp message','open whatsapp and send a message','can you open whatsapp and send a message','can you please open whatsapp and send a message' ],query):
                whatsapp=Annex.WhatsApp(scrollable_text)
                whatsapp.send()
                del whatsapp
            #what is meant by
            elif there_exists(['what is meant by','what is mean by','what is the meaning of '],query):
                results=wikipedia.summary(query,sentences=2)
                SR.speak("According to wikipedia:\n")
                SR.speak(results)

            #taking photo
            elif there_exists(['take a photo','take a selfie','take my photo','take photo','take selfie','one photo please','click a photo','click my photo','click one photo please','please click a photo','please can you click a photo','click a picture','click a picture of me',' take a picture','please take a picture'],query):
                takephoto=Annex.camera()
                Location=takephoto.takePhoto()
                os.startfile(Location)
                del takephoto
                SR.speak("Captured picture is stored in Camera folder.")

            #bluetooth file sharing
            elif there_exists(['send some files through bluetooth','send file through bluetooth','bluetooth sharing','bluetooth file sharing','open bluetooth','i want to send some files through bluetooth','can you open bluetooth','please open bluetooth file transfer','please open bluetooth file transfer for me'],query):
                SR.speak("Opening bluetooth...")
                os.startfile(r"C:\Windows\System32\fsquirt.exe")
                break

            #opening different websites 
            elif there_exists(["translate",'open translator for me ', ' please open translator for me', 'can please open translator for me','can you translate this for me','please translate this for me'],query):
                SR.speak("Opening Translator")
                SR.speak("enter the statement which you want to translate and then select the language in which you want it to get translated")
                webbrowser.open("https://translate.google.co.in")

            elif there_exists (["dictionary",'open dictionary','please open dictionary','open dictionary for me ','please open dictionary for me','can you open dictionary','can you please open dictionary', 'please can you open dictionary', 'can you please open dictionary for me','please can you open dictionary for me'],query):
                SR.speak("Opening Dictionary")
                webbrowser.open("https://www.dictionary.com")
                SR.speak("Enter the word in the search bar of the dictionary, whose definition or synonyms you want to know")

            elif there_exists(["google game"],query):
                webbrowser.open("https://chromedino.com/")
                SR.speak("click upper arrow key to start the game")

            elif there_exists(["instagram",'open instagram','please open instagram','open instagram for me ','please open instagram for me','can you open instagram','can you please open instagram', 'please can you open instagram', 'can you please open instagram for me','please can you open instagram for me'],query):
                SR.speak("Opening Instagram")
                webbrowser.open("instagram.com")

            elif there_exists(['stack overflow','open stackoverflow','please open stackoverflow','open stackoverflow for me ','please open stackoverflow for me','can you open stackoverflow','can you please open stackoverflow', 'please can you open stackoverflow', 'can you please open stackoverflow for me','please can you open stackoverflow for me'],query):
                SR.speak("Opening Stack Overflow")
                webbrowser.open("stackoverflow.com")

            elif there_exists(["w3schools",'open w3schools','please open w3schools','open w3schools for me ','please open w3schools for me','can you open w3schools','can you please open w3schools', 'please can you open w3schools', 'can you please open w3schools for me','please can you open w3schools for me'],query):
                SR.speak("Opening W3Schools")
                webbrowser.open("w3schools.com")

            elif there_exists(['mks college','open mks college','please open mks college','open mks college for me ','please open mks college for me','can you open mks college','can you please open mks college', 'please can you open mks college', 'can you please open mks college for me','please can you open mks college for me'],query):
                SR.speak("Opening MKS College Website")
                webbrowser.open("mkscollege.edu.in")

            elif there_exists(['amazon','open amazon','please open amazon','open amazon for me ','please open amazon for me','can you open amazon','can you please open amazon', 'please can you open amazon', 'can you please open amazon for me','please can you open amazon for me'],query):
                SR.speak("Opening Amazon")
                webbrowser.open("amazon.in")

            
            elif there_exists(['flipkart','open flipkart','please open flipkart','open flipkart for me ','please open flipkart for me','can you open flipkart','can you please open flipkart', 'please can you open flipkart', 'can you please open flipkart for me','please can you open flipkart for me'],query):
                SR.speak("Opening flipkart")
                webbrowser.open("flipkart.com")

            
            elif there_exists(['myntra','open myntra','please open myntra','open myntra for me ','please open myntra for me','can you open myntra','can you please open myntra', 'please can you open myntra', 'can you please open myntra for me','please can you open myntra for me'],query):
                SR.speak("Opening myntra")
                webbrowser.open("myntra.com")

            
            elif there_exists(['netflix','open netflix','please open netflix','open netflix for me ','please open netflix for me','can you open netflix','can you please open netflix', 'please can you open netflix', 'can you please open netflix for me','please can you open netflix for me'],query):
                SR.speak("Opening netflix")
                webbrowser.open("https://www.netflix.com/in/")

            elif there_exists(['amazon prime video','open amazon prime video','please open amazon prime video','open amazon prime video for me ','please open amazon prime video for me','can you open amazon prime video','can you please open amazon prime video', 'please can you open amazon prime video', 'can you please open amazon prime video for me','please can you open amazon prime video for me'],query):
                SR.speak("Opening Amazon Prime Video")
                webbrowser.open("https://www.primevideo.com/")
            
            elif there_exists(['hotstar','open hotstar','please open hotstar','open hotstar for me ','please open hotstar for me','can you open hotstar','can you please open hotstar', 'please can you open hotstar', 'can you please open hotstar for me','please can you open hotstar for me'],query):
                SR.speak("Opening Hotstar")
                webbrowser.open("https://www.hotstar.com/in")

            #play game
            elif there_exists(['would like to play some games','play some games','would like to play some game','want to play some games','want to play game','want to play games','play games','open games','play game','open game','i want to play some games','i want to play games'],query):
                SR.speak("We have 2 games right now.\n")
                SR.updating_ST_No_newline('1.')
                SR.speak("Stone Paper Scissor")
                SR.updating_ST_No_newline('2.')
                SR.speak("Flappy Bird")
                SR.speak("\nTell us your choice:")
                while(True):
                    query=SR.takeCommand().lower()
                    if ('stone' in query) or ('paper' in query):
                        SR.speak("Opening stone paper scissor...")
                        sps=Annex.StonePaperScissor()
                        sps.start(scrollable_text)
                        break
                    elif ('flappy bird' in query):
                        SR.speak("Opening flappy bird...")
                        flappybird()
                        
                        break
                    else:
                        SR.speak("It did not match the option that we have. \nPlease say it again.")

            #makig note
            elif there_exists(['make a note','take note','take a note','note it down','make note','remember this as note','open notepad and write','remeber this'],query):
                SR.speak("What would you like to write down?")
                data=SR.takeCommand()
                n=Annex.note()
                n.Note(data)
                SR.speak("I have a made a note of that.")
                break

            #flipping coin
            elif there_exists(["toss a coin","flip a coin","toss",'can you flip a coin','can you flip a coin for me','can you toss a coin','can you toss a coin for me'],query):
                moves=["head", "tails"]
                cmove=random.choice(moves)
                playsound.playsound('quarter spin flac.mp3')
                SR.speak("It's " + cmove)

            #time and date
            elif there_exists(['the time','what is the current time','what is the time','what time is it ','what time it is','whats the time now','current time'],query):
                strTime =datetime.datetime.now().strftime("%H:%M:%S")
                SR.speak(f"Sir, the time is {strTime}")
            elif there_exists(['the date','todays date','what is the current date','what is the date today','what date is today','what is todays date'],query):
                strDay=datetime.date.today().strftime("%B %d, %Y")
                SR.speak(f"Today is {strDay}")
            elif there_exists(['what day it is','what day is today','which day is today',"today's day name please"],query):
                SR.speak(f"Today is {datetime.datetime.now().strftime('%A')}")

            #opening software applications
            elif there_exists(['open chrome','open chrome','please open chrome','open chrome for me ','please open chrome for me','can you open chrome','can you please open chrome', 'please can you open chrome', 'can you please open chrome for me','please can you open chrome for me'],query):
                SR.speak("Opening chrome")
                os.startfile(r'"C:\Program Files\Google\Chrome\Application\chrome.exe"')
                break
           
            elif there_exists(['open notepad','start notepad','open notepad','please open notepad','open notepad for me ','please open notepad for me','can you open notepad','can you please open notepad', 'please can you open notepad', 'can you please open notepad for me','please can you open notepad for me'],query):
                SR.speak('Opening notepad')
                os.startfile(r'C:\Windows\notepad.exe')
                break

           

            elif there_exists(['powershell','open powershell','open powershell','please open powershell','open powershell for me ','please open powershell for me','can you open powershell','can you please open powershell', 'please can you open powershell', 'can you please open powershell for me','please can you open powershell for me'],query):
                SR.speak("Opening powershell")
                os.startfile(r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe')
                break
            elif there_exists(['cmd','command prompt','command prom','commandpromt','open command prompt','please open command prompt','open command prompt for me ','please open command prompt for me','can you open command prompt','can you please open command prompt', 'please can you open command prompt', 'can you please open command prompt for me','please can you open command prompt for me'],query):
                SR.speak("Opening command prompt")
                os.startfile(r'C:\Windows\System32\cmd.exe')
                break
           
            elif there_exists(['open settings','open control panel','open this computer setting Window','open computer setting Window'   ,'open computer settings','open setting','show me settings','open my computer settings'],query):
                SR.speak("Opening settings...")
                os.startfile(r'C:\Users\Admin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\System Tools')
                break
            elif there_exists(['open your setting','open your settings','open settiing window','show me setting window','open voice assistant settings'],query):
                SR.speak("Opening my Setting window..")
                sett_wind=Annex.SettingWindow()
                sett_wind.settingWindow(root)
                break
           

            elif there_exists(['open word','please open word','open word for me ','please open word for me','can you open word','can you please open word', 'please can you open word', 'can you please open word for me','please can you open word for me'],query):
                SR.speak("Opening Microsoft Word")
                os.startfile(r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE")
                break

            elif there_exists(['open excel','please open excel','open excel for me ','please open excel for me','can you open excel','can you please open excel', 'please can you open excel', 'can you please open excel for me','please can you open excel for me'],query):
                SR.speak("Opening Microsoft Excel")
                os.startfile(r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE")
                break

            elif there_exists(['open microsoft edge','please open microsoft edge','open microsoft edge for me ','please open microsoft edge for me','can you open microsoft edge','can you please open microsoft edge', 'please can you open microsoft edge', 'can you please open microsoft edge for me','please can you open microsoft edge for me'],query):
                SR.speak("Opening Microsoft Edge")
                os.startfile(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
                break

            elif there_exists(['open telegram','please open telegram','open telegram for me ','please open telegram for me','can you open telegram','can you please open telegram', 'please can you open telegram', 'can you please open telegram for me','please can you open telegram for me'],query):
                SR.speak("Opening Telegram")
                os.startfile(r"C:\Users\Admin\AppData\Roaming\Telegram Desktop\Telegram.exe")
                break

            elif there_exists(['open code','open visual studio ','open vs code''start visual studio','open visual studio','please open visual studio','open visual studio for me ','please open visual studio for me','can you open visual studio','can you please open visual studio', 'please can you open visual studio', 'can you please open visual studio for me','please can you open visual studio for me','open vs code','start vs code','open vs code','please open vs code','open vs code for me ','please open vs code for me','can you open vs code','can you please open vs code', 'please can you open vs code', 'can you please open vs code for me','please can you open vs code for me'],query):
                SR.speak("Opening Visual Code")
                os.startfile(r"C:\Users\Admin\AppData\Local\Programs\Microsoft VS Code\Code.exe")
                break

            elif there_exists(["open powerpoint",'please open powerpoint','open powerpoint for me ','please open powerpoint for me','can you open powerpoint','can you please open powerpoint', 'please can you open powerpoint', 'can you please open powerpoint for me','please can you open powerpoint for me'],query):
                SR.speak("Opening Microsoft Power Point")
                os.startfile(r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE")
                break

            elif there_exists(["open outlook",'please open outlook','open outlook for me ','please open outlook for me','can you open outlook','can you please open outlook', 'please can you open outlook', 'can you please open outlook for me','please can you open outlook for me'],query):
                SR.speak("Opening Microsoft Outlook")
                os.startfile(r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE")
                break 

            elif there_exists(["open onenote",'please open onenote','open onenote for me ','please open onenote for me','can you open onenote','can you please open onenote', 'please can you open onenote', 'can you please open onenote for me','please can you open onenote for me'],query):
                SR.speak("Opening Microsoft One Note")
                os.startfile(r"C:\Program Files\Microsoft Office\root\Office16\ONENOTE.EXE")
                break

            elif there_exists(['open spotify','please open spotify','open spotify for me ','please open spotify for me','can you open spotify','can you please open spotify', 'please can you open spotify', 'can you please open spotify for me','please can you open spotify for me'],query):
                SR.speak("Opening Spotify")
                os.startfile(r"C:\Users\Admin\AppData\Roaming\Spotify\Spotify.exe" )
                break 

            elif there_exists(['open android studio','please open android studio','open android studio for me ','please open android studio for me','can you open android studio','can you please open android studio', 'please can you open android studio', 'can you please open android studio for me','please can you open android studio for me'],query):
                SR.speak("Opening Android Studio")
                os.startfile(r"C:\Program Files\Android\Android Studio\bin\studio64.exe")
                break

            elif there_exists(['open whatsapp'],query):
                SR.speak("Opening WhatsApp")
                os.startfile(r"C:\Users\Admin\AppData\Local\WhatsApp\WhatsApp.exe")
                break

            elif there_exists(['open gis','please open gis','open gis for me ','please open gis for me','can you open gis','can you please open gis', 'please can you open gis', 'can you please open gis for me','please can you open gis for me'],query):
                SR.speak("opening GIS")
                os.startfile(r"C:\Users\Admin\Desktop\Excel\gis")
                break

        

            #password generator
            elif there_exists(['suggest me a password','password suggestion','i want a password','give me a password','generate a password for me','generate a password','suggest a password','generate a password to me'],query):
                m3=Annex.PasswordGenerator()
                m3.givePSWD(scrollable_text)
                del m3
            #screeshot
            elif there_exists(['take screenshot','take a screenshot','screenshot please','capture my screen'],query):
                SR.speak("Taking screenshot")
                SS=Annex.screenshot()
                SS.takeSS()
                SR.speak('Captured screenshot is saved in Screenshots folder.')
                del SS

            #voice recorder
            elif there_exists(['record my voice','start voice recorder','voice recorder'],query):
                VR=Annex.VoiceRecorer()
                VR.Record(scrollable_text)
                del VR

            #text to speech conversion
            elif there_exists(['text to speech','convert my notes to voice','open text to speech mode','text to speech mode'],query):
                SR.speak("Opening Text to Speech mode")
                TS=Annex.TextSpeech()
                del TS

            #Empty recycling bin
            elif there_exists(["remove the recycle bin",'empty my bin','mt my bin','mt my recycling bin','empty my recycling bin','mt my recycle bin','empty my recycle bin'],query):
                winshell.recycle_bin().empty(
                    confirm = True, show_progress = False, sound = True
                )
                SR.speak("Recycle bin emptied")

            #weather report
            elif there_exists(['weather report','temperature','show weather report','show temperature'],query):
                Weather=Annex.Weather()
                Weather.show(scrollable_text)

            #shutting down system
            elif there_exists(['exit','quit','goodbye'],query):
                SR.speak("shutting down")
                exit()
            
            elif there_exists(["shutdown"],query):
                SR.speak("Hold on a Sec! Your system is on its way to shut down")
                subprocess.call('shutdown /p /f')
            
            elif there_exists(['restart'],query):
                SR.speak("Restarting your system")
                subprocess.call(["shutdown","/r"])

            elif there_exists(["sleep"],query):
                SR.speak("Setting in sleep mode")
                subprocess.call("shutdown /h")

            elif there_exists(['none'],query):
                pass
            elif there_exists(['stop the flow','stop the execution','halt','halt the process','stop the process','stop listening','stop the listening'],query):
                SR.speak("Listening halted.")
                break

            #it will give online results for the query
            elif there_exists(['search something for me','to do a little search','search mode','i want to search something'],query):
                SR.speak('What you want me to search for?')
                query=SR.takeCommand()
                SR.speak(f"Showing results for {query}")
                try:
                    res=app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    print("Sorry, but there is a little problem while fetching the result.")

            #Change its voice
            
                
                
            #what is the capital
            elif there_exists(['what is the capital of','capital of','capital city of'],query):
                try:
                    res=app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    print("Sorry, but there is a little problem while fetching the result.")

           

            elif there_exists(['temperature'],query):
                try:
                    res=app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    print("Internet Connection Error")
            elif there_exists(['+','-','*','x','/','plus','add','minus','subtract','divide','multiply','divided','multiplied','what is'],query):
                try:
                    res=app.query(query)
                    SR.speak(next(res.results).text)
                except:
                    print("Internet Connection Error")

            else:
                SR.speak("Sorry it did not match with any commands that i'm registered with. Please say it again.")
    except Exception as e:
        pass
keyboard.add_hotkey("`", mainframe)
def gen(n):
    for i in range(n):
        yield i

class MainframeThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        mainframe()

def Launching_thread():
    Thread_ID=gen(1000)
    global MainframeThread_object
    MainframeThread_object=MainframeThread(Thread_ID.__next__(),"Mainframe")
    MainframeThread_object.start()

if __name__=="__main__":
        #tkinter code
        root=themed_tk.ThemedTk()
        root.set_theme("winnative")
        root.geometry("{}x{}+{}+{}".format(745,360,int(root.winfo_screenwidth()/2 - 745/2),int(root.winfo_screenheight()/2 - 360/2)))
        root.resizable(0,0)
        root.title("AIDA")
        root.iconbitmap('aida.ico')
        root.configure(bg='#2c4557')
        scrollable_text=scrolledtext.ScrolledText(root,state='disabled',height=15,width=87,relief='sunken',bd=5,wrap=tk.WORD,bg='#add8e6',fg='#800000')
        scrollable_text.place(x=10,y=10)
        mic_img=Image.open("mic.png")
        mic_img=mic_img.resize((55,55),Image.ANTIALIAS)
        mic_img=ImageTk.PhotoImage(mic_img)

        """Setting up objects"""
        SR=Annex.SpeakRecog(scrollable_text)    #Speak and Recognition class instance
        Listen_Button=tk.Button(root,image=mic_img,borderwidth=0,activebackground='#2c4557',bg='#2c4557',command=Launching_thread)
        Listen_Button.place(x=330,y=280)
        myMenu=tk.Menu(root)
        m1=tk.Menu(myMenu,tearoff=0) #tearoff=0 means the submenu can't be teared of from the window
        m1.add_command(label='Commands List',command=CommandsList)
        myMenu.add_cascade(label="Help",menu=m1)
        stng_win=Annex.SettingWindow()
        myMenu.add_cascade(label="Settings",command=partial(stng_win.settingWindow,root))
        myMenu.add_cascade(label="Clear Screen",command=clearScreen)
        root.config(menu=myMenu)
        root.mainloop()