#3) Creare una chat client-server. Il client si collega e chiede al server i
#seguenti comandi: 'L': il server manda la lista dei client connessi
#'ip:port msg': il client spedisce il messaggio msg al server che lo manda al
#client ip:port. In questo caso i thread vanno gestiti sia dal server che dal
# client che dovra' averne uno per ricevere i messaggi e uno (anche il main) per mandarli


import socket
from threading import Thread
from SocketServer import ThreadingMixIn
import signal
import sys

EXIT = False
address = []
address2 = []

# handler per il comando Ctrl+C
def sig_handler(signum, frame):
    if (signum == 2):
        print("Called SIGINT")
        EXIT = True

signal.signal(signal.SIGINT, sig_handler) # setto l'handler per i segnali


# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):

    def __init__(self,conn,ip,port):
        Thread.__init__(self)
        self.conn = conn
        self.ip = ip
        self.port = port
        print "[+] New server socket thread started for " + ip + ":" + str(port)

    def run(self):
        while True:
            data = self.conn.recv(1024)
            print "Server received data:", data
            if (data=='L'):
                print "QUI",address2
                tosend = ""
                for i in address2:
                    tosend = tosend + "ip:"+str(i[0]) + "port:"+str(i[1])+"\n"
                self.conn.send(tosend)
                #mandare elenco client connessi
            else:
                print "QUA"
                #manda ip:port msg
                st = data.split(" ")
                msg = st[1:]
                msg = ' '.join(msg)
                print "MSG DA INVIARE:",msg
                ipport = st[0].split(":")
                ip = ipport[0]
                port = ipport[1]
                flag = False
                print "Address2:",address2
                print "ip:",ip
                print "port:",port
                for i in address2:
                    print i[0],ip,type(i[0]),type(ip),i[1],type(i[1]),port,type(port)
                    if str(i[0])==str(ip) and str(i[1])==str(port):
                        i[2].send(msg)
                        self.conn.send("msg inviato")
                        flag = True
                        break
                if flag == False:
                    self.conn.send("client non esistente")


if __name__ == '__main__':
    # Multithreaded Python server : TCP Server Socket Program Stub
    TCP_IP = '127.0.0.1'
    TCP_PORT = 2004
    TCP_PORTB = 2005
    BUFFER_SIZE = 1024  # Usually 1024, but we need quick response

    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServer.bind((TCP_IP, TCP_PORT))

    tcpServerB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServerB.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServerB.bind((TCP_IP, TCP_PORTB))
    threads = []

    tcpServer.listen(4)
    tcpServerB.listen(4)

    while True:
        print "Multithreaded Python server : Waiting for connections from TCP clients..."
        (conn, (ip,port)) = tcpServer.accept()
        address.append((ip,port,conn))

        (conn2, (ip2,port2)) = tcpServerB.accept()
        address2.append((ip2,port2,conn2))

        newthread = ClientThread(conn,ip,port)
        newthread.start()
        threads.append(newthread)
        if EXIT==True:
            break

    print "SERVER EXIT"

    for t in threads:
        t.join()
