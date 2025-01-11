from abc import ABC, abstractmethod
from time import sleep
import os
import random
#Board
class BoardGame:
    def __init__(self):
        self.reset(self)
        return self
    
    def show():
        os.system('cls')
        border = f"{'╼'*23:^25}"
        print(border)
        print(f" ○{'► OTHELLO ◄':^21}○")
        print(border)
        for i in Board().board:
            print(" │",i,end = " │ ")
            for j in Board().board[i]:
                print(j, end = " ")
            print("│")
            if i == " ":
                print(border)
        print(border)

    def reset(self):
        self.board = {" ": [1,2,3,4,5,6,7,8]} #Use dictionary to draw board
        for i in range (65,73): #Key is denoted with Decimal -> ASCII character
            self.board[chr(i)] = ["+" for i in range(8)]
        self.board["D"][3] = "X" #Black is denoted as X
        self.board["D"][4] = "O" #White is denoted as O
        self.board["E"][3] = "O" 
        self.board["E"][4] = "X"
                
class Board(BoardGame): #Singleton
    _singletonInstance = None
    def __new__(cls):
        if cls._singletonInstance == None:
            cls._singletonInstance = super().__init__(BoardGame)
        return cls._singletonInstance

#End of Board
    
#Count the chips at the end
class CountChips:
    def count(self):
        counts = {"X":0,"O":0}
        for key in Board().board:
            for chips in Board().board[key]:
                if chips == "X":
                    counts["X"] += 1
                elif chips == "O":
                    counts["O"] += 1
        return counts
#End of count chips
    
#Validity Checks : Return an array of location if a moves is possible, return False if found "+" or empty space which means it's not possible to place.
class Validity: #Template Pattern
    @abstractmethod
    def is_valid(self) -> bool:
        pass

class ValidBlack(Validity): #Black is denoted as X
    def is_valid(self, location, step, visitedLoc = []):
        visitedLoc += [location]                            # Return True when the outer ring had Black chip, 
        x, y = location[0], location[1]                     # ex. current Board : || (X) O O O X ||  NB : (X) means you want to place it there, so it check to the East;
        x1 = ord(x)                                         # check to the East O -> O -> O -> X then return True
        step_x, step_y = step[0], step[1]
        if (chr(x1+step_x) not in Board().board) or (y + step_y < 0) or(y + step_y > 7):
            return None
        if Board().board[chr(x1+step_x)][y+step_y] == "O":
            return self.is_valid([chr(x1+step_x),y+step_y],step, visitedLoc)
        elif Board().board[chr(x1+step_x)][y+step_y] == "X":
            return visitedLoc
        elif Board().board[chr(x1+step_x)][y+step_y] == "+":
            return False

class ValidWhite(Validity): #White is denoted as O   
    def is_valid(self, location, step, visitedLoc):    # Return True when the outer ring had White chip,
        visitedLoc += [location]                            # ex. current Board : || (X) O O O X ||  NB : (X) means you want to place it there, so it check to the East;
        x, y = location[0], location[1]                     # check to the East O -> O -> O -> X then return True
        x1 = ord(x)                                         
        step_x, step_y = step[0], step[1]
        if (chr(x1+step_x) not in Board().board) or (y + step_y < 0) or(y + step_y > 7):
            return None 
        if Board().board[chr(x1+step_x)][y+step_y] == "X":
            return self.is_valid([chr(x1+step_x),y+step_y],step,visitedLoc)
        elif Board().board[chr(x1+step_x)][y+step_y] == "O":
            return visitedLoc
        elif Board().board[chr(x1+step_x)][y+step_y] == "+":
            return False 

#End of Validity Checks
    
#Check Direction : Return all the location that need to be change according to the chip.
class DirectionCheck(ABC):
    @abstractmethod
    def check(self, location):
        pass

