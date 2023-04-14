import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QLineEdit, QAction, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QFont, QIntValidator
from PyQt5 import QtCore
from random import shuffle
from PyQt5.QtTest import QTest

class Window(QMainWindow):
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

        sshFile="style.css"
        with open(sshFile,"r") as fh:
            self.setStyleSheet(fh.read())

        self.home()
        
    def home(self):
        self.btnA=[]
        self.btnB=[]

        self.btnA.append(QPushButton("Hit", self))
        self.btnA.append(QPushButton("Stand", self))

        self.btnB.append(QPushButton("Bet $1", self))
        self.btnB.append(QPushButton("Bet $5", self))
        self.btnB.append(QPushButton("Bet $10", self))
        self.btnB.append(QPushButton("Bet $50", self))
        self.btnB.append(QPushButton("Bet $", self))
        self.btnB.append(QLineEdit("0", self))
        
        self.resize()
        self.var_bet = 1
        self.pic = []
        self.drawn = 0
        self.picIndex = 0
        self.indent=[150, 150]
        self.play_test = 1
        self.oneOrTwoCards = 0
        self.totalGamesCount = 0
        self.var_money = 100
        self.var_difficulty = 21

        # Buttons for hitting & standing (Player)
        self.btnA[0].clicked.connect(self.play)
        self.btnA[0].resize(100, 50)
        self.btnA[0].move(0, 100)
        self.btnA[0].setShortcut("H")
       
        self.btnA[1].clicked.connect(self.stand)
        self.btnA[1].move(0, 150)
        self.btnA[1].resize(100, 50)
        self.btnA[1].setShortcut("S")

        self.money = QLabel(("Money: $%s"%(str(self.var_money))), self)
        self.money.setStyleSheet(("background-color: white;"))

        self.gameCount = QLabel(("Total Games: %s"%(str(self.totalGamesCount))), self)
        self.gameCount.setStyleSheet(("background-color: white;"))

        # 1st is player, 2nd is dealer
        # Buttons for betting (Player)
        self.btnB[0].clicked.connect(lambda: self.bet(1, 0))
        self.btnB[0].resize(100, 50)
        self.btnB[0].move(0, 250)
        self.btnB[0].setEnabled(True)
        self.btnB[0].setStyleSheet("background-color:black;color:white;")
        self.btnB[0].setShortcut("1")
        
        self.btnB[1].clicked.connect(lambda: self.bet(5, 1))
        self.btnB[1].resize(100, 50)
        self.btnB[1].move(0, 300)
        self.btnB[1].setEnabled(True)
        self.btnB[1].setShortcut("2")

        self.btnB[2].clicked.connect(lambda: self.bet(10, 2))
        self.btnB[2].resize(100, 50)
        self.btnB[2].move(0, 350)
        self.btnB[2].setEnabled(True)
        self.btnB[2].setShortcut("3")
        
        self.btnB[3].clicked.connect(lambda: self.bet(50, 3))
        self.btnB[3].resize(100, 50)
        self.btnB[3].move(0, 400)
        self.btnB[3].setEnabled(True)
        self.btnB[3].setShortcut("4")

        self.btnB[4].clicked.connect(lambda: self.bet(int(self.btnB[5].text()), 4))
        self.btnB[4].resize(100, 50)
        self.btnB[4].move(0, 450)
        self.btnB[4].setEnabled(True)
        self.btnB[4].setShortcut("5")

        validator = QIntValidator()
        self.btnB[5].setValidator(validator)
        self.btnB[5].textEdited.connect(lambda: self.bet(int(self.btnB[5].text()), 4))
        self.btnB[5].resize(100, 30)
        self.btnB[5].move(0, 500)
        self.btnB[5].setEnabled(True)
        
        fontA = QFont()
        fontB = QFont()
        fontA.setPointSize(20)
        fontB.setPointSize(10)

        # Element for money indicator (Player)
        self.money.move(0, 30)
        self.money.resize(200, 50)
        self.money.setFont(fontA)

        # Element for total play amount indicator
        self.gameCount.move(6, 870)
        self.gameCount.resize(100, 20)
        self.gameCount.setFont(fontB)

        # Element for Player card deck textbox
        self.player = QLabel("", self)
        self.player.setStyleSheet(("background-color: transparent;"))
        self.player.move(120, 420)
        self.player.resize(500, 50)
        self.player.setFont(fontB)

        # Element for Dealer card deck textbox
        self.dealer = QLabel("", self)
        self.dealer.move(120, 815)
        self.dealer.resize(500, 50)
        self.dealer.setStyleSheet(("background-color: transparent;"))
        self.dealer.setFont(fontB)

        # Element for win indicator
        self.win = QLabel("", self)
        self.win.move(400, 30)
        self.win.resize(150,  50)
        self.win.setStyleSheet(("background-color: transparent;"))
        self.win.setFont(fontA)
        
        self.show()

    def openSettings(self):
        self.window = QMainWindow()
        self.settingsUI(self.window)
        self.window.show()

    def play(self):
        if self.play_test == 1:
            self.hitMe()
        elif self.play_test == 2:
            self.restart()

    def empty(self):
        global drawnCards, cardValue, win, charlie
        for i in range(0, len(self.pic)):
            self.pic[i].resize(0, 0)
        self.indent[0], self.indent[1], self.picIndex, self.pic, cardValue, drawnCards = 150, 150, 0, [], [[], []], [[], []]
        win = 0
        charlie = 0
    
    def resize(self):
        self.btnA[1].setEnabled(False)
        for i in range(0, len(self.btnB)):
            self.btnB[i].setEnabled(False)
    
    def bet(self, n, index):
        self.var_bet = n
        for i in range(0, 5):
            self.btnB[i].setStyleSheet("background-color:none;")
        self.btnB[index].setStyleSheet("background-color:black;color:white;")

        if self.var_bet > self.var_money:
            self.var_bet = self.var_money

        if self.var_bet < 0:
            self.var_bet = self.var_bet

    def cardDraw(self, handLength, OneOrTwo, plyr, name, indentIndex, line):
        global win, drawnCards, cardValue, charlie
        hand =[]
        for i in range(0, handLength):
            hand.append(cardDeck[self.drawn])
            drawnCards[plyr].append(cardDeck[self.drawn])
            self.pic.append(QLabel(self))
            self.pic[self.picIndex].setPixmap(QPixmap("img/%s.svg"%(cardDeck[self.drawn])))
            self.pic[self.picIndex].setGeometry(self.indent[indentIndex], line, 238, 322)
            self.indent[indentIndex] += 50
            self.pic[self.picIndex].show()
            
            self.picIndex+=1
            self.drawn+=1

        for i in range(0, OneOrTwo):
            if "Ace" in hand[i]:
                cardValue[plyr].append(11)
            elif hand[i][:1] in ("Q", "J", "K"):
                cardValue[plyr].append(10)
            else:
                cardValue[plyr].append(int(hand[i][0:2])) #0:2 takes the 2 first letters from the string
        
        self.testForAces(plyr)
        if OneOrTwo == 2:
            if sum(cardValue[plyr]) == (self.var_difficulty):
                card="%s got a %s and a %s, \nwhich is a blackjack."%(name, hand[0], hand[1])
                win = 1
                self.check()
            else:
                card="%s got a %s and a %s which is a total of %s."%(name, hand[0], hand[1], sum(cardValue[plyr]))
            self.player.setText(card)
            self.player.setStyleSheet(("background-color: white;"))

        elif OneOrTwo == 1:
            if len(cardValue[plyr]) >= 5 and sum(cardValue[plyr]) <= (self.var_difficulty) and plyr == 1: # ADD KRAV NOT OVER 21 and only for player
                card="%s got a %s, which is a five card Charlie."%(name, hand[0])
                charlie = 1
                self.check()
            elif sum(cardValue[plyr]) == (self.var_difficulty):
                card="%s got a %s, which is a total of %s."%(name, hand[0], sum(cardValue[plyr]))
                self.resize()
                if plyr != 0:
                    self.stand()
            elif sum(cardValue[plyr]) >= (self.var_difficulty + 1):
                card="%s got a %s, which is %s and got busted."%(name, hand[0], sum(cardValue[plyr]))
                self.resize()
                if plyr == 1:
                    self.check()
                self.play_test = 2
                self.enableBet()
            else:
                card="%s got a %s, which is a total of %s."%(name, hand[0], sum(cardValue[plyr]))

            if plyr == 0:
                self.dealer.setText(card)
                self.dealer.setStyleSheet(("background-color: white;"))
            else:
                self.player.setText(card)
                self.player.setStyleSheet(("background-color: white;"))
    
    def testForAces(self, plyr):
        if sum(cardValue[plyr]) >= (self.var_difficulty + 1):
            for i in range(0, len(cardValue[plyr])):
                if "Ace" in drawnCards[plyr][i]:
                    if cardValue[plyr][i] == 1:
                        continue
                    else:
                        cardValue[plyr][i] = 1
                        break
    
    def check(self):
        global win, cardValue, drawnCards, charlie
        self.var_money = round(self.var_money, 2)
        if win == 1:
            print("OK BLACKJACK")
            self.var_money += self.var_bet * 1.5
            self.money.setText("Money: $%s"%(str(self.var_money)))
            self.win.setText("You Win!")

        elif charlie == 1:
            print("CHARLIE")
            self.var_money += self.var_bet
            self.money.setText("Money: $%s"%(str(self.var_money)))
            self.win.setText("You Win!")

        elif sum(cardValue[1]) == sum(cardValue[0]):
            print("TIE")
            self.win.setText("Tie")

        elif (sum(cardValue[1]) >= (self.var_difficulty + 1) or sum(cardValue[1]) < sum(cardValue[0])) and not sum(cardValue[0]) >= (self.var_difficulty + 1):
            print("LOOSE")
            self.var_money -= self.var_bet
            self.money.setText("Money: $%s"%(str(self.var_money)))
            self.win.setText("Dealer Win!")

        elif (sum(cardValue[0]) >= (self.var_difficulty + 1) or sum(cardValue[1]) > sum(cardValue[0])) and not sum(cardValue[1]) >= (self.var_difficulty + 1):
            print("WIN")
            self.var_money += self.var_bet
            self.money.setText("Money: $%s"%(str(self.var_money)))
            self.win.setText("You Win!")

        self.win.setStyleSheet(("background-color: white;"))
        shuffle(cardDeck)
        drawnCards, cardValue, self.oneOrTwoCards, win, self.drawn=[[], []], [[], []], -1, 0, 0
        print("HERE", self.oneOrTwoCards)
        self.resize()
        self.play_test = 2
        self.enableBet()
        self.totalGamesCount += 1
        self.gameCount.setText("Total Games: %s"%(str(self.totalGamesCount))) 

    def enableBet(self):
        for i in range(0, len(self.btnB)):
            self.btnB[i].setEnabled(True)

    def restart(self):
        self.resize()
        self.play_test = 1
        self.win.setText("")
        self.dealer.setText("")
        self.player.setText("")
        self.empty()
        self.dealer.setStyleSheet(("background-color: transparent;"))
        self.player.setStyleSheet(("background-color: transparent;"))
        self.win.setStyleSheet(("background-color: transparent;"))
        self.hitMe()

    def reset(self):
        self.resize()
        self.play_test = 1
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

    def stand(self):
        self.btnA[0].setEnabled(False)
        self.resize()
        speed = 100
        while True:
            if sum(cardValue[0]) <= 16 and sum(cardValue[1]) != 0 and sum(cardValue[1]) <= (self.var_difficulty + 1):
                print(i)
                QTest.qWait(speed)
                self.cardDraw(1, 1, 0, "Dealer",1 , 490)
                speed+=200
            else:
                self.resize()
                self.play_test = 2
                self.enableBet()
                self.check()
                self.btnA[0].setEnabled(True)
                break

    def hitMe(self):
        for i in range(0, len(self.btnB)):
            self.btnB[i].setEnabled(False)
        print(self.oneOrTwoCards)

        if self.oneOrTwoCards < 0:
            print("This doesnt run when it is blackjack?")
            self.oneOrTwoCards = 0

        if self.oneOrTwoCards == 0:
            print("THIS DID RUN")
            self.btnA[1].setEnabled(True)
            self.cardDraw(2, 2, 1, "You", 0, 95)
            self.cardDraw(1, 1, 0, "Dealer", 1, 490)
            self.oneOrTwoCards += 1
            
        elif self.oneOrTwoCards > 0:
            self.cardDraw(1, 1, 1, "You", 0, 95)
        # MABY THIS += has something to do iwth it moved it inside if 
        self.var_money=round(self.var_money, 2)
        self.money.setText("Money: $%s"%(str(self.var_money)))

    def settingsUI(self, settingsUI):
        self.difficultyValue = self.var_difficulty
        self.moneyValue = self.var_money

        settingsUI.setObjectName("settingsUI")
        settingsUI.resize(400, 300)
        settingsUI.setFixedSize(settingsUI.width(), settingsUI.height())
        settingsUI.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.changeMoneyLabel = QLabel(settingsUI)
        self.changeMoneyLabel.setGeometry(20, 20, 111, 16)
        self.changeMoneyLabel.setObjectName("changeMoneyLabel")
        
        self.changeDifficultyLabel = QLabel(settingsUI)
        self.changeDifficultyLabel.setGeometry(20, 50, 101, 16)
        self.changeDifficultyLabel.setObjectName("changeDifficultyLabel")

        self.applyButton = QPushButton(settingsUI)
        self.applyButton.setGeometry(200, 260, 75, 23)
        self.applyButton.setObjectName("applyButton")
        self.applyButton.clicked.connect(lambda: self.settingsUpdate())

        self.exitButton = QPushButton(settingsUI)
        self.exitButton.setGeometry(290, 260, 75, 23)
        self.exitButton.setObjectName("exitButton")
        self.exitButton.clicked.connect(settingsUI.close)

        self.changePlayerMoneyLine = QLineEdit(settingsUI)
        self.changePlayerMoneyLine.setGeometry(140, 20, 113, 20)
        self.changePlayerMoneyLine.setObjectName("changePlayerMoneyLine")

        self.changeDifficultyLine = QLineEdit(settingsUI)
        self.changeDifficultyLine.setGeometry(140, 50, 113, 20)
        self.changeDifficultyLine.setObjectName("changeDifficultyLine")
        self.changeDifficultyLine.setReadOnly(True)

        self.difficultyStandard = QPushButton(settingsUI)
        self.difficultyStandard.setGeometry(30, 80, 75, 23)
        self.difficultyStandard.setObjectName("difficultyStandard")
        self.difficultyStandard.clicked.connect(lambda: self.difficultyChange(21))

        self.difficultyEasy = QPushButton(settingsUI)
        self.difficultyEasy.setGeometry(30, 110, 75, 23)
        self.difficultyEasy.setObjectName("difficultyEasy")
        self.difficultyEasy.clicked.connect(lambda: self.difficultyChange(30))

        self.difficultyHard = QPushButton(settingsUI)
        self.difficultyHard.setGeometry(30, 140, 75, 23)
        self.difficultyHard.setObjectName("difficultyHard")
        self.difficultyHard.clicked.connect(lambda: self.difficultyChange(16))

        self.currentStatusLabel = QLabel(settingsUI)
        self.currentStatusLabel.setGeometry(20, 200, 111, 16)
        self.currentStatusLabel.setObjectName("currentStatusLabel")

        self.playerMoneyStatus = QLabel(settingsUI)
        self.playerMoneyStatus.setGeometry(30, 220, 180, 16)
        self.playerMoneyStatus.setObjectName("playerMoneyStatus")

        self.blackjackDifficultyStatus = QLabel(settingsUI)
        self.blackjackDifficultyStatus.setGeometry(30, 240, 121, 16)
        self.blackjackDifficultyStatus.setObjectName("blackjackDifficultyStatus")

        self.retranslateUi(settingsUI)
        QtCore.QMetaObject.connectSlotsByName(settingsUI)

        self.changeDifficultyLine.setText("%d"%(self.difficultyValue))
        self.blackjackDifficultyStatus.setText("Blackjack difficulty = %d"%(self.var_difficulty))
        
        self.changePlayerMoneyLine.setText("%d"%(self.moneyValue))
        self.playerMoneyStatus.setText("Player Money = $%d"%(self.var_money))

    def difficultyChange(self, value):
        self.difficultyValue = value
        self.changeDifficultyLine.setText("%d"%(value))
        self.blackjackDifficultyStatus.setText("Blackjack difficulty = %d"%(value))

    def settingsUpdate(self):
        self.var_difficulty = self.difficultyValue
        self.var_money = int(self.changePlayerMoneyLine.text())
        self.money.setText("Money: $%s"%(str(self.var_money)))
        self.changePlayerMoneyLine.setText("%d"%(self.moneyValue))
        self.playerMoneyStatus.setText("Player Money = $%d"%(self.var_money))
        print(self.var_difficulty)
        print(self.var_money)
        self.confirmUser = QMessageBox()
        self.confirmUser.setWindowTitle("Confirm")
        self.confirmUser.setText("The changes has been made!")
        self.confirmUser.setIcon(QMessageBox.Information)
        self.confirmUser.exec_()


    def retranslateUi(self, settingsUI):
        _translate = QtCore.QCoreApplication.translate
        settingsUI.setWindowTitle(_translate("settingsUI", "Settings"))
        self.changeMoneyLabel.setText(_translate("settingsUI", "Change player money:"))
        self.changeDifficultyLabel.setText(_translate("settingsUI", "Change difficulty:"))
        self.applyButton.setText(_translate("settingsUI", "Apply"))
        self.exitButton.setText(_translate("settingsUI", "Exit"))
        self.difficultyStandard.setText(_translate("settingsUI", "Standard [21]"))
        self.difficultyEasy.setText(_translate("settingsUI", "Easy [30]"))
        self.difficultyHard.setText(_translate("settingsUI", "Hard [16]"))
        self.currentStatusLabel.setText(_translate("settingsUI", "Current status:"))
        self.playerMoneyStatus.setText(_translate("settingsUI", "Player Money = $"))
        self.blackjackDifficultyStatus.setText(_translate("settingsUI", "Blackjack difficulty = 21"))

drawnCards=[[], []]
cardValue=[[], []]
cardDeck=[]
ans=6
#Put in ans how many decks you want to play with

for a in range(0, ans):
    for j in ("Hearts", "Diamonds", "Spades", "Clubs"):
        for i in ("2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"):
            cardDeck.append("%s of %s"%(i, j))

shuffle(cardDeck)
win = 0
charlie=0

# COMBINE THESE TWO list called win eller dict
if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window()
    sys.exit(app.exec_())