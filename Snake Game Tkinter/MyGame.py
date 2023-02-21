# Screen Resolution: 1366x768 .

# Snake Game #

# Importing section
from tkinter import *
import random
import time
import tkinter.messagebox
import csv
import pickle
import os

# When the player losses, this function will append his name and score to
# a file.


def GameOver():
    global gameOver, FirstAttempt, data, score

    # Since My sorting Fumction doesnt work unless there are 3 names already
    # in the file,so we need to add 3 empty scores with Empty Names .
    EList = ["Empty", "Empty", "Empty"]
    CheckFile = os.path.isfile("Recorder.txt")
    if CheckFile is False:
        for i in range(3):
            with open("Recorder.txt", "a+") as file1:
                file1.seek(0)
                data1 = file1.read(100)
                if len(data1) > 0:
                    file1.write("\n")
                file1.write(EList[i] + ', ' + '')
                file1.write("0")

    # Appending the player name.
    with open("Recorder.txt", "a+") as file1:
        file1.seek(0)
        data1 = file1.read(100)
        if len(data1) > 0:
            file1.write("\n")
        file1.write(data + ', ' + '')
    gameOver = True

    # MessageBox appears
    canvas.create_text(
        width / 2,
        height / 2,
        fill="white",
        font="Times 40 italic bold",
        text="GAME OVER!",
        underline=1)
    GOChoice = tkinter.messagebox.askquestion(
        "Question 1",
        "          GAME OVER!\n" +
        "Good Job " +
        data +
        ", \nYou Scored: " +
        str(score) +
        "\nWould you like to play again?")

    # If the player wants to play again
    if GOChoice == 'yes':
        a = open("Recorder.txt", "a")
        a.write(str(score))
        a.close()
        Restart()

    #  If not,he will be returned to main menu .
    if GOChoice == "no":
        a = open("Recorder.txt", "a")
        a.write(str(score))
        a.close()
        window.destroy()
        root.deiconify()
        FirstAttempt = False

    # After each completed game, Sort the the leaderboard file.
    leaderboardsorted()


def SaveGame():
    global snake, positions, direction, foodX, foodY, score, currentlevel
    global sHeadPos, window, canvas, PlayerName, CoordsList
    # Crate an empty list with number of elements equal to the number of body
    # parts of the snake.
    CoordsList = [] * (len(snake) - 1)

    # If the game is running, pause it
    if GameResumed:
        GamePause()

    # Save the coordinates for each square of the snake into a list.
    for i in range(len(snake) - 1):
        x = canvas.coords(snake[i])
        CoordsList.append(x)
    # Save each necessary variable into a file using "pickle" .
    pickle.dump(CoordsList, open("SnakeCoordsMemory.dat", "wb"))
    pickle.dump(PlayerName, open("NameMemory.dat", "wb"))
    pickle.dump(positions, open("posMemory.dat", "wb"))
    pickle.dump(direction, open("dirMemory.dat", "wb"))
    pickle.dump(score, open("ScoreMemory.dat", "wb"))
    pickle.dump(currentlevel, open("lvlMemory.dat", "wb"))
    pickle.dump(sHeadPos, open("HeadposMemory.dat", "wb"))
    pickle.dump(foodX, open("FoodXMemory.dat", "wb"))
    pickle.dump(foodY, open("FoodYMemory.dat", "wb"))


def LoadGame():
    global LoadSnakeCoords, LoadfoodX, LoadfoodY, Loadpositions
    global Loaddirection, Loadscore, GameLoaded, LoadsHeadPos
    global Loadcurrentlevel, txt, window, canvas, LoadPlayerName

    # Cheack if there is a previous game saved.
    CheckFile = os.path.isfile("FoodYMemory.dat")
    if CheckFile:
        # First close the current game.
        window.destroy()

        # Our Magnificent variable that we will use to load our game in many
        # places through the code.
        GameLoaded = True

        # Load each file that was saved last time into a new variable.
        LoadSnakeCoords = pickle.load(open("SnakeCoordsMemory.dat", "rb"))
        LoadPlayerName = pickle.load(open("NameMemory.dat", "rb"))
        Loadpositions = pickle.load(open("posMemory.dat", "rb"))
        Loaddirection = pickle.load(open("dirMemory.dat", "rb"))
        Loadscore = pickle.load(open("ScoreMemory.dat", "rb"))
        Loadcurrentlevel = pickle.load(open("lvlMemory.dat", "rb"))
        LoadsHeadPos = pickle.load(open("HeadposMemory.dat", "rb"))
        LoadfoodX = pickle.load(open("FoodXMemory.dat", "rb"))
        LoadfoodY = pickle.load(open("FoodYMemory.dat", "rb"))

        # Run a typical new game, But the difference this time is
        # that GameLoaded have been set to the Value "True" .
        MainFunc()

    else:
        pass


