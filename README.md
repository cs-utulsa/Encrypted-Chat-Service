# Encrypted-Chat-Service
Uses 3 classes for basic chat functionality. They are chat, client and server
* The client class is used to attempt to directly connect to another host.
* The server class is for listening on a port for a connection to be made.
* The chart class drives the application. It utulizes client and server to establish a connection, then runs the chat session.

# Running Hermes in Console mode
Use powershell to start the following files

* To run the client class use,
python .\main.py client --target 127.0.0.1 --port 8888

* To run the server class use,
python .\main.py host --target 127.0.0.1 --port 8888

# Running Hermes in GUI mode
Use powershell to start the following files

* python ./main.py 
* You will be promted to type in your username
* The GUI will now appear and you will type in your targeted ip and port.