class D_Check_Black(DirectionCheck):
    def check(self, location):
        x, y = location[0], location[1] #X => A ; Y => 2 (Coordinate)
        x1 = ord(x) #X1 => A -> 65 (Decimal code of A)
        arrayDirection = [1, 0, -1] #To determine the direction
        v = ValidBlack()
        if x not in Board().board:
            raise ValueError("Letter coordinate is not in the board.")
        if y < 0 or y > 7:
            raise ValueError("Number coordinate is not in the board.")
        if Board().board[x][y] != "+":
            raise ValueError("Unable to place chip, coordinate is filled with chip.")
        validatedFlag = False
        for i in arrayDirection: #Determine the first coordinate, -1 : North ;; 0 : West , East ;; +1 : South || Since A is the upper level, and H is the lower level, so increment means going down 
            for j in arrayDirection: #Determine the second coordinate, -1 : West ;; 0: South, North ;; +1 : East || If it's i := -1, and j := -1 then it's South West || i := 1 and j := 0 then it's South
                if [chr(x1+i),y+j] == [x, y]: #If the coordinate is the same with current selected coordinate
                    continue
                if (chr(x1+i) not in Board().board) or (y + j < 0) or (y + j > 7): #If goes beyond the range of the board [A ~ H] and [0 ~ 7]
                    continue
                if Board().board[chr(x1+i)][y+j] == "O": #If next coordinate (West, Northwest, North, Northeast, East, Southeast, South, Southwest) 8 direction is White colored
                    checkValid = v.is_valid([chr(x1+i), y+j], [i,j], [])
                    if(checkValid): #If is_possible function return True, which mean the direction we're heading to had a Black chip on the outer rings.
                        if (not validatedFlag):
                            validatedFlag = checkValid
                        else:
                            validatedFlag += checkValid
        if (validatedFlag):
            return validatedFlag
        else:
            raise ValueError("Unable to place chip that has no X's end.")
                            

class D_Check_White(DirectionCheck):
    def check(self, location):
        x, y = location[0], location[1] #X => A ; Y => 2 (Coordinate)
        x1 = ord(x) #X1 => A -> 65 (Decimal code of A)
        arrayDirection = [1, 0, -1] #To determine the direction
        v = ValidWhite()
        if x not in Board().board:
            raise ValueError("Letter coordinate is not in the board.")
        if y < 0 or y > 7:
            raise ValueError("Number coordinate is not in the board.")
        if Board().board[x][y] != "+":
            raise ValueError("Unable to place chip, coordinate is filled with chip.")
        validatedFlag = False
        for i in arrayDirection: #Determine the first coordinate, -1 : North ;; 0 : West , East ;; +1 : South || Since A is the upper level, and H is the lower level, so increment means going down 
            for j in arrayDirection: #Determine the second coordinate, -1 : West ;; 0: South, North ;; +1 : East || If it's i := -1, and j := -1 then it's South West || i := 1 and j := 0 then it's South
                if [chr(x1+i),y+j] == [x, y]: #If the coordinate is the same with current selected coordinate
                    continue
                if (chr(x1+i) not in Board().board) or (y + j < 0) or (y + j > 7): #If goes beyond the range of the board [A ~ H] and [0 ~ 7]
                    continue
                if Board().board[chr(x1+i)][y+j] == "X": #If next coordinate (West, Northwest, North, Northeast, East, Southeast, South, Southwest) 8 direction is Black colored
                    checkValid = v.is_valid([chr(x1+i), y+j], [i,j], [])
                    if(checkValid): #If is_possible function return True, which mean the direction we're heading to had a White chip on the outer rings.
                        if (not validatedFlag):
                            validatedFlag = checkValid
                        else:
                            validatedFlag += checkValid
        if (validatedFlag):
            return validatedFlag
        else:
            raise ValueError("Unable to place chip that has no O's end.")
# End of Direction Checks

# Possibilities Checks : If there's no possible move, then return False.
class CheckPossiblity(ABC):
    @abstractmethod
    def is_possible(self, location):
        pass

class P_Check_Black(CheckPossiblity): #To check whether black had a possible moves.
    def is_possible(self, location):
        x, y = location[0], location[1]
        x1 = ord(x)
        arrayDirection = [1, 0, -1]
        v = ValidBlack()
        validatedFlag = False
        for i in arrayDirection:  
            for j in arrayDirection: 
                if [chr(x1+i),y+j] == [x, y]: 
                    continue
                if (chr(x1+i) not in Board().board) or (y + j < 0) or (y + j > 7): 
                    continue
                if Board().board[chr(x1+i)][y+j] == "O": 
                    checkValid = v.is_valid([chr(x1+i), y+j], [i,j], [])
                    if(not checkValid) and (checkValid != None): #If valid return False, it means there are "+" empty space that could be filled with "X"
                        return True
        return False