# Our Simple Cheat Code will increase the score by 10 Whenever "9" is pressed.
def CheatCode(event):
    global score, txt, Cheated
    score += 10
    txt = "Score:" + str(score)
    ScoreVar.set(txt)

    # To prevent Saving game when cheated later.
    Cheated = True


def leaderboard():
    global LBwindow, LBcanvas, frame2, users, button13, currentwindow
    global file, NameEntry, score, TxtCL

    # If No Game is running.
    if GameResumed:

        # doing usual window adjustments.
        LBwindow = Toplevel()
        LBwindow.geometry("750x550")
        LBwindow.title("Leaderboard")
        LBwindow.config(bg="darkslategrey")
        LBwindow.resizable(False, False)
        LBcanvas = Canvas(LBwindow, width=750, height=550, bg="darkslategrey")
        LBcanvas.place(x=0, y=0)

        # Open The Sorted File that contains names,scores.
        fileM = open('SortedLeaderBoard.txt')

        # Extract The Top 3 players from the sorted file.
        Txt1 = fileM.readline()
        TxtCL = fileM.readline()
        Txt1 = "1. " + Txt1 + "\n" + "2. " + str(TxtCL)
        TxtCL = fileM.readline()
        Txt1 = Txt1 + "\n" + "3. " + str(TxtCL)

        #  Creating texts and images for the LeaderBoard Page.
        TitleLabel = Label(
            LBcanvas,
            text='LEADERBAORD',
            fg='khaki',
            highlightbackground='darkslategrey',
            font="Arcade 35 bold",
            bg='darkslategrey')
        TitleLabel.place(x=180, y=10)
        button13 = Button(
            LBcanvas,
            text='MAIN MENU',
            relief=FLAT,
            height=2,
            width=10,
            highlightbackground='black',
            command=lambda: LBwindow.destroy())
        button13.place(x=300, y=480)
        Top3Image = PhotoImage(file="top3.png")
        LBcanvas.create_image(100, 80, image=Top3Image)
        Image123 = PhotoImage(file="cup.png")
        LBcanvas.create_image(622, 440, image=Image123)
        LBcanvas.create_text(
            390,
            275,
            text=Txt1,
            font="Times 30 bold",
            fill="white")
        LBwindow.mainloop()

    else:  # IF there is a game running and it is paused.
        tkinter.messagebox.showinfo(
            "Sorry", "You Can't access Leaderboard\n while a game is running")


# Sort The Recorder file from higher to lower.
def leaderboardsorted():
    global file, file2, NameEntry, score, data, data2, slist, r_csv
    file = open("Recorder.txt")

    # Using "csv" along with "sorted()" to create a list, each element of the
    # list contain [name,score], where the elements are sorted From the
    # highest score to the lowest.
    r_csv = csv.reader(file)
    slist = sorted(r_csv, key=lambda row: int(row[1]), reverse=True)
    file.close()

    # Now We will write a new file with each element of the slist as a line in
    # the format (name's Score: score).
    file2 = open("SortedLeaderBoard.txt", "w")
    Positioncounter = 0
    for i in range(len(slist)):
        firstline = slist[i][0] + "'s Score: " + slist[i][1]
        file2.seek(Positioncounter)
        currentlineLength = len(firstline)
        Positioncounter = Positioncounter + currentlineLength + 1
        file2.write(str(firstline))
        if i < len(slist) - 1:
            file2.write("\n")


# Simple function to check weather the user entered a text or not.
def checkname():
    global NameEntry, errortext, Nameframe, PlayerName
    if len(NameEntry.get()) == 0:
        errortext = Label(
            Nameframe,
            fg="red",
            bg="grey",
            font="Arcade 10 bold",
            text="You Must Enter Something!!")
        errortext.place(x=20, y=85)
        Namecanvas.update()
        time.sleep(3)
        errortext.place_forget()

    else:
        PlayerName = NameEntry.get()
        LaunchGame()


