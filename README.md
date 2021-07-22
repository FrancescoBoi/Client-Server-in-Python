# Client-Server-in-Python
Each subfolder contains the python code for the client and the server. The three client-server applications are: CHATROOM THREAD, TOMBOLA and TOMBOLA THREAD

- CHATROOM THREAD
  The program creates a client-server chatroom. The clients initiates the connection and can ask the following commands:

  'L' lists all the clients connected to the server
  ip:port msg will send the msg to the client (passing by the server) identified by ip:port
  Both server and clients use multithread programming. To launch the program:

  server: python server.py
  client: python client.py
  You can create many clients by launchin the same command many times.
  
- TOMBOLA
  This is a Tombola game in python using the server-client architecture. The server waits the connection of MAX_NUM_CLIENT clients. When MAX_NUM_CLIENT clients are connected, the game begins.
  Each client has a board of 15 numbers. The server draws a number in the range of [1, 90] every x seconds and send this number to all the clients connected.
  The first client that has all the 15 numbers drawn wins the game and send a message to the server to communicate the event. The server informs all the clients that the game
  is over. The clients disconnect while the server stays on and waits for other clients,

  RUN:
  Open a terminal window and navigate to this folder. Launch the server with the command
  'python tombolaServer.py'

  Then launch all the clients you want by opening wach time a new terminal, navigating to this folder and launching the command
  'python tombolaClient.py'
  
- TOMBOLA THREAD
  This is a Tombola game in python with threads using the client-server architecture. Each client has a board of 15 numbers. The server draws a number in the range of [1, 90] every x seconds and send this number to all the clients connected.
  If another client connects when the game has already begun, the server will send all the numbers drawn hitherto and the client checks if all his 15 numbers have been drawn. 
  The first client that has all the 15 numbers drawn wins the game and send a message to the server to communicate the event. The server informs all the clients that the game
  is over and in 1 minute another game will take place. All the clients can play again or exit. The client will use the same board.

  SOLUTION:
  The server has the main thread which waits for clients to connect. Another thread is created for the number drawing. When a client connects a new thread is created which is used to receive from
  the client the message saying that the client made tombola.
  2 ports are used: one for sending the numbers from the server to the client and to inform the clients one someone made tombola and another port usedby the winner to communicate to the server that
  he made client.

  RUN:
  Open a terminal window and navigate to this folder. Launch the server with the command
  'python tombolaThreadServer.py'

  Then launch all the clients you want by opening wach time a new terminal, navigating to this folder and launching the command
  'python tombolaThreadClient.py'
