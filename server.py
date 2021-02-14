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

contactList = None
if(len(sys.argv) == 3):
    contactList = sys.argv[2] if (
        sys.argv[2] and sys.argv[2][-4:] == ".txt") else None
print("Contact list: {}\t".format(contactList), end="") if contactList else None
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

        if(regContactName not in registerList):
            registerList[regContactName] = adFormat
            serverSocket.sendto("SUCCESS".encode(),clientAddr)
        else:
            serverSocket.sendto("FAILURE".encode(), clientAddr)



    elif(init == "create"):
        print("You want to create something")

        conList = command_split[1]

    elif(init == "query-lists"):
        # queries the server for the names of the contact lists
        # returns code equal to number of contact lists and names
        pass

    elif(init == "join"):
        contactListName = command_split[1]
        contactName = command_split[2]

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
        fileName = command_split[1]
    else:
        print("Command not found")


def main():
    print("PORT NUM: {}".format(serverPort))

    serverSocket.bind(('', serverPort))
    print("The server is ready to receive")

    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        # print(message.decode().upper())
        realMsg = message.decode()
        readCommand(realMsg, clientAddress)
        # modifiedMessage = message.decode().upper()
        # serverSocket.sendto(modifiedMessage.encode(), clientAddress)

main()