class P_Check_White(CheckPossiblity): #To check whether white had a possible moves.
    def is_possible(self, location):
        x, y = location[0], location[1]
        x1 = ord(x)
        arrayDirection = [1, 0, -1]
        v = ValidWhite()
        validatedFlag = False
        for i in arrayDirection:  
            for j in arrayDirection: 
                if [chr(x1+i),y+j] == [x, y]: 
                    continue
                if (chr(x1+i) not in Board().board) or (y + j < 0) or (y + j > 7): 
                    continue
                if Board().board[chr(x1+i)][y+j] == "X": 
                    checkValid = v.is_valid([chr(x1+i), y+j], [i,j], [])
                    if(not checkValid) and (checkValid != None): #If valid return False, it means there are "+" empty space that could be filled with "O"
                        return True
        return False
#End of Possibilities Checks

class BoardPossibilityChecks(ABC):
    @abstractmethod
    def checksPossibility(self):
        pass

class B_Possible_Checks(BoardPossibilityChecks):
    def checksPossibility(self):
        BCheck = P_Check_Black()
        for key in Board().board:
            index = 0
            for loc in Board().board[key]:
                if loc == "X":
                    if(BCheck.is_possible([key, index])):
                        return True
                index += 1
        return False

class W_Possible_Checks(BoardPossibilityChecks):
    def checksPossibility(self):
        BCheck = P_Check_White()
        for key in Board().board:
            index = 0
            for loc in Board().board[key]:
                if loc == "O":
                    if(BCheck.is_possible([key, index])):
                        return True
                index += 1
        return False


#Chips : The player denoter
class Chip(ABC):
    @abstractmethod
    def place_chip(self):
        pass

class BlackChip(Chip):
    def place_chip(self, *args):
        BMove = D_Check_Black()
        x, y = args[0], args[1]-1
        checks = BMove.check([x,y])
        if (checks):
            Board().board[x][y] = "X"
            Board().show()
            for loc in checks:
                sleep(0.1)
                newX, newY = loc[0], loc[1]
                Board().board[newX][newY] = "X"
                Board().show()
            return True
        else:
            return False
        
class WhiteChip(Chip):
    def place_chip(self, *args):
        WMove = D_Check_White()
        x, y = args[0], args[1]-1
        checks = WMove.check([x,y])
        if (checks):
            Board().board[x][y] = "O"
            Board().show()
            for loc in checks:
                sleep(0.1)
                newX, newY = loc[0], loc[1]
                Board().board[newX][newY] = "O"
                Board().show()
            return True
        else:
            return False
#End of Chips



def startNotice():
    time = [0.025 , 0.03 , 0.045, 0.05 , 0.6, 0.65, 0.7 , 0.08 , 0.09 , 0.1 , 0.2 , 0.28 , 0.3 ]
    dotString = "LOADING CHIPS..."
    loadingString = ""
    for _ in range(1,21):
        os.system('cls')
        print("\n"*4)
        print(f"{dotString:^70}",flush=True)
        percent = f"{int(_/20*100)}%"
        print(f"{f'{percent:^5}':>25}|",end ="",flush=True)
        loadingString += "■"
        print(loadingString,end="",flush=True)
        if _ % 20 == 0:
            sleep(1)
        if _ % 19 == 0:
            dotString = "WELCOME TO OTHELLO!"
        elif _ % 16 == 0:
            dotString = "LOADING RULES..."
        elif _ % 12 == 0:
            dotString = "LOADING SCOREBOARD..."
        elif _ % 8 == 0:
            dotString = "LOADING BOARD..."
        elif _ % 4 == 0:
            dotString = "LOADING CONTROLS..."
        print("")
        sleep(random.choice(time))
    print("")
    os.system('cls')
    print(f"{'='*10} Game Tutorial {'='*10}")
    print("1. Othello is a board game, consisting 2 player, and 8 x 8 square board.")
    print("2. The two player are denoted as X and O")
    print("3. It is only possible to place a chip (in this case X and Y)")
    print("   if there are at least one straight occupied line between the")
    print("   currently placed chip, and another chip with one or more")
    print("   contiguous enemy pieces between the two player chips.")
    print("4. After placing such chip, all the contiguous enemy pieces will be flipped")
    print("   resulting in player owning their chip, this can be done vice versa.")
    print("5. The condition of winning are the player who had the most chip on the board.")
    print(f"{'='*35}")
    print("Done reading?")
    os.system('PAUSE')