def NameFunc():
    global NameEntry, Namewindow, Namecanvas, Nameframe
    # Usual window adjusting.
    Namewindow = Toplevel()
    Namewindow.geometry("704x320")
    Namewindow.resizable(False, False)
    Namewindow.title("Player's Name")
    Namewindow.config(bg='lightslategrey')

    #  A canvas to contain the background image.
    Namecanvas = Canvas(Namewindow, width=704, height=320, bg="black")
    Namecanvas.create_image(
        352,
        160,
        anchor=CENTER,
        image=grass,
        tag='texture')
    Namecanvas.place(x=0, y=0)

    # Labels for the page and an entry with a button for the name entering.
    Nameframe = LabelFrame(
        Namecanvas,
        text="Enter Your Name: ",
        padx=20,
        pady=30,
        font='Arcade 20 bold',
        bg='grey',
        bd=4,
        fg='black')
    Nameframe.place(x=220, y=0)
    NameEntry = Entry(Nameframe)
    NameEntry.pack(padx=20, pady=30)
    Namebutton = Button(
        Nameframe,
        text='Launch Game',
        relief=FLAT,
        height=2,
        width=20,
        highlightbackground='black',
        command=checkname)
    Namebutton.pack(padx=30, pady=20)
    root.withdraw()

    Namewindow.mainloop()


def LaunchGame():
    global score, data

    # Save the name to a variable, we will need it later.
    data = NameEntry.get()

    # close the name window and start a new game.
    Namewindow.destroy()
    Startnewgame()


#  A Function to dssplay the boss key page, nothing unclear here.
def BossKeyFunc():
    global GameResumed

    Bosskey = Toplevel()
    Bosskey.title("Portfolio Analysis-Excel")
    Bosscanvas = Canvas(Bosskey, width=1920, height=1080)
    Bosscanvas.pack()
    bosskeyimage = PhotoImage(file='BossKey.png')
    Bosscanvas.create_image(960, 540, image=bosskeyimage, )
    if GameResumed:
        GamePause()

    else:
        window.after(90, moveSnake)

    Bosskey.mainloop()


def Startnewgame():
    global FirstAttempt

    # If its not the first time to start a game, then probably a previous game
    # window is withdrawn, so destroy it.
    if FirstAttempt is False:
        window.destroy()
        MainFunc()
    else:

        # if its the first time then just run the game.
        MainFunc()


# Our Main Function thats run the snake game.
def MainFunc():
    global pause, Cheated, GameSpeed, OneTimer, OneTimer2, gameOver, score
    global Loaddirection, snakeSize, PauseImage, direction, LoadsHeadPos
    global LoadSnakeCoords, Loadscore, GameLoaded, Continue, GameResumed
    global width, height, window, canvas, PauseButtonLabel, snake, txt
    global currentlevel, LevelString, Levelvar, ScoreVar, Loadcurrentlevel

    # Creating Very Important variables to help me implement the code
    # perfectly.
    GameResumed = True
    gameOver = False
    OneTimer = False
    OneTimer2 = False
    GameSpeed = 140
    Cheated = False

    # Hide the main menu page, So the user sees only one window while playing.
    root.withdraw()

    # Creating the canvas which the snake will be moving at.
    width = 704
    height = 320
    window = setWindowDimensions()
    canvas = Canvas(window, bg="Dark green", width=width, height=height)
    canvas.create_image(352, 160, image=grass)

    # Creating a string variable to change the text of the pause button.
    Continue = "Continue"
    pause = "Pause"
    PauseButtonLabel = StringVar()
    PauseButtonLabel.set(pause)

    # Creating The Head of the sneak
    snake = []
    snakeSize = 15
    snake.append(
        canvas.create_rectangle(
            snakeSize,
            snakeSize,
            snakeSize * 2,
            snakeSize * 2,
            fill="saddle brown",
            outline="goldenrod"))

    # When Game is loaded, load the coordinates of the sneak's head.
    if GameLoaded:
        canvas.coords(
            snake[0],
            LoadsHeadPos[0],
            LoadsHeadPos[1],
            LoadsHeadPos[2],
            LoadsHeadPos[3])

    # Load score.
    if GameLoaded:
        score = Loadscore
    else:
        score = 0

    # Create the body of the snake depending on the saved score, not a perfect
    # way if the user used the cheat code, But cheating doesn't count anyways
    # :).
    if GameLoaded:
        growth = int(score / 10)

        for i in range(growth):
            snake.append(
                canvas.create_rectangle(
                    0,
                    0,
                    snakeSize,
                    snakeSize,
                    fill="saddle brown",
                    outline="saddle brown"))
            # Set the locations of the each body part exactly the same as the
            # saved game.
            canvas.coords(snake[i + 1],
                          LoadSnakeCoords[i][0],
                          LoadSnakeCoords[i][1],
                          LoadSnakeCoords[i][2],
                          LoadSnakeCoords[i][3])

    # Load the level
    if GameLoaded:
        currentlevel = Loadcurrentlevel
    else:
        currentlevel = 1

    # Creating strinVars for the score and level labels.
    LevelString = "Level= " + str(currentlevel)
    Levelvar = StringVar()
    Levelvar.set(LevelString)
    txt = "Score:" + str(score)
    ScoreVar = StringVar()
    ScoreVar.set(txt)
    PauseImage = PhotoImage(file="greenpause.png")

    # Binding Section.
    canvas.bind("<Left>", leftKey)
    canvas.bind("<Right>", rightKey)
    canvas.bind("<Up>", upKey)
    canvas.bind("<Down>", downKey)
    canvas.bind("<9>", CheatCode)
    canvas.focus_set()

    # Load at wich direction the snake was moving.
    if GameLoaded:
        direction = Loaddirection
    else:
        direction = "right"

    # Run everything that completes the game window.
    labels()
    CreateMenu()
    placeFood()
    moveSnake()

    window.mainloop()


