The program creates a client-server chatroom. The clients initiates the connection and can ask the following commands:
- 'L' lists all the clients connected to the server
- ip:port msg will send the msg to the client (passing by the server) identified by ip:port

Both server and clients use multithread programming.
To launch the program:
- server: python server.py
- client: python client.py

You can create many clients by launchin the same command many times.
