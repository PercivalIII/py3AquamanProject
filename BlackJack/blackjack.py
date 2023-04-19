import sys
# Importing several PyQt5 libraries for the program's user interface.
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QLineEdit, QAction, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QFont, QIntValidator
from PyQt5 import QtCore
# Import 'random' function for the shuffle mechanism in the blackjack game.
from random import shuffle
from PyQt5.QtTest import QTest

class Window(QMainWindow):
    
    # Initializes the PyQt5 formatting of the main program window.
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(0, 0, 640, 900)
        self.setFixedSize(640, 900)
        self.setWindowTitle("LBYCPA1 AQUAMAN - Blackjack")
        self.setWindowIcon(QIcon("favicon.ico.png"))
        
        Exit = QAction("&Exit application", self)
        Exit.setShortcut("Ctrl+Alt+E")
        Exit.triggered.connect(self.close)
        
        optionA = QAction("&Change Values", self)
        optionA.triggered.connect(self.openSettings)

        optionB = QAction("&Reset Game", self)
        optionB.triggered.connect(self.reset)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        editMenu = mainMenu.addMenu("&Options")
        fileMenu.addAction(Exit)
        editMenu.addAction(optionA)
        editMenu.addAction(optionB)

        sshFile = "style.css"
        with open(sshFile,"r") as fh:
            self.setStyleSheet(fh.read())

        self.home() # Calls the function home() to load the main 
    
    #
    # START 
    # A.) Main Program Graphical User Interface (GUI)
    #

    def home(self):
        # Declaring 'btnA' and 'btnB' as a array list for the buttons in home().
        # Each button is classified by its variable names.
        # 'btnA' is used for actions such as "Hit" and "Stand", while 'btnB' is used for betting.
        self.btnA=[]
        self.btnB=[]

        # Appending button elements in the btnA[] and btnB[] arrays.
        self.btnA.append(QPushButton("Hit", self)) # btnA[0]
        self.btnA.append(QPushButton("Stand", self)) # btnA[1]

        self.btnB.append(QPushButton("Bet $1", self)) # btnB[0]
        self.btnB.append(QPushButton("Bet $5", self)) # btnB[1]
        self.btnB.append(QPushButton("Bet $10", self)) # btnB[2]
        self.btnB.append(QPushButton("Bet $50", self)) # btnB[3]
        self.btnB.append(QPushButton("Bet $", self)) # btnB[4]
        self.btnB.append(QLineEdit("0", self)) # btnB[5]
        
        self.resize()
        # Every variable data here is used for storing information.
        self.var_bet = 1 # The player's amount to bet.
        self.pic = []
        self.drawn = 0
        self.picIndex = 0
        self.indent = [150, 150]
        self.play_test = 1 # If it's 1 -> The game starts, if it's 2 -> the UI application restarts the blackjack deck, then starts the game. Used for conditional statements.
        self.oneOrTwoCards = 0
        self.totalGamesCount = 0 # The player's overall game count, every game increments to 1.
        self.var_money = 100 # The player's money.
        self.var_difficulty = 21 # The value to get a blackjack in normal games in 21. Exceeding 21 is a instant lose. This is declared as a integer variable for the adjustable difficulty.

        # 'btnA' buttons for hitting & standing.
        self.btnA[0].clicked.connect(self.play)
        self.btnA[0].resize(100, 50)
        self.btnA[0].move(0, 100)
        self.btnA[0].setShortcut("H")
       
        self.btnA[1].clicked.connect(self.stand)
        self.btnA[1].move(0, 150)
        self.btnA[1].resize(100, 50)
        self.btnA[1].setShortcut("S")

        # Declaring 'money' and 'gameCount' as text elements, set as color white.
        # Each text element gets the integer variable data from 'var_money' and 'totalGamesCount' to show the player's money and their total games.
        self.money = QLabel(("Money: $%s"%(str(self.var_money))), self)
        self.money.setStyleSheet(("background-color: white;"))

        self.gameCount = QLabel(("Total Games: %s"%(str(self.totalGamesCount))), self)
        self.gameCount.setStyleSheet(("background-color: white;"))

        # btnB buttons for betting.
        self.btnB[0].clicked.connect(lambda: self.bet(1, 0))
        self.btnB[0].resize(100, 50)
        self.btnB[0].move(0, 250)
        self.btnB[0].setEnabled(True)
        self.btnB[0].setStyleSheet("background-color:black;color:white;")
        self.btnB[0].setShortcut("1")
        
        self.btnB[1].clicked.connect(lambda: self.bet(5, 1)) # Bet $5 button
        self.btnB[1].resize(100, 50)
        self.btnB[1].move(0, 300)
        self.btnB[1].setEnabled(True)
        self.btnB[1].setShortcut("2")

        self.btnB[2].clicked.connect(lambda: self.bet(10, 2)) # Bet $10 button
        self.btnB[2].resize(100, 50)
        self.btnB[2].move(0, 350)
        self.btnB[2].setEnabled(True)
        self.btnB[2].setShortcut("3")
        
        self.btnB[3].clicked.connect(lambda: self.bet(50, 3)) # Bet $50 button
        self.btnB[3].resize(100, 50)
        self.btnB[3].move(0, 400)
        self.btnB[3].setEnabled(True)
        self.btnB[3].setShortcut("4")

        self.btnB[4].clicked.connect(lambda: self.bet(int(self.btnB[5].text()), 4)) # Bet $ button option
        self.btnB[4].resize(100, 50)
        self.btnB[4].move(0, 450)
        self.btnB[4].setEnabled(True)
        self.btnB[4].setShortcut("5")

        validator = QIntValidator()
        self.btnB[5].setValidator(validator)
        self.btnB[5].textEdited.connect(lambda: self.bet(int(self.btnB[5].text()), 4)) # Bet $ textbox
        self.btnB[5].resize(100, 30)
        self.btnB[5].move(0, 500)
        self.btnB[5].setEnabled(True)
        
        # Declaring fortA and fontB for adjusting text font sizes in elements.
        fontA = QFont()
        fontB = QFont()
        fontA.setPointSize(20)
        fontB.setPointSize(10)

        # Element for money indicator (Player).
        self.money.move(0, 30)
        self.money.resize(200, 50)
        self.money.setFont(fontA)

        # Element for total play amount indicator.
        self.gameCount.move(6, 870)
        self.gameCount.resize(100, 20)
        self.gameCount.setFont(fontB)

        # Element for Player card deck text element.
        self.player = QLabel("", self)
        self.player.setStyleSheet(("background-color: transparent;"))
        self.player.move(120, 420)
        self.player.resize(500, 50)
        self.player.setFont(fontB)

        # Element for Dealer card deck text element.
        self.dealer = QLabel("", self)
        self.dealer.move(120, 815)
        self.dealer.resize(500, 50)
        self.dealer.setStyleSheet(("background-color: transparent;"))
        self.dealer.setFont(fontB)

        # Element for the "You Win!", "Dealer Win!", and "Tie!" indicator.
        self.win = QLabel("", self)
        self.win.move(400, 30)
        self.win.resize(150,  50)
        self.win.setStyleSheet(("background-color: transparent;"))
        self.win.setFont(fontA)
        
        self.show() # Calls the function show() to initialize the changes made in PyQt5.

    # Function openSettings() is used for opening the Settings window.
    def openSettings(self):
        self.window = QMainWindow()
        self.settingsUI(self.window)
        self.window.show() # Calls the function show() to initialize and display  the settings window.

    #
    # END
    # A.) Main Program Graphical User Interface (GUI)
    #

    #
    # START
    # B.) Settings Graphical User Interface (GUI)
    #

    # Function settingsUI() to initialize Settings window.
    def settingsUI(self, settingsUI):

        # Declaring integer variables to separate it from the variables used for the blackjack game.
        # The integer variables here are used to check the changes made before processing it to the real blackjack game decided by the user.
        self.difficultyValue = self.var_difficulty
        self.moneyValue = self.var_money

        # Initializes the Qt5 formatting of the Settings window.
        settingsUI.setObjectName("settingsUI")
        settingsUI.resize(400, 200)
        settingsUI.setFixedSize(settingsUI.width(), settingsUI.height())
        settingsUI.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)

        # Elements for text indicators to the player money and difficulty value.
        self.changeMoneyLabel = QLabel(settingsUI)
        self.changeMoneyLabel.setGeometry(20, 20, 111, 16)
        self.changeMoneyLabel.setObjectName("changeMoneyLabel")
        
        self.changeDifficultyLabel = QLabel(settingsUI)
        self.changeDifficultyLabel.setGeometry(20, 50, 101, 16)
        self.changeDifficultyLabel.setObjectName("changeDifficultyLabel")
        
        # Elements for textboxs.
        # The player money textbox 'changePlayerMoneyLine' is editable to any numerical values in order to change it by the user.
        # The game difficulty textbox 'changeDifficultyLine' is read-only; only used as an indicator for the user to see changes/updates.
        self.changePlayerMoneyLine = QLineEdit(settingsUI)
        self.changePlayerMoneyLine.setGeometry(140, 20, 113, 20)
        self.changePlayerMoneyLine.setObjectName("changePlayerMoneyLine")

        self.changeDifficultyLine = QLineEdit(settingsUI)
        self.changeDifficultyLine.setGeometry(140, 50, 113, 20)
        self.changeDifficultyLine.setObjectName("changeDifficultyLine")
        self.changeDifficultyLine.setReadOnly(True)
        
        # Elements for buttons in the Settings UI.
        self.applyButton = QPushButton(settingsUI)
        self.applyButton.setGeometry(200, 160, 75, 23)
        self.applyButton.setObjectName("applyButton")
        self.applyButton.clicked.connect(lambda: self.settingsUpdate())

        self.exitButton = QPushButton(settingsUI)
        self.exitButton.setGeometry(290, 160, 75, 23)
        self.exitButton.setObjectName("exitButton")
        self.exitButton.clicked.connect(settingsUI.close)

        self.difficultyStandard = QPushButton(settingsUI)
        self.difficultyStandard.setGeometry(30, 80, 120, 23)
        self.difficultyStandard.setObjectName("difficultyStandard")
        self.difficultyStandard.clicked.connect(lambda: self.difficultyChange(21)) # Standard Difficulty [21] button

        self.difficultyEasy = QPushButton(settingsUI)
        self.difficultyEasy.setGeometry(30, 110, 120, 23)
        self.difficultyEasy.setObjectName("difficultyEasy")
        self.difficultyEasy.clicked.connect(lambda: self.difficultyChange(30)) # Easy Difficulty [30] button

        self.difficultyIntermediate = QPushButton(settingsUI)
        self.difficultyIntermediate.setGeometry(30, 140, 120, 23)
        self.difficultyIntermediate.setObjectName("difficultyIntermediate")
        self.difficultyIntermediate.clicked.connect(lambda: self.difficultyChange(16)) # Intermediate Difficulty [16] button

        self.difficultyHard = QPushButton(settingsUI)
        self.difficultyHard.setGeometry(30, 170, 120, 23)
        self.difficultyHard.setObjectName("difficultyHard")
        self.difficultyHard.clicked.connect(lambda: self.difficultyChange(12)) # Hard Difficulty [12] button

        # Elements for the status of the game values in the Settings UI.
        self.currentStatusLabel = QLabel(settingsUI)
        self.currentStatusLabel.setGeometry(210, 80, 111, 16)
        self.currentStatusLabel.setObjectName("currentStatusLabel")

        self.playerMoneyStatus = QLabel(settingsUI)
        self.playerMoneyStatus.setGeometry(220, 100, 180, 16)
        self.playerMoneyStatus.setObjectName("playerMoneyStatus")

        self.blackjackDifficultyStatus = QLabel(settingsUI)
        self.blackjackDifficultyStatus.setGeometry(220, 115, 121, 16)
        self.blackjackDifficultyStatus.setObjectName("blackjackDifficultyStatus")

        self.retranslateUi(settingsUI) # Calls the function retranslateUi(settingsUI) to initialize the settings text elements.
        QtCore.QMetaObject.connectSlotsByName(settingsUI)

        # Calls the function setText to specific variable data to change the text content.
        self.changeDifficultyLine.setText("%d"%(self.difficultyValue))
        self.blackjackDifficultyStatus.setText("Blackjack difficulty = %d"%(self.var_difficulty))
        
        self.changePlayerMoneyLine.setText("%d"%(self.moneyValue))
        self.playerMoneyStatus.setText("Player Money = $%d"%(self.var_money))

    # Function difficultyChange(value) to adjust the difficulty of the blackjack game by changing the '21' rule.
    def difficultyChange(self, value):
        self.difficultyValueChange = value
        self.changeDifficultyLine.setText("%d"%(value))

    # Function settingsUpdate() to apply every change made by the user to the blackjack game such as their money value and the game difficulty.
    def settingsUpdate(self):
        self.var_difficulty = self.difficultyValueChange
        self.var_money = int(self.changePlayerMoneyLine.text())
        self.money.setText("Money: $%s"%(str(self.var_money)))
        self.changePlayerMoneyLine.setText("%d"%(self.moneyValue))
        self.playerMoneyStatus.setText("Player Money = $%d"%(self.var_money))
        self.blackjackDifficultyStatus.setText("Blackjack difficulty = %d"%(self.var_difficulty))

        # Intiializes the PyQt5 pop-up messagebox to remind the user that the game's settings has been changed/updated.
        self.confirmUser = QMessageBox()
        self.confirmUser.setWindowTitle("Confirm")
        self.confirmUser.setText("The changes has been made!")
        self.confirmUser.setIcon(QMessageBox.Information)
        self.confirmUser.exec_() # Calls function exec_() to display the messagebox.

    # Function retranslateUi(settingsUI) to initialize the Settings text elements.
    def retranslateUi(self, settingsUI):
        _translate = QtCore.QCoreApplication.translate
        settingsUI.setWindowTitle(_translate("settingsUI", "Settings"))
        self.changeMoneyLabel.setText(_translate("settingsUI", "Change player money:"))
        self.changeDifficultyLabel.setText(_translate("settingsUI", "Change difficulty:"))
        self.applyButton.setText(_translate("settingsUI", "Apply"))
        self.exitButton.setText(_translate("settingsUI", "Exit"))
        self.difficultyStandard.setText(_translate("settingsUI", "Standard [21]"))
        self.difficultyEasy.setText(_translate("settingsUI", "Easy [30]"))
        self.difficultyIntermediate.setText(_translate("settingsUI", "Intermediate [16]"))
        self.difficultyHard.setText(_translate("settingsUI", "Hard [12]"))
        self.currentStatusLabel.setText(_translate("settingsUI", "Current status:"))
        self.playerMoneyStatus.setText(_translate("settingsUI", "Player Money = $"))
        self.blackjackDifficultyStatus.setText(_translate("settingsUI", "Blackjack difficulty = 21"))

    #
    # END
    # B.) Settings Graphical User Interface (GUI)
    #

    #
    # START
    # C.) Blackjack Functionality
    #

    # Function play() to start the game depending on the 'play_test' value.
    def play(self):
        if self.play_test == 1:
            self.hitMe()
        elif self.play_test == 2:
            self.restart()

    # Function empty() to wipe the player and dealer's card deck in the main program's GUI, resets variables such as 'cardValue' and 'drawnCard', and also sets 'win' and 'charlie' to 0.
    def empty(self):
        global drawnCards, cardValue, win, charlie
        for i in range(0, len(self.pic)):
            self.pic[i].resize(0, 0)
        self.indent[0], self.indent[1], self.picIndex, self.pic, cardValue, drawnCards = 150, 150, 0, [], [[], []], [[], []]
        win = 0
        charlie = 0

    # Function resize() to update the changes made in the main program's GUI overall.
    def resize(self):
        self.btnA[1].setEnabled(False)
        for i in range(0, len(self.btnB)):
            self.btnB[i].setEnabled(False)

    # Function bet(n, index) to process the player's bet; 
    def bet(self, n, index):
        self.var_bet = n
        for i in range(0, 5):
            self.btnB[i].setStyleSheet("background-color:none;")
        self.btnB[index].setStyleSheet("background-color:black;color:white;")
        if self.var_bet > self.var_money:
            self.var_bet = self.var_money
        if self.var_bet < 0:
            self.var_bet = self.var_bet
    
    # Function hitMe() for the player to hit a card.
    def hitMe(self):
        # When the player starts to hit the dealer, all betting options will be inaccessible until the game ends.
        for i in range(0, len(self.btnB)):
            self.btnB[i].setEnabled(False)

        if self.oneOrTwoCards < 0:
            self.oneOrTwoCards = 0
        
        # This is where the game starts. 
        # Player draws 2 cards, while dealer draws 1 card.
        if self.oneOrTwoCards == 0:
            self.btnA[1].setEnabled(True)
            self.cardDraw(2, 2, 1, "You", 0, 95)
            self.cardDraw(1, 1, 0, "Dealer", 1, 490)
            self.oneOrTwoCards += 1

        # If the player has one or two cards in their card deck, they can only draw 1 card.
        # The dealer is also affected to this.
        elif self.oneOrTwoCards > 0:
            self.cardDraw(1, 1, 1, "You", 0, 95)

        self.var_money = round(self.var_money, 2) # Turns 'var_money' into an decimal if the player's win contains less than $1.
        self.money.setText("Money: $%s"%(str(self.var_money)))

    # Function cardDraw() if the player or dealer draws a card.
    # The arguments of cardDraw(self, handLength, OneOrTwo, plyr, name, indentIndex, line) goes as follows:
    # - handLength is the amount of cards in their deck.
    # - OneOrTwo if the
    # - plyr to classify the owner of the card deck. plyr = 1 is the dealer, while plyr = 2 is the player.
    # - name to indicate whose card draw is, and is also used for the player / dealer card deck status in the text box below.
    # - indentIndex and line is used for formatting purposes for the card deck being displayed in the main program's GUI.
    def cardDraw(self, handLength, OneOrTwo, plyr, name, indentIndex, line):
        global win, drawnCards, cardValue, charlie # Function to access the global variable data 'win', 'drawnCards', 'cardValue', and 'charlie'. 
        hand = []
        for i in range(0, handLength):
            # Appends the content of the item specified in 'cardDeck[self.drawn]' in 'card' and 'drawnCards[plyr].
            hand.append(cardDeck[self.drawn]) 
            drawnCards[plyr].append(cardDeck[self.drawn])

            # The process of displaying the player / dealer card deck in the main program's GUI.
            # Technically, the vector images '.svg' of the 52 standard card-deck are used for displaying the player / dealer card deck.
            # The vector images are named in the same structure as 'cardDeck[]' items are called.

            # The structures goes: ["1 to 9 or King/Queen/Jack" of "Diamonds/Clubs/Hearts/Spades"]

            self.pic.append(QLabel(self))
            self.pic[self.picIndex].setPixmap(QPixmap("img/%s.svg"%(cardDeck[self.drawn])))
            self.pic[self.picIndex].setGeometry(self.indent[indentIndex], line, 238, 322)
            self.indent[indentIndex] += 50
            self.pic[self.picIndex].show()
            
            # Integer variables increments to 1.
            self.picIndex += 1
            self.drawn += 1

        # Looping process to calculate the value sum of the player / dealer card deck.
        for i in range(0, OneOrTwo):
            if "Ace" in hand[i]:
                cardValue[plyr].append(11)
            elif hand[i][:1] in ("Q", "J", "K"):
                cardValue[plyr].append(10)
            else:
                cardValue[plyr].append(int(hand[i][0:2])) # 0:2 takes the 2 first letters from the string. 
                # Checks the contents of array list 'hand[i]', and only checks the number.
                # e.g If 'hand[1]' contains '6 of Diamonds', 'cardValue[plyr]' will only append the integer '6' only.

        self.testForAces(plyr)

        # Every operation calculates the sum of every item (individual card value), stored in the array list 'cardValue[plyr]'.
        if OneOrTwo == 2:
            if sum(cardValue[plyr]) == (self.var_difficulty):
                card = "%s got a %s and a %s, which is a blackjack!"%(name, hand[0], hand[1])
                win = 1
                self.check()
            else:
                card = "%s got a %s and a %s which is a total of %s."%(name, hand[0], hand[1], sum(cardValue[plyr]))
            self.player.setText(card)
            self.player.setStyleSheet(("background-color: white;"))
        
        elif OneOrTwo == 1:
            if len(cardValue[plyr]) >= 5 and sum(cardValue[plyr]) <= (self.var_difficulty) and plyr == 1: # If the player's card deck contains 5 cards, while the player's card deck sum value is higher than the dealer's card deck.
                card = "%s got a %s, which is a five card Charlie!"%(name, hand[0])
                charlie = 1
                self.check()
            elif sum(cardValue[plyr]) == (self.var_difficulty):
                card = "%s got a %s, which is a total of %s."%(name, hand[0], sum(cardValue[plyr])) # If the player's card deck sum value is equivalent to 'var_difficulty' value.
                self.resize()
                if plyr != 0:
                    self.stand()
            elif sum(cardValue[plyr]) >= (self.var_difficulty + 1): # If the player's card deck sum value is less than or equal to 'var_difficulty + 1' value.
                card = "%s got a %s, which is %s and got busted."%(name, hand[0], sum(cardValue[plyr]))
                self.resize()
                if plyr == 1:
                    self.check()
                self.play_test = 2
                self.enableBet()
            else:
                card = "%s got a %s, which is a total of %s."%(name, hand[0], sum(cardValue[plyr]))
            
            if plyr == 0: # Updates the dealer's card deck text box if plyr == 0.
                self.dealer.setText(card)
                self.dealer.setStyleSheet(("background-color: white;"))
            else: # Updates the player's card deck text box if plyr != 0, assuming plyr == 1.
                self.player.setText(card)
                self.player.setStyleSheet(("background-color: white;"))
        
        self.initCheck()
    
    # Function testForAces() to check for 'Ace' cards in the player / dealer drawn card.F
    def testForAces(self, plyr):
        if sum(cardValue[plyr]) >= (self.var_difficulty + 1):
            for i in range(0, len(cardValue[plyr])):
                if "Ace" in drawnCards[plyr][i]:
                    if cardValue[plyr][i] == 1:
                        continue
                    else:
                        cardValue[plyr][i] = 1
                        break
    
    # Function check() to process if the player or dealer is the winner, otherwise it's a tie. 
    def check(self):
        global win, cardValue, drawnCards, charlie # Function to access the global variable data 'win', 'drawnCards', 'cardValue', and 'charlie'. 
        self.var_money = round(self.var_money, 2) # Turns 'var_money' into an decimal in case the player's win contains less than $1.
        if win == 1:
            self.var_money += self.var_bet * 1.5
            self.money.setText("Money: $%s"%(str(self.var_money)))
            self.win.setText("You Win!")

        elif charlie == 1:
            self.var_money += self.var_bet
            self.money.setText("Money: $%s"%(str(self.var_money)))
            self.win.setText("You Win!")
            
        elif sum(cardValue[1]) == sum(cardValue[0]):
            self.win.setText("Tie")

        elif (sum(cardValue[1]) >= (self.var_difficulty + 1) or sum(cardValue[1]) < sum(cardValue[0])) and not sum(cardValue[0]) >= (self.var_difficulty + 1):
            self.var_money -= self.var_bet
            self.money.setText("Money: $%s"%(str(self.var_money)))
            self.win.setText("Dealer Win!")

        elif (sum(cardValue[0]) >= (self.var_difficulty + 1) or sum(cardValue[1]) > sum(cardValue[0])) and not sum(cardValue[1]) >= (self.var_difficulty + 1):
            self.var_money += self.var_bet
            self.money.setText("Money: $%s"%(str(self.var_money)))
            self.win.setText("You Win!")

        self.updateCheck()

    # Function initCheck() works at the very beginnning of the game. This is used for blackjack games when the difficulty value is lower than 21.
    def initCheck(self):
        self.var_money = round(self.var_money, 2) # Turns 'var_money' into an decimal in case the player's win contains less than $1.
        if (sum(cardValue[1]) >= (self.var_difficulty + 1)):
            self.var_money -= self.var_bet
            self.money.setText("Money: $%s"%(str(self.var_money)))
            self.win.setText("Dealer Win!")
            self.updateCheck()

    # Function updateCheck() is done after check() has been executed or when the game has decided who wins the game. Function resets some variables and shuffles the card deck. 
    def updateCheck(self):
        global win, cardValue, drawnCards, charlie # Function to access the global variable data 'win', 'drawnCards', 'cardValue', and 'charlie'. 
        self.win.setStyleSheet(("background-color: white;"))
        shuffle(cardDeck) # Shuffles the 'cardDeck' array list.
        drawnCards, cardValue, self.oneOrTwoCards, win, self.drawn = [[], []], [[], []], -1, 0, 0 # Resets back values and conditions of the blackjack game back from the start.
        self.resize()
        self.play_test = 2 # Sets 'play_test' = 2.
        self.enableBet() # Enable access to the 'btnB[]' buttons.
        self.totalGamesCount += 1 # Integer variable 'totalGamesCount' increments to  1.
        self.gameCount.setText("Total Games: %s"%(str(self.totalGamesCount)))  # Updates the 'gameCount' text element.


    # Function enableBet() to enables betting options by enabling the 'btnB' variable buttons functionality.
    def enableBet(self):
        for i in range(0, len(self.btnB)):
            self.btnB[i].setEnabled(True)

    # Function restart() to restart the blackjack game.
    def restart(self):
        self.resize()
        self.play_test = 1 # Sets 'play_test' = 2.
        self.win.setText("") 
        self.dealer.setText("")
        self.player.setText("")
        self.empty()
        self.dealer.setStyleSheet(("background-color: transparent;"))
        self.player.setStyleSheet(("background-color: transparent;"))
        self.win.setStyleSheet(("background-color: transparent;"))
        self.hitMe() # Starts the blackjack game.

    # Function reset() to reset the blackjack game back from the very beginning; resets the player money to 100, resets the player's total play count back to 0.
    def reset(self):
        self.resize()
        self.play_test = 1
        self.oneOrTwoCards = 0
        self.win.setText("")
        self.dealer.setText("")
        self.player.setText("")
        self.dealer.setStyleSheet(("background-color: transparent;"))
        self.player.setStyleSheet(("background-color: transparent;"))
        self.win.setStyleSheet(("background-color: transparent;"))
        self.empty()
        self.var_money = 100
        self.money.setText("Money: $%s"%(str(self.var_money)))
        self.totalGamesCount = 0
        self.gameCount.setText("Total Games: %s"%(str(self.totalGamesCount)))
        self.enableBet()

    # Function stand() if the player decides to stand in their current card deck, but it's also used if the player's card value sum is equals to 'var_difficulty' when it's player's turn.
    def stand(self):
        self.btnA[0].setEnabled(False)
        self.resize()
        speed = 100 # Declares 'speed' to add delay when the dealer is drawing their card.
        while True:
            if sum(cardValue[0]) <= 16 and sum(cardValue[1]) != 0 and sum(cardValue[1]) <= (self.var_difficulty + 1):
                QTest.qWait(speed) # Set speed limit to add delay when the dealer is drawing their cards.
                self.cardDraw(1, 1, 0, "Dealer",1 , 490)
                speed += 200
            else:
                self.resize()
                self.play_test = 2
                self.enableBet()
                self.check()
                self.btnA[0].setEnabled(True)
                break

# Global variables primarily used by the "Blackjack Functionality" section.
drawnCards = [[], []]
cardValue = [[], []]
cardDeck = []
ans = 6 # The total decks you want to play with.
shuffle(cardDeck) # Shuffles the 'cardDeck' array list.
win = 0
charlie = 0

# This is where all of the 52 playing cards are processed, all of them are compiled and stored in the 'cardDeck' array list.
# if shuffle(cardDeck) is called, the array list in 'cardDeck' is shuffled in random order. 
for a in range(0, ans):
    for j in ("Hearts", "Diamonds", "Spades", "Clubs"):
        for i in ("2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"):
            cardDeck.append("%s of %s"%(i, j))

    #
    # END
    # C.) Blackjack Functionality
    #

# Initializes the entire program.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window()
    sys.exit(app.exec_())