#  A Menu at the top of the Game window.
def CreateMenu():
    global window

    mainmenu = Menu(window, bg="slategrey", foreground='white')
    window.config(menu=mainmenu)
    subMenu = Menu(
        mainmenu,
        bg="lightslategrey",
        tearoff=0,
        foreground='white')
    FileMenu = Menu(
        mainmenu,
        bg="lightslategrey",
        tearoff=0,
        foreground='white')
    mainmenu.add_cascade(label="Menu", menu=subMenu, font="Times 14 bold ")
    subMenu.add_command(
        label="Back To Main Menu",
        command=ReturnToMainMenu,
        font="Times 14 bold ")
    subMenu.add_command(
        label="Customize Control Buttons",
        command=CustomizeCB,
        font="Times 14 bold ")
    subMenu.add_command(
        label="Restart",
        command=Restart,
        font="Times 14 bold ")
    subMenu.add_command(label="Exit", command=QuitGame, font="Times 14 bold ")
    mainmenu.add_cascade(label="File", menu=FileMenu, font="Times 14 bold ")
    FileMenu.add_command(
        label="Save",
        command=lambda: CheatDetector(),
        font="Times 14 bold ")
    FileMenu.add_command(
        label="Load",
        command=lambda: LoadGame(),
        font="Times 14 bold ")


# If the player used the CheatCode then he cant save.
def CheatDetector():
    global Cheated, GameResumed
    if Cheated:
        tkinter.messagebox.showinfo(
            "Cheating is a Choice... ",
            "Cheaters cant Save!")

    else:
        SaveGame()


# When the user wants to return to the main menu WHILE the game is still
# running.
def ReturnToMainMenu():
    global GameResumed, FirstAttempt, window, Paused
    if GameResumed is True:

        # Pause the game since the user didnt, then hide the game window and
        # display the main menu back again,
        window.withdraw()
        root.deiconify()
        FirstAttempt = False
        GamePause()

    else:
        # Same thing without pausing.
        window.withdraw()
        root.deiconify()
        FirstAttempt = False

# Function for the Control Customization window.


def CustomizeCB():
    global windowCB, LeftButtonEntry, RightButtonEntry
    global UpButtonEntry, DownButtonEntry, TopCB

    # A bit different than usual window adjustments.
    TopCB = Toplevel()
    TopCB.title("Control Customization")
    TopCB.geometry("400x400")
    TopCB.resizable(False, False)

    # A note at the end of the window
    UpdateCompletedLabel = Label(
        TopCB,
        text="*Note: Only Lowercase Alphabets Are Valid.",
        fg="red",
        font="arial 12 italic")
    UpdateCompletedLabel.place(x=50, y=350)

    #  4 Entries for each direction with their labels.

    # Entries
    LeftButtonEntry = Entry(TopCB)
    RightButtonEntry = Entry(TopCB)
    UpButtonEntry = Entry(TopCB)
    DownButtonEntry = Entry(TopCB)

    # Labels
    EntryLabel = Label(
        TopCB,
        text="Enter Your prefered Controls\nfor each direction: ",
        font="Times 16 bold")
    LeftEntryLabel = Label(TopCB, text="Left: ", font="Arial 12")
    RightEntryLabel = Label(TopCB, text="Right: ", font="Arial 12")
    UpEntryLabel = Label(TopCB, text="Up: ", font="Arial 12")
    DownEntryLabel = Label(TopCB, text="Down: ", font="Arial 12")

    # Place them all.
    EntryLabel.place(x=70, y=20)
    LeftEntryLabel.place(x=30, y=100)
    RightEntryLabel.place(x=30, y=150)
    UpEntryLabel.place(x=30, y=200)
    DownEntryLabel.place(x=30, y=250)
    LeftButtonEntry.place(x=100, y=100)
    RightButtonEntry.place(x=100, y=150)
    UpButtonEntry.place(x=100, y=200)
    DownButtonEntry.place(x=100, y=250)

    # A button to Update the new controls.
    UpdateControlsButton = Button(
        TopCB, text="Update Controls", command=updateCB)
    UpdateControlsButton.place(x=120, y=300)