def main():
    B = BlackChip()
    W = WhiteChip()
    B_PosTurn = B_Possible_Checks()
    W_PosTurn = W_Possible_Checks()
    Counter = CountChips()
    ForfeitHandler = {"X":False, "O":False}
    takeTurn = 0
    while True:
        Board().show()
        if (not(W_PosTurn.checksPossibility()) and not(B_PosTurn.checksPossibility())) or (ForfeitHandler["X"] == True and ForfeitHandler["O"] == True):
            print("Game Ends")
            print("Counting the result",end="")
            for _ in range(3): print(".",end = "",flush = True), sleep(random.choice([0.2,0.3,0.5]))
            print("")
            counted = Counter.count()
            print(f"{'╼'*23:^25}")
            x, o = counted['X'], counted['O']
            print(f" │{f'X : {x}   |   O : {o}':^21}│")
            print(f"{'╼'*23:^25}")
            if counted['X'] > counted['O'] : print(f" │{'X WINS':^21}│")
            elif counted['X'] < counted['O'] : print(f" │{'O WINS':^21}│")
            else: print(f" │{'GAME IS DRAW':^21}│")
            print(f"{'╼'*23:^25}")
            os.system('pause')
            os.system('cls')
            Board().reset(BoardGame)
            main()
            break
        if (takeTurn):
            if (W_PosTurn.checksPossibility()): #If White got possible turn
                try:
                    if ForfeitHandler["X"] == True:
                        ask = input("X has forfeited, do you also want to forfeit? [Y | N]\n").upper()
                        if ask == "Y":
                            print("O has also forfeited, ending the game...")
                            ForfeitHandler["O"] = True
                            os.system('pause')
                            continue
                        elif ask == "N":
                            print("X hasn't forfeited, continuing the game...")
                            ForfeitHandler["X"] = False
                            takeTurn = 0
                            os.system('pause')
                            continue
                        else:
                            continue
                    
                    x,y = list(input("O's Turn : ").split())
                    if x.upper() == "Z" and int(y) == 0:
                        ask = input("Are you sure you want to forfeit O? [Y | N]\n").upper()
                        if ask == "Y":
                            ForfeitHandler["O"] = True
                            takeTurn = 0
                            continue
                        else:
                            continue
                    W.place_chip(x.upper(),int(y))
                    takeTurn = 0
                except Exception as error:
                    print(error)
                    os.system('pause')
            else:
                print("No Possible Turn for O's.")
                os.system('pause')
                takeTurn = 0
            
        else:
            if (B_PosTurn.checksPossibility()): #If Black got possible turn
                try:
                    if ForfeitHandler["O"] == True:
                        ask = input("O has forfeited, do you also want to forfeit? [Y | N]\n").upper()
                        if ask == "Y":
                            print("X has also forfeited, ending the game...")
                            ForfeitHandler["X"] = True
                            os.system('pause')
                            continue
                        elif ask == "N":
                            print("X hasn't forfeited, continuing the game...")
                            ForfeitHandler["O"] = False
                            takeTurn = 1
                            os.system('pause')
                            continue
                        else:
                            continue

                    x,y = list(input("X's Turn : ").split())

                    if x.upper() == "Z" and int(y) == 0:
                        ask = input("Are you sure you want to forfeit X? [Y | N]\n").upper()
                        if ask == "Y":
                            ForfeitHandler["X"] = True
                            takeTurn = 1
                            continue
                        else:
                            continue
                    B.place_chip(x.upper(),int(y))
                    takeTurn = 1
                except Exception as error:
                    print(error)
                    os.system('pause')
            else:
                print("No Possible Turn for X's.")
                os.system('pause')
                takeTurn = 1

