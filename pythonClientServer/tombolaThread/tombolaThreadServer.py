import socket 
#from threading import Thread 
import threading
from SocketServer import ThreadingMixIn 
import signal
import sys
import time
import random

EXIT = False
num_clients = list()
tombola_clients = list()
import pdb

# handler per il comando Ctrl+C
def sig_handler(signum, frame):
    if (signum == 1):
        print("Called SIGINT")
        EXIT = True

signal.signal(signal.SIGINT, sig_handler) # setto l'handler per i segnali


# Multithreaded Python server : TCP Server Socket Thread Pool
class DrawingThread(threading.Thread): 
 
    def __init__(self, lock, lock2): 
        threading.Thread.__init__(self)
        self.tombola = list()
        self.victoryLock = lock
        self.clientsLock = lock2
    
    def run(self): 
        global num_clients
        print("Drawing started")
        sleep_amount = 0
        while True:
            time.sleep(sleep_amount)#before lock it blocks the client
            self.victoryLock.acquire()
            self.clientsLock.acquire()
            
            if sleep_amount>0:
                ClientThread.victory = False
                sleep_amount = 0
            if ClientThread.victory or len(self.tombola)==90:
                sleep_amount = 60
                print(ClientThread.winner)
                for el in num_clients:
                    el[2].send("TOMBOLA")
                    print("Client informed")
                self.tombola.sort()
                print("Drawn numbers: \n" + str(self.tombola))
                self.tombola = list()
                print("\n\n--------NEW GAME STARTING IN 60 SECONDS------")
            
            else:            
                time.sleep(1)
                val = random.randint(1,91)
                while val in self.tombola:
                    val = random.randint(1,91)
                print (str(val))
                self.tombola.append(val)
                
                for el in num_clients:
                    el[2].send(str(val))
            self.clientsLock.release()
            self.victoryLock.release()
               
    def getTombola(self):
        return self.tombola[:]


class ClientThread(threading.Thread): 
    victory = False
    winner = None #same lock for victory and 
    def __init__(self, conn_rec, ip_rec, port_rec, send_conn, lock, lock2): 
        threading.Thread.__init__(self)
        self.myIp = ip_rec
        self.myPort = port_rec
        self.myConn = conn_rec
        self.victoryLock = lock
        self.clientsLock = lock2
        self.sendEl = send_conn #to eliminate it from num_clients
      
    
    def run(self):
        global num_clients
        while True: 
            while True:
                msg = self.myConn.recv(1024)
                self.victoryLock.acquire()
                print("Messaggio dal cliente: " + msg)
                #if another client wins:
                if ClientThread.victory == True:
                    self.victoryLock.release()
                    break
                #if this client wins:
                if msg == "TOMBOLA":
                    print("-----------A CLIENT WON-----------")
                    ClientThread.victory = True
                    ClientThread.winner = (self.myIp, self.myPort,self.myConn)
                    self.victoryLock.release()
                    msg = self.myConn.recv(1024)
                    break
                self.victoryLock.release()
            print("Waiting for clients reply for the new game")
            
            print("Does the client play again? " + msg)
            self.clientsLock.acquire()
            if msg.lower() != "yes":
                self.myConn.send("goodbye")
                num_clients.remove(self.sendEl)
                self.clientsLock.release()
                break
            self.clientsLock.release() 
        print("client disconnected")

if __name__ == '__main__':
    # Multithreaded Python server : TCP Server Socket Program Stub
    TCP_IP = '127.0.0.1'
    #define 2 ports
    num_port = 2004 #port for sending the numbers
    tombola_port = 2005 #port for sending the TOMBOLA MESSAGFE
    BUFFER_SIZE = 1024  # Usually 1024, but we need quick response 
 
    num_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    num_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    num_sock.bind((TCP_IP, num_port)) 

    tombola_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    tombola_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    tombola_sock.bind((TCP_IP, tombola_port)) 
    threads = [] 
 
    num_sock.listen(4) 
    tombola_sock.listen(4)
    #Lancio l'estrazione     
    lock = threading.Lock()    
    lock2 = threading.Lock()
    drawing = DrawingThread(lock, lock2)
    drawing.start()
    
    while True:
         
        print "Multithreaded Python server : Waiting for connections from TCP clients..." 
        print("Waiting for the 1st connection")
        (conn, (ip,port)) = num_sock.accept() 
        print("Connessione 1 accettata")
        lock2.acquire()
        num_clients.append((ip,port,conn))
        lock2.release()
        print("Waiting fo 2nd connection")
        (conn2, (ip2,port2)) = tombola_sock.accept() 
        #tombola_clients.append((ip2,port2,conn2))
        print("Waiting for the 2nd connection")
        #non appena si connette devo mandargli un messaggio con INIZIO oppure la lista dei
        #estratti fino ad ora:
        msg = ""
        if len(drawing.getTombola())>0:
            
            for el in drawing.getTombola():
                msg = msg + " " +  str(el)
            msg = msg[1:]
        else:
            msg = "BEGIN"
        conn.send(msg)
        #1 thread for each client  
        newthread = ClientThread(conn2, ip2, port2, ( ip, port, conn),  lock, lock2) 
        newthread.start() 
        threads.append(newthread) 
        if EXIT==True:
            break

    print "SERVER EXIT" 
    drawing.join()
    for t in threads: 
        t.join() 


