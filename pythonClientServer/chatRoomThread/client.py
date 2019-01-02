#3) Creare una chat client-server. Il client si collega e chiede al server i seguenti comandi:
#'L': il server manda la lista dei client connessi
#'ip:port msg': il client spedisce il messaggio msg al server che lo manda al client ip:port
#In questo caso i thread vanno gestiti sia dal server che dal client che dovra'
# averne uno per ricevere i messaggi e uno (anche il main) per mandarli


# Python TCP Client A
import socket
import random #importo la libreria per i numeri casuali
from threading import Thread

class ClientThread(Thread):

    def __init__(self,conn):
        Thread.__init__(self)
        self.conn = conn

    def run(self):
        while True:
            data = self.conn.recv(1024)
            print "Ricevuto msg:",data

host = socket.gethostname()
print "host:",host
port = 2004
portB = 2005
BUFFER_SIZE = 2000

tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientA.connect(('127.0.0.1', port))
tcpClientB.connect(('127.0.0.1', portB))

newthread = ClientThread(tcpClientB)
newthread.start()


while(True):
    msg = raw_input("Inserisci comando: ")
    tcpClientA.send (msg)
    data = tcpClientA.recv(BUFFER_SIZE)
    print "data received:",data

tcpClientA.close()