if __name__ == "__main__":
    string = "PyOTHELLO by Aswin, Samuel, Giovanny (ASamNy Othello)"
    print(f"",end="")
    for _ in range(4):
        os.system('cls')
        print("""      ■■■■■■■■■■■■             ■■■■■■             ┃              ┃  ┃
      ┃           ┃           ┃      ┃     ┃      ┃              ┃  ┃
      ┃           ┃ ┃     ┃   ┃      ┃     ┃      ┃       ■■■■   ┃  ┃
      ■■■■■■■■■■■■   ■■■■■┃   ┃      ┃  ■■■┃■■■   ┃■■■■  ┃    ┃  ┃  ┃   ■■■■
      ┃                   ┃   ┃      ┃     ┃      ┃    ┃ ┃■■■■   ┃  ┃  ┃    ┃
      ┃             ┃     ┃   ┃      ┃     ┃   ┃  ┃    ┃ ┃       ┃  ┃  ┃    ┃
      ┃              ■■■■■     ■■■■■■       ■■■   ┃    ┃  ■■■■   ┃  ┃   ■■■■\n\n""")
        print(f"{string:^70}\n",end = "",flush = True)
        string += "."
        sleep(random.choice([0.2,0.3,0.5]))
    print("")
    sleep(2)
    startNotice()
    main()



'''
B.place_chip("F",4)
W.place_chip("D",3)
B.place_chip("C",3)
W.place_chip("F",5)
B.place_chip("F",6)
W.place_chip("G",4)
B.place_chip("E",3)
W.place_chip("C",4)
B.place_chip("D",6)
W.place_chip("E",2)
B.place_chip("F",3)
W.place_chip("E",6)
B.place_chip("D",1)
W.place_chip("F",2)
B.place_chip("F",1)
W.place_chip("C",2)
B.place_chip("E",7)
W.place_chip("G",5)
B.place_chip("H",5)
W.place_chip("G",3)
B.place_chip("H",4)
W.place_chip("H",3)
B.place_chip("H",2)
W.place_chip("G",2)

'''
''' List index out of range test
B.place_chip("F",4)
W.place_chip("D",3)
B.place_chip("C",3)
W.place_chip("F",5)
B.place_chip("F",6)
W.place_chip("G",4)
B.place_chip("E",3)
W.place_chip("C",4)
B.place_chip("D",6)
W.place_chip("E",2)
B.place_chip("F",3)
W.place_chip("E",6)
B.place_chip("D",1)
W.place_chip("F",2)
B.place_chip("F",1)
W.place_chip("C",2)
B.place_chip("E",7)
W.place_chip("G",5)
B.place_chip("H",5)
W.place_chip("G",3)
B.place_chip("H",4)
W.place_chip("H",3)
B.place_chip("H",2)
W.place_chip("G",2)
'''

'''
Left H1 alone
B.place_chip("C",5)
W.place_chip("C",6)
B.place_chip("D",6)
W.place_chip("C",4)
B.place_chip("C",3)
W.place_chip("E",6)
B.place_chip("C",7)
W.place_chip("B",8)
B.place_chip("D",7)
W.place_chip("E",7)
B.place_chip("F",8)
W.place_chip("C",2)
B.place_chip("E",3)
W.place_chip("D",3)
B.place_chip("B",3)
W.place_chip("B",4)
B.place_chip("A",5)
W.place_chip("F",7)
B.place_chip("G",8)
W.place_chip("F",6)
B.place_chip("B",7)
W.place_chip("B",2)
B.place_chip("G",6)
W.place_chip("G",7)
B.place_chip("C",1)
W.place_chip("A",7)
B.place_chip("A",1)
W.place_chip("E",2)
B.place_chip("H",8)
W.place_chip("A",2)
B.place_chip("A",3)
W.place_chip("A",4)
B.place_chip("A",8)
W.place_chip("D",2)
B.place_chip("F",2)
W.place_chip("E",1)
B.place_chip("F",3)
W.place_chip("G",4)
B.place_chip("F",4)
W.place_chip("D",1)
B.place_chip("F",1)
W.place_chip("B",1)
B.place_chip("B",5)
W.place_chip("B",6)
B.place_chip("A",6)
W.place_chip("H",7)
B.place_chip("H",4)
W.place_chip("F",5)
B.place_chip("G",5)
W.place_chip("H",5)
B.place_chip("E",8)
W.place_chip("G",3)
B.place_chip("D",8)
W.place_chip("H",3)
B.place_chip("G",2)
W.place_chip("C",8)
B.place_chip("H",6)
W.place_chip("G",1)
B.place_chip("H",2)

Board().show()

'''
