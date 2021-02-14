# register
# create < contact
# query-lists
# join
# save

from socket import * 
import sys
HOST = '127.0.0.1'
serverPort = int(sys.argv[1])

# We're group number 79
# So we own port ranges [40500,40999]
# PORT = 40501

contactList = None
if(len(sys.argv) == 3):
    contactList =  sys.argv[2] if (sys.argv[2] and sys.argv[2][-4:] == ".txt") else None
print("Contact list: {}\t".format(contactList), end="") if contactList else None
print("PORT NUM: {}".format(serverPort))

# command = input("Enter a command: ")

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server is ready to receive")

while True:
    # print("hello")
    message, clientAddress = serverSocket.recvfrom(2048)
    # print(message.decode().upper())
    realMsg = message.decode()
    readCommand(realMsg)
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)







def readCommand(command):
    command_split = command.split(" ")
    init = command_split[0].lower()

    if(init == "register"):
        print("You want to register something")
        regContactName = command_split[1]
        regIp = command_split[2]
        regPort = command_split[3]


        pass

    elif(init == "create"):
        print("You want to create something")

        conList = command_split[1]
        pass

    elif(init == "query-lists"):
        # queries the server for the names of the contact lists
        # returns code equal to number of contact lists and names
        pass

    elif(init == "join"):
        contactListName = command_split[1]
        contactName = command_split[2]
        pass

    elif(init == "leave"):
        contactListName = command_split[1]
        contactName = command_split[2]
        pass

    elif(init == "exit"):
        contactName = command_split[1]
        pass

    elif(init == "im-start"):
        contactListName = command_split[1]
        contactName = command_split[2]
        pass

    elif(init == "im-complete"):
        contactListName = command_split[1]
        contactName = command_split[2]

        pass

    elif(init == "save"):
        fileName = command_split[1]
        pass
    else:
        print("Command not found")

def main():
    pass