def updateCB():
    global direction, LeftButtonEntry, RightButtonEntry, UpButtonEntry
    global DownButtonEntry, InvalidInputLabel1, USInputLabel1, TopCB

    # Labels for each entry either the text entered is valid or not.
    InvalidInputLabel1 = Label(
        TopCB,
        text="(Invalid Input!)",
        fg="red",
        font="Times 10 italic bold")
    InvalidInputLabel2 = Label(
        TopCB,
        text="(Invalid Input!)",
        fg="red",
        font="Times 10 italic bold")
    InvalidInputLabel3 = Label(
        TopCB,
        text="(Invalid Input!)",
        fg="red",
        font="Times 10 italic bold")
    InvalidInputLabel4 = Label(
        TopCB,
        text="(Invalid Input!)",
        fg="red",
        font="Times 10 italic bold")
    USInputLabel1 = Label(
        TopCB,
        text="Control Updated!",
        fg="green",
        font="Times 9 italic bold")
    USInputLabel2 = Label(
        TopCB,
        text="Control Updated!",
        fg="green",
        font="Times 9 italic bold")
    USInputLabel3 = Label(
        TopCB,
        text="Control Updated!",
        fg="green",
        font="Times 9 italic bold")
    USInputLabel4 = Label(
        TopCB,
        text="Control Updated!",
        fg="green",
        font="Times 9 italic bold")

    Alphabets = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z"]

    # If the new control key is valid,then unbind the old one and bind the new.
    if LeftButtonEntry.get() in Alphabets:
        L = "<" + LeftButtonEntry.get() + ">"
        canvas.unbind("<Left>")
        canvas.bind(L, leftKey)
        USInputLabel1.place(x=280, y=100)

    else:
        InvalidInputLabel1.place(x=280, y=100)

    if RightButtonEntry.get() in Alphabets:
        R = "<" + RightButtonEntry.get() + ">"
        canvas.unbind("<Right>")
        canvas.bind(R, rightKey)
        USInputLabel2.place(x=280, y=150)

    else:
        InvalidInputLabel2.place(x=280, y=150)

    if UpButtonEntry.get() in Alphabets:
        U = "<" + UpButtonEntry.get() + ">"
        canvas.unbind("<Up>")
        canvas.bind(U, upKey)
        USInputLabel3.place(x=280, y=200)

    else:
        InvalidInputLabel3.place(x=280, y=200)

    if DownButtonEntry.get() in Alphabets:
        D = "<" + DownButtonEntry.get() + ">"
        canvas.unbind("<Down>")
        canvas.bind(D, downKey)
        USInputLabel4.place(x=280, y=250)

    else:
        InvalidInputLabel4.place(x=280, y=250)


def Restart():
    window.destroy()
    MainFunc()


def QuitGame():
    root.destroy()


# This Function isn't necessary,I made it to prevent some errors,
# it works as a central.
def GamePause():
    global pause, Continue, GameResumed, width, height, window, canvas
    global PauseButtonLabel, snake, snakeSize, PauseImage, direction
    global score, currentlevel, LevelString, Levelvar, txt, ScoreVar

    if GameResumed is True:
        ActivatePause()
        GameResumed = False

    else:
        DisablePause()
        GameResumed = True

    window.update()


def ActivatePause():
    global Paused, pause, Continue, GameResumed, width, height, window
    global canvas, PauseButtonLabel, txt, ScoreVar, PauseImage, direction
    global snake, snakeSize, score, currentlevel, LevelString, Levelvar

    # Before pausing the game create a text and an image to notify the game is
    # paused.
    PauseButtonLabel.set(Continue)
    canvas.create_image(352, 100, image=PauseImage, tag="Pauseimg")
    canvas.create_text(
        352,
        230,
        text="Game Paused",
        font="Times 28 italic bold ",
        fill="white",
        tag="PauseLabel")
    canvas.update()


