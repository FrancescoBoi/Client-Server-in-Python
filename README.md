# Client-Server-in-Python
These repository contains different example of client-server applications in Python. Each subfolder contains an example of client server application in Python. The three client-server applications are: **Chat random**, **Tombola** and **Tombola thread**. Each one contains two python files: the server file and the client.

## General launch of the program
Providing that the server file is named `server.py` and the client one is named `client.py`, first open a Terminal and launch the server with:
```
python server.py
```
Then open a new Terminal window (or tab) and launch the client with:
```
python client.py
```
The tombola client-server applications start the game only when 2 clients connect.

### Chat random application
The program creates a client-server chatroom. The clients initiate the connection and can ask the following commands:

- `L` lists all the clients connected to the server
- `ip:port msg` will send the msg to the client (passing by the server) identified by `ip:port`
 
Both server and clients use multithread programming. To launch the program:
### Launch the Chat random application
To launch the server open a Terminal window and do
```
server: python server.py
```
To launch the client open a new Terminal window or tab and do:

```
client: python client.py
```
You can create many clients by launching the same command many times on a different Terminal.
  
## Tombola application
This is a Tombola game in python using the server-client architecture. The server waits the connection of `MAX_NUM_CLIENT` clients. When `MAX_NUM_CLIENT` clients are connected, the game begins.
 
Each client has a board of 15 numbers. The server draws a number in the range of `[1, 90]` every `1` second and send this number to all the clients connected.
 
The first client that has all the 15 numbers drawn wins the game and send a message to the server to communicate the event. Then,the server informs all the clients that the game is over. The clients disconnect while the server stays on and waits for other clients to start a new game.

### Launch the client-server Tombola application
To launch the program, type the command
```
python tombolaServer.py
```

Then launch all the clients you want by opening each time a new Terminal with
```
python tombolaClient.py
```
  
## Tombola application with thread programming
This is a Tombola game in Python similar to the previous one but using thread programming. Each client has a board of 15 numbers. The server draws a number in the range of `[1, 90]` every `1` second and send this number to all the clients connected.
If another client connects when the game has already begun, the server will send all the numbers drawn hitherto and the client checks if all his 15 numbers have been drawn. 

The first client that has all the 15 numbers drawn wins the game and send a message to the server to communicate the event. The server informs all the clients that the game
 is over and in 1 minute another game will take place. All the clients can play again or exit. The client will use the same board.

### Solution adopted for the multithread Tombola program:
The server has the main thread which waits for clients to connect. Another thread is created for the number drawing. When a client connects a new thread is created which is used to receive from the optional message `tombola` from the clients.

Two ports are used: one for sending the numbers from the server to the client and to inform the clients someone made tombola and another port is used by the winner to communicate to the server that he made tombola.

### Launch the multithread version of the client-server Tombola application
Open a terminal window and launch the server with the command

```python tombolaThreadServer.py```

Then launch all the clients you want by opening each time a new terminal and typing the command:
```
python tombolaThreadClient.py
```
