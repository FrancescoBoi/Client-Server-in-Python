import socket
import sys
import random

sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

#Try connecting to the server
try:
    sock_fd.connect(("127.0.0.1", 8000))
    print("Connected")
except:
    print("Be sure the server is on")
    sys.exit()

#create the board
board = list()
while len(board)<15:
    num = random.randrange(1,91)
    while num in board:
        num = random.randrange(1,91)
    board.append(num)
board.sort()
print("The numbers of my board are")
print(board)    

#Ready to play
score = 0
while 1:
    #Wait for the next extracted number from the server
    msg_rec = sock_fd.recv(1024)
    if "FINISHED" in msg_rec:
        print(msg_rec)
        msg_sent = "ok going away" #just to send some text
        break
    elif int(msg_rec) in board:
        print("New number: " + msg_rec)
        score = score +1
        msg_sent = "I have this number" #just to send some text
    else:
        msg_sent = "NO LUCK" #just to send some text

    if (score ==15):
        print(board)
        msg_sent = "TOMBOLA" #this message makes the server stop the current game
        #break

    sock_fd.send(msg_sent)
sock_fd.send(msg_sent)
sock_fd.close()
del sock_fd
sys.exit()