def DisablePause():
    global Paused, pause, Continue, GameResumed, width, height, direction
    global window, canvas, PauseButtonLabel, txt, ScoreVar, PauseImage
    global snake, snakeSize, score, currentlevel, LevelString, Levelvar

    # Remove the text and image,and give the user 3 seconds before resuming.
    PauseButtonLabel.set(pause)
    canvas.delete("Pauseimg")
    canvas.delete("PauseLabel")
    canvas.update()
    canvas.create_text(
        352,
        150,
        text="3",
        font="Times 32 italic bold ",
        fill="white",
        tag="3Seconds")
    canvas.update()
    time.sleep(1)
    canvas.delete("3Seconds")
    canvas.update()
    canvas.create_text(
        352,
        150,
        text="2",
        font="Times 32 italic bold ",
        fill="white",
        tag="2Seconds")
    canvas.update()
    time.sleep(1)
    canvas.delete("2Seconds")
    canvas.update()
    canvas.create_text(
        352,
        150,
        text="1",
        font="Times 32 italic bold ",
        fill="white",
        tag="1Second")
    canvas.update()
    time.sleep(1)
    canvas.delete("1Second")
    canvas.update()


def LevelIncrease():
    global currentlevel, GameSpeed, score, LevelString, OneTimer, OneTimer2
# The Leveling method, while your score increases,the snake speed will
# increase. and in final two levels, borders will close.
    if (50 > score > 20):
        currentlevel = 2
        LevelString = "Level= " + str(currentlevel)
        Levelvar.set(LevelString)
        GameSpeed = 120
    elif (90 > score > 40):
        currentlevel = 3
        LevelString = "Level= " + str(currentlevel)
        Levelvar.set(LevelString)
        GameSpeed = 100
    elif (130 > score > 80):
        currentlevel = 4
        LevelString = "Level= " + str(currentlevel)
        Levelvar.set(LevelString)
        GameSpeed = 80
    elif (190 > score > 120):
        currentlevel = 5
        LevelString = "Level= " + str(currentlevel)
        Levelvar.set(LevelString)
        GameSpeed = 70
    elif (250 > score > 180) and OneTimer is False:
        currentlevel = 6
        LevelString = "Level= " + str(currentlevel)
        Levelvar.set(LevelString)
        GameSpeed = 60
        OneTimer = True

        # if the game is loaded, no need to show the player this message again.
        if GameLoaded is False:
            canvas.create_text(
                width / 2,
                height / 2,
                fill="red",
                font="Times 30 italic bold",
                text="Top/Down Borders Are Now Closed!",
                underline=1,
                tag="notice")
            canvas.update()
            time.sleep(2)
            canvas.delete("notice")
            canvas.update()

    elif (score > 240) and OneTimer2 is False:
        currentlevel = "MAX"
        LevelString = "Level= " + str(currentlevel)
        Levelvar.set(LevelString)
        GameSpeed = 50
        OneTimer2 = True

        # if the game is loaded, no need to show the player this message again.
        if GameLoaded is False:
            canvas.create_text(
                width / 2,
                height / 2,
                fill="red",
                font="Times 40 italic bold",
                text="All Borders Are Now Closed!",
                underline=1,
                tag="notice2")
            canvas.update()
            time.sleep(2)
            canvas.delete("notice2")
            canvas.update()
    else:
        pass


# All Labels for the game window.
def labels():
    global Button1, BossButton, RedButton

    levellabel = Label(
        window,
        textvariable=Levelvar,
        fg="antiquewhite",
        font="Times 16 bold",
        bg="darkslategrey")
    levellabel.place(x=30, y=20)
    Button1 = Button(
        window,
        textvariable=PauseButtonLabel,
        font="Times 24 bold",
        fg="Black",
        highlightbackground='grey',
        width="8",
        height="2",
        command=lambda: GamePause())
    Button1.place(x=300, y=390)
    scorelabel = Label(
        window,
        fg="antiquewhite",
        textvariable=ScoreVar,
        font="Times 20 italic bold",
        bg="darkslategrey")
    scorelabel.place(x=345, y=18)
    RedButton = PhotoImage(file="redball.png")
    BossButton = Button(
        window,
        image=RedButton,
        text="Boss Key",
        bg="darkslategrey",
        highlightbackground="darkslategrey",
        command=lambda: BossKeyFunc())
    BossButton.place(x=600, y=380)
    RedButtonLabel = Label(
        window,
        text="Boss Key!",
        font="Arcade 16 bold",
        fg="yellow",
        bg="darkslategrey")
    RedButtonLabel.place(x=585, y=470)


