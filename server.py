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

registerList = {}
contactList = {}

contactFile = None
if(len(sys.argv) == 3):
    contactFile = sys.argv[2] if (
        sys.argv[2] and sys.argv[2][-4:] == ".txt") else None
print("Contact list: {}\t".format(contactFile), end="") if contactFile else None
serverSocket = socket(AF_INET, SOCK_DGRAM)


def readCommand(command, clientAddr):
    command_split = command.split(" ")
    init = command_split[0].lower()

    if(init == "register"):
        print("You want to register something")
        regContactName = command_split[1]
        regIp = command_split[2]
        regPort = command_split[3]

        adFormat = {
            "name" : regContactName,
            "ip" : regIp,
            "port" : regPort
        }
    
        print(regIp)

        if(regContactName not in registerList):
            registerList[regContactName] = adFormat
            serverSocket.sendto("SUCCESS".encode(),clientAddr)
        else:
            serverSocket.sendto("FAILURE".encode(), clientAddr)



    elif(init == "create"):

        listName = command_split[1]
        
        # if this list name doesn't exist prior we make a new contact list
        if(listName not in contactList):
            contactList[listName] = set()
            serverSocket.sendto("SUCCESS".encode(), clientAddr)
        else:
            serverSocket.sendto("FAILURE".encode(), clientAddr)


    elif(init == "query-lists"):
        # queries the server for the names of the contact lists
        # returns code equal to number of contact lists and names
        serverSocket.sendto("{} {}".format(len(contactList),contactList.keys()).encode(), clientAddr)
        serverSocket.sendto("SUCCESS".encode(), clientAddr)




    elif(init == "join"):
        contactListName = command_split[1]
        contactName = command_split[2]

        if((contactName not in registerList.keys()) or (contactListName not in contactList.keys()) or len(contactList[contactListName]) == 3):
            serverSocket.sendto("FAILURE".encode(), clientAddr)
        else:
            # adding the name to the contact list
            contactList[contactListName].add(contactName)

            # send a success to the client
            serverSocket.sendto("SUCCESS".encode(), clientAddr)


    elif(init == "leave"):
        contactListName = command_split[1]
        contactName = command_split[2]

    elif(init == "exit"):
        contactName = command_split[1]

    elif(init == "im-start"):
        contactListName = command_split[1]
        contactName = command_split[2]

    elif(init == "im-complete"):
        contactListName = command_split[1]
        contactName = command_split[2]

    elif(init == "save"):
        linesPrinted = []
        fileName = command_split[1]
        with open(fileName,'w') as saveFile:
            saveFile.writelines()
        activeUsers = len(registerList)
        numContactList = len(contactList)

        linesPrinted.append(activeUsers)
        for key, value in registerList.items():
            line = "{} {} {}".format(value.name, value.ip, value.port)
            linesPrinted.append(line)

        linesPrinted.append(numContactList)
        for key,value in contactList.items():
            line = "{} {}".format(key, len(value))
            linesPrinted.append(line)


    else:
        print("Command not found")
        serverSocket.sendto("This command was not found".encode(), clientAddr)



def main():
    print("PORT NUM: {}".format(serverPort))

    serverSocket.bind(('', serverPort))
    print("The server is ready to receive")

    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        realMsg = message.decode()
        readCommand(realMsg, clientAddress)
        print(clientAddress)
        # modifiedMessage = message.decode().upper()
        # serverSocket.sendto(modifiedMessage.encode(), clientAddress)

main()



