This is a Tombola game in python using the server-client architecture. The server waits the connection of MAX_NUM_CLIENT clients. When MAX_NUM_CLIENT clients are connected, the game begins.
Each client has a board of 15 numbers. The server draws a number in the range of [1, 90] every x seconds and send this number to all the clients connected.
The first client that has all the 15 numbers drawn wins the game and send a message to the server to communicate the event. The server informs all the clients that the game
is over. The clients disconnect while the server stays on and waits for other clients,

RUN:
Open a terminal window and navigate to this folder. Launch the server with the command
'python tombolaServer.py'

Then launch all the clients you want by opening wach time a new terminal, navigating to this folder and launching the command
'python tombolaClient.py'