# Whenever the snakes collides with food it grows,
# through this function
def growSnake():
    global lastElement, lastElementPos, pause, Continue, GameResumed
    global width, height, window, canvas
    global PauseButtonLabel, snake, snakeSize, score, currentlevel
    global LevelString, Levelvar, txt, ScoreVar, Image, PhotoImage, direction

    lastElement = len(snake) - 1
    lastElementPos = canvas.coords(snake[lastElement])
    snake.append(
        canvas.create_rectangle(
            0,
            0,
            snakeSize,
            snakeSize,
            fill="saddle brown",
            outline="saddle brown"))
    if (direction == "left"):
        canvas.coords(snake[lastElement + 1],
                      lastElementPos[0] + snakeSize,
                      lastElementPos[1],
                      lastElementPos[2] + snakeSize,
                      lastElementPos[3])

    elif (direction == "right"):
        canvas.coords(snake[lastElement + 1], lastElementPos[0] -
                      snakeSize, lastElementPos[1], lastElementPos[2] -
                      snakeSize, lastElementPos[3])

    elif (direction == "up"):
        canvas.coords(snake[lastElement + 1], lastElementPos[0],
                      lastElementPos[1] + snakeSize, lastElementPos[2],
                      lastElementPos[3] + snakeSize)

    else:
        canvas.coords(snake[lastElement + 1], lastElementPos[0],
                      lastElementPos[1] - snakeSize, lastElementPos[2],
                      lastElementPos[3] - snakeSize)


# Move the food to another place when its eaten.
def moveFood():
    global food, foodX, foodY
    canvas.move(food, (foodX * (-1)), (foodY * (-1)))
    foodX = random.randint(0, width - snakeSize)
    foodY = random.randint(0, height - snakeSize)
    canvas.move(food, foodX, foodY)


# When a and b are im the same position.
def overlapping(a, b):
    if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
        return True
    return False


# This function is the Core of our game.
def moveSnake():
    global positions, gameOver, OneTimer, OneTimer2, GameSpeed, GameLoaded
    global Loadpositions, pause, sHeadPos, foodPos, Continue, GameResumed
    global width, height, window, canvas, PauseButtonLabel, snake
    global snakeSize, score, currentlevel, LevelString, Levelvar, txt
    global ScoreVar, Image, PhotoImage, direction, FirstAttempt

    # A variable to use when the game is over and we dont want the function to
    # continue running and crashes.
    ForceStop = False

    # place the canvas at the middle of the window.
    canvas.place(x=23, y=50)

    # If the game has just been loaded, pause it.
    if GameLoaded:
        GamePause()

    positions = []

    # The loop To decide weather the game is resumed or not.
    while True:
        if GameResumed:
            positions.append(canvas.coords(snake[0]))
            if positions[0][0] < 0:

                # If the player reaches the final level prevent channelling
                # through the window from this side
                if currentlevel == "MAX":
                    GameOver()
                    ForceStop = True

                else:
                    canvas.coords(
                        snake[0],
                        width,
                        positions[0][1],
                        width - snakeSize,
                        positions[0][3])

            if ForceStop:
                break

            elif positions[0][2] > width:

                # If the player reaches the final level prevent channelling
                # through the window from this side
                if currentlevel == "MAX":
                    GameOver()
                    ForceStop = True

                else:
                    canvas.coords(
                        snake[0],
                        0 - snakeSize,
                        positions[0][1],
                        0,
                        positions[0][3])

            if ForceStop:
                break

            elif positions[0][3] > height:

                # If the player reaches the final level or level 6 prevent
                # channelling through the window from this side
                if currentlevel == "MAX" or currentlevel == 6:
                    GameOver()
                    ForceStop = True

                else:
                    canvas.coords(
                        snake[0],
                        positions[0][0],
                        0 - snakeSize,
                        positions[0][2],
                        0)

            if ForceStop:
                break

            elif positions[0][1] < 0:

                # If the player reaches the final level or level 6 prevent
                # channelling through the window from this side
                if currentlevel == "MAX" or currentlevel == 6:
                    GameOver()
                    ForceStop = True

                else:
                    canvas.coords(
                        snake[0],
                        positions[0][0],
                        height,
                        positions[0][2],
                        height - snakeSize)

            if ForceStop:
                break

            positions.clear()
            positions.append(canvas.coords(snake[0]))

            # Move the snake depending on the current direction the player
            # choose.
            if direction == "left":
                canvas.move(snake[0], -snakeSize, 0)
            elif direction == "right":
                canvas.move(snake[0], snakeSize, 0)
            elif direction == "up":
                canvas.move(snake[0], 0, -snakeSize)
            elif direction == "down":
                canvas.move(snake[0], 0, snakeSize)

            # Save the loacations for the head of the snake and the food.
            sHeadPos = canvas.coords(snake[0])
            foodPos = canvas.coords(food)

            # If the snake eats food.
            if overlapping(sHeadPos, foodPos):
                moveFood()
                growSnake()
                score += 10
                txt = "Score:" + str(score)
                ScoreVar.set(txt)

            # When the game is loaded dont check for collision, because this
            # may cause bugs.
            if GameLoaded is False:
                for i in range(1, len(snake)):
                    if overlapping(sHeadPos, canvas.coords(snake[i])):
                        GameOver()
                        ForceStop = True

            if ForceStop:
                break

            for i in range(1, len(snake)):
                positions.append(canvas.coords(snake[i]))

            if GameLoaded is False:
                for i in range(len(snake) - 1):
                    canvas.coords(snake[i + 1], positions[i][0],
                                  positions[i][1], positions[i][2],
                                  positions[i][3])

            # While the snake is moving.
            if gameOver is False:

                # Repeat this fumction.
                window.after(GameSpeed, moveSnake)
                # Check if the level increased depending on the score.
                LevelIncrease()

            # set the value to false so the game loads only once,otherwise its
            # gonna repeat loading forever.
            GameLoaded = False
            break

        else:
            window.update()

