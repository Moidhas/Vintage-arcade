from tkinter import *
from math import *
from random import * 
root = Tk()
screen = Canvas( root, width=800, height=800, background = "black" )
screen.pack()

from time import*

def setInitialValues():
    global score, xSpeed, ySpeed, alive, xMouse, yMouse, textbookImgFile, numBook, xPlay, yPlay, speed, player, bullets, xBullets, yBullets, bSpeed,xText,yText 
    global mouseClick, startTime, clock, information, timeInfo 

    #Time and Statistics 
    score = 0
    startTime = time()
    clock = 15
    information = 0
    timeInfo = 0

    #Player
    xSpeed = 0
    ySpeed = 0
    xPlay = 400
    yPlay = 400
    player = 0

    #Bullets
    bullets = []
    xBullets = []
    yBullets = []
    bSpeed = 8 

    speed = 5

    #Aiming
    xMouse = 400
    yMouse = 400
    mouseClick = False

    #Textbook
    textbookImgFile = PhotoImage(file = "Textbook.png")
    numBook = 7
    xText = []
    yText = []
    alive = []

def textBookDraw():
    global xText,yText,textImg
    for i in range (numBook):
        if alive [i] == True:
            textImg [i] = screen.create_image(xText[i],yText[i], image = textbookImgFile)

def playerDraw():
    global player, xPlay, yPlay

    player = screen.create_polygon(xPlay - 15, yPlay + 30, xPlay, yPlay, xPlay + 15, yPlay + 30, fill= "yellow")

def createBB():
    global xBullets, yBullets, bullets
    xBullets.append(xPlay)
    yBullets.append(yPlay)
    bullets.append("")

def createRanText():
    global xText, yText, alive, textImg, xtextSpeed, ytextSpeed

    textImg = []
    xtextSpeed = []
    ytextSpeed = []

    for i in range (numBook):
        xText.append(randint(1,800))
        yText.append(randint(1,800))
        textImg.append(0)
        xtextSpeed.append(uniform(-5,5))
        ytextSpeed.append(uniform(-5,5))
        alive.append (True)
           

def drawBB ():
    for i in range (len(yBullets)):
       bullets[i] = screen.create_line(xBullets[i], yBullets[i], xBullets[i], yBullets[i] - 10, fill = "white", width = 3)

def deleteBB():
    for i in range (len(yBullets)):
        screen.delete(bullets[i])

def deleteText ():
    global textImg
    for i in range (numBook):
        screen.delete(textImg[i])
        

def updatePlayer():
    global xPlay, yPlay
    xPlay = xPlay + xSpeed
    yPlay = yPlay + ySpeed

    if xPlay - 15 <= 0:
        xPlay = 15
        if yPlay <= 0:
            yPlay = 0

        elif yPlay + 30 >= 800:
            yPlay = 770

    elif xPlay + 15 >= 800:
        xPlay = 785
        if yPlay <= 0:
            yPlay = 0

        elif yPlay + 30 >= 800:
            yPlay = 770

    elif yPlay <= 0:
        yPlay = 0

    elif yPlay + 30 >= 800:
        yPlay = 770

def updateBB():
    global bullets, xBullets, yBullets
    
    for i in range (len(yBullets)):
        yBullets [i] = yBullets [i] - bSpeed

    f = 0
    while f < len(yBullets) - 1:
        if yBullets[f] < 0:
            yBullets.pop(f)
            xBullets.pop(f)
            bullets.pop(f)

        else:
            f = f + 1
 

def updateText ():
    global xtextSpeed, ytextSpeed ,xText, yText 
    for i in range (numBook):
        if alive [i] == True:
        
            if xText [i] <= 0 or xText[i] >= 800:
                xtextSpeed [i] = xtextSpeed [i] * - 1
            
            elif yText [i] <= 0 or yText[i] >= 800:
                ytextSpeed [i] = ytextSpeed [i] * - 1
        
            yText [i] = yText [i] + ytextSpeed [i]
            xText [i] = xText [i] + xtextSpeed [i]


def deadText ():
    global alive, mouseClick, xText, yText, score 

    for i in range (numBook):
        if alive[i] == True:
            if mouseClick == True:
                if xText[i] - 20 < xBullets[i%len(xBullets)] < xText [i] + 20 and yText [i] - 30 < yBullets[i%len(yBullets)] - 10 < yText [i] + 30 :
                    alive [i] = False
                    score = score + 1 

def newTimer ():
    global startTime, clock
    lastTime = time () - startTime
    if lastTime >= 1:
        clock = clock -1
        startTime = time()

def info ():
    global information, timeInfo 
    information = screen.create_text(50,30, text = "Score: " +  str(score) + "/"+ str(numBook), fill = "white" ,font = "Arial 15")
    timeInfo = screen.create_text(40, 60, text = "Time: " + str(clock), fill = "white", font = "Arial 15")
        

def keyDownHandler(event):
    global xSpeed, ySpeed, speed, Qpress

    if event.keysym == "w" or event.keysym == "Up":
        ySpeed = -speed

    elif event.keysym == "a" or event.keysym == "Left":
        xSpeed = -speed

    elif event.keysym == "d" or event.keysym == "Right":
        xSpeed = speed

    elif event.keysym == "s" or event.keysym == "Down":
        ySpeed = speed
        
    else:
        print("Nothing")
   

def keyUpHandler(event):
    global xSpeed, ySpeed

    xSpeed = 0
    ySpeed = 0

    
def mouseClickHandler (event):
    global mouseClick
    createBB()
    mouseClick = True


def runGame():
    setInitialValues()
    createRanText()

    while clock > 0 and score < numBook:
        
        deadText()
        
        updatePlayer()
        updateBB()
        updateText()
        newTimer()

        info()
        playerDraw()
        textBookDraw()
        drawBB()
        
        screen.update()
        sleep(0.01)
        screen.delete(player, information, timeInfo)
        deleteBB()
        deleteText()

    if score == numBook:
        screen.create_text(400,400, text = "You Won the Game", fill = "white" ,font = "Arial 50")

    else:
        screen.create_text(400,400, text = "You Lost", fill = "white" ,font = "Arial 50")

        


root.after( 0, runGame )

screen.bind("<Button-1>", mouseClickHandler) 
screen.bind("<Key>", keyDownHandler)
screen.bind("<KeyRelease>", keyUpHandler)

screen.pack()
screen.focus_set()
root.mainloop()
