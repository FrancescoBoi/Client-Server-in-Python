# Python TCP Client A
import socket
import random 
from threading import Thread
import sys
import pdb

#GLOBAL VARIABLES
host = socket.gethostname() 
print "host:",host

def createBoard():
    loc_board = list()
    while len(loc_board)<15:
        num = random.randrange(1,91)
        while num in loc_board:
            num = random.randrange(1,91)
        loc_board.append(num)
    loc_board.sort()
    print(loc_board)
    return loc_board[:]

def askToContinue():
    global tombola_sock, scheda
    res = False
    temp =""
    #pdb.set_trace()
    while temp.lower() != "yes" and temp.lower() != "no":
        temp = raw_input("New game starting in 60 seconds: do you want to play?(yes/no)\n")
    print("'" + temp +"' " + "sending to server")
    tombola_sock.send(temp)
    if temp == "yes":
        #uncomment to create a new board for the new game
        #board = createBoard()
        res = True
    return res    
    
#create the board
board = createBoard() 

score = 0

#define 2 ports
num_port = 2004
tombola_port = 2005

#buffer for receiver
BUFFER_SIZE = 1024

#END GLOBAL VARIABLES

#FUNC DEFINITION
num_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tombola_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

MAX_SCORE = 15

def checkScore(myval):
    global score, board, tombola_sock
    res = True
    if myval in board:
        score = score + 1
        print ("New score: " + str(score))
        if score == MAX_SCORE:
            tombola_sock.send("TOMBOLA")
            dummy = ""

            print("---------YOU WIN--------------")
            print("Your board is:\n "+ str(board))
            res = askToContinue()
            #if the client wants to play again
            if res:
                while "TOMBOLA" not in dummy:
                    # Server will sendo the message also to the winner
                    print("Waiting for the server message tombola: " + dummy)
                    dummy = num_sock.recv(BUFFER_SIZE) 
                score = 0
                
            return res
    return True

try:
    print("Trying to connect")
    num_sock.connect(('127.0.0.1', num_port))#2004
    tombola_sock.connect(('127.0.0.1', tombola_port))#2005
    print("connected")
except:
    print("Be sure server is on")
    sys.exit()

continua = True
while(continua):
    
    data = num_sock.recv(BUFFER_SIZE)
    try:
        val = int(data)
        print(data)
        continua = checkScore(val)
    except:
        if "TOMBOLA" in data:
            print("\n----------YOU LOSE----------")
            print("Your board is:\n "+ str(board))
            continua = askToContinue()
            if continua:
                score = 0
            else:
                break
        elif data=="BEGIN":
            print(data)
        else:
            nums = data.split()
            for el in nums:
                continua = checkScore(int(el))
            print(score)
print(str(score) + " == " + str(MAX_SCORE)) 
final_mess = ""
while final_mess.lower() != "Goodbye":
    final_mess = tombola_sock.recv(1024)
num_sock.close()
tombola_sock.close() 