# Place the apple for the first time.


def placeFood():
    global food, foodX, foodY, GameLoaded, LoadfoodX, LoadfoodY
    food = canvas.create_rectangle(0, 0, snakeSize, snakeSize, fill="red")

    # If Game is loaded, place the apple in the same place as saved game.
    if GameLoaded:
        foodX = LoadfoodX
        foodY = LoadfoodY
    else:
        foodX = random.randint(0, width - snakeSize)
        foodY = random.randint(0, height - snakeSize)
    canvas.move(food, foodX, foodY)

#  4 Functions for changing directions.


def leftKey(event):
    global direction

    # If moving towards the right, you can not go left, to avoid eating
    # yourself backwards. thats a silly way for losing.
    if direction == "right":
        pass
    else:
        direction = "left"


def rightKey(event):
    global direction

    if direction == "left":
        pass
    else:
        direction = "right"


def upKey(event):
    global direction
    if direction == "down":
        pass
    else:
        direction = "up"


def downKey(event):
    global direction

    if direction == "up":
        pass
    else:
        direction = "down"


# Adjustments for our game window.
def setWindowDimensions():
    global window

    window = Toplevel()
    window.title("Snake Game")
    window.configure(bg="darkslategrey")
    window.geometry("750x500")  # window size
    window.resizable(False, False)
    return window


def ContinuePreviousRun():
    global FirstAttempt, GameResumed
    # If its not the first time to start the game .
    if FirstAttempt is False:
        # And the there is a running paused game.
        if GameResumed is False:

            # Hide main menu and display the game window back.
            window.deiconify()
            root.withdraw()
        else:
            tkinter.messagebox.showinfo(
                "Error", "No Game is Running Currently")
    else:
        tkinter.messagebox.showinfo("Error", "No Game is Running Currently")

# The Main Menu


# Usual window adjustments.
root = Tk()
root.title("Main Menu")
root.resizable(False, False)
root.geometry("750x550")
root.configure(bg="darkslategrey")

# Necessary intial values for those variables.
FirstAttempt = True
GameResumed = True
GameLoaded = False

# Creating the main menu
grass = PhotoImage(file="GrassSample.png")
StartButton = Button(
    root,
    text="New Game",
    command=lambda: NameFunc(),
    width=50,
    height=2,
    highlightbackground="black",
    bg="grey",
    fg="lemonchiffon",
    font="Arial 18 bold")
StartButton.place(x=50, y=170)
continueButton = Button(
    root,
    text="Continue",
    command=lambda: ContinuePreviousRun(),
    width=50,
    height=2,
    highlightbackground="black",
    bg="grey",
    fg="khaki",
    font="Arial 18 bold")
continueButton.place(x=50, y=240)
continueButton = Button(
    root,
    text="Exit",
    command=lambda: QuitGame(),
    width=50,
    height=2,
    highlightbackground="black",
    bg="grey",
    fg="palegoldenrod",
    font="Arial 18 bold")
continueButton.place(x=50, y=380)
MainLabel = Label(
    root,
    text="Snake Game",
    fg="khaki",
    font="Times 48 italic bold",
    bg="darkslategrey")
MainLabel.place(x=200, y=80)
LBButton = Button(
    root,
    text="Leaderboard",
    command=lambda: leaderboard(),
    width=50,
    height=2,
    highlightbackground="black",
    bg="grey",
    fg="white",
    font="Arial 18 bold")
LBButton.place(x=50, y=310)
CCHcanvas = Canvas(
    root,
    width=200,
    height=150,
    bg="darkslategrey",
    highlightbackground="darkslategrey")
CCHcanvas.place(x=0, y=10)
CCHcanvas.create_text(
    100,
    75,
    text="Cheat Code: Hint: X + 13 = 22",
    fill="white",
    angle=30,
    font="Times 12 italic bold")

root.mainloop()
