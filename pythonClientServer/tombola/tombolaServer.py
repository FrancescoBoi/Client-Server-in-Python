import socket
import random
from time import sleep

sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
sock_fd.bind(("127.0.0.1", 8000))
sock_fd.listen(1)
MAX_NUM_CLIENT = 2

client_list =list()
tombola = list()
while 1:
    #Wait for clients to connect
    print("Waiting for other " + str(MAX_NUM_CLIENT - len(client_list)) + " players")
    client_sock, client_addr = sock_fd.accept()
    print("Another client connected")
    client_list.append((client_sock, client_addr))
    # If there are enough clients the game starts:    
    if (len(client_list)==MAX_NUM_CLIENT):
        print("Game begins")
        tombola = list()
        while 1 and len(tombola)<90:
            winners_list = list()
            num = random.randrange(1,91)
            sleep(1) #some delay between 2 extractions
            #print(num, tombola)
            #If number already in the board:            
            while num in tombola:
                num = random.randrange(1,91)
            tombola.append(num)
            tombola.sort()
            print("New number: " + str(num)) 
#           print("Messaggi dei giocatori: \n")
            #send the number to every player            
            for el in  client_list:
                el[0].send(str(num))
                msg = el[0].recv(1024)
                #if somebody won he sent the message "TOMBOLA":                
                if msg == "TOMBOLA":
                    winners_list.append(el)
                    print("somebody won")
                    print(el[1][0] + " says: "+msg)
            #unlikely but there may be more than one winner            
            if (len(winners_list)>0):
                print("Winners list: " + str(len(winners_list)))
                print(winners_list)

                print(tombola)
                if (len(winners_list))==1:
                    toSend = "FINISHED, PLAYER " + winners_list[0][1][0] + " : " + str(winners_list[0][1][1]) + " WON"
                else:
                    toSend = "FINISHED, THE FOLLOWING PLAYERS WON "
                    for el in winners_list:
                        toSend = toSend + el[1][0] + " : "+ el[1][1] + "\n"
                for el in client_list:
                    if el not in winners_list:
                        el[0].send(toSend)
                    else:
                        el[0].send("FINISHED: YOU WON")
                    el[0].close()

                del winners_list, tombola
                client_list = list()
                break
        msg =raw_input("Another game?[y/n]")
        if msg =="n":
            break
del sock_fd
