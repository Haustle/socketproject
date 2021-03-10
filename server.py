# register
# create < contact
# query-lists
# join
# save

from socket import *
import sys
serverPort = int(sys.argv[1])
import time

# We're group number 79
# So we own port ranges [40500,40999]


# this is the register list and contact list dictionaries
registerList = {
    # "p1" : {
    #     "name" : "p1",
    #     "ip": "127.0.0.1",
    #     "port": "40501"
    # },
    # "p2": {
    #     "name": "p2",
    #     "ip": "127.0.0.1",
    #     "port": "40502"
    # },
    # "p3": {
    #     "name": "p3",
    #     "ip": "127.0.0.1",
    #     "port": "40503"
    # }
}
contactList = {}
activeText = {}

# this will be a command line argument later on when we start IM part
contactFile = None
if(len(sys.argv) == 3):
    # setting command line arguments to variables
    contactFile = sys.argv[2] if (
        sys.argv[2] and sys.argv[2][-4:] == ".txt") else None
print("Contact list: {}\t".format(contactFile), end="") if contactFile else None
serverSocket = socket(AF_INET, SOCK_DGRAM)



# this function is given a string command the client address
def readCommand(command, clientAddr):
    # we split the command based on the space character
    command_split = command.split(" ")
    # we just need to know the first word of the command
    init = command_split[0].lower()

    if(init == "register"):

        # we make variables for the paramters of the register command
        regContactName = command_split[1]
        regIp = command_split[2]
        regPort = command_split[3]

        adFormat = {
            "name" : regContactName,
            "ip" : regIp,
            "port" : regPort
        }

        # check to see if the name already exists
        if(regContactName not in registerList):
            registerList[regContactName] = adFormat
            serverSocket.sendto("\nSUCCESS".encode(),clientAddr)
        else:
            serverSocket.sendto("FAILURE".encode(), clientAddr)


    # create a new contact list
    elif(init == "create"):

        listName = command_split[1]
        
        # if this list name doesn't exist prior we make a new contact list
        if(listName not in contactList):
            contactList[listName] = set()
            serverSocket.sendto("\nSUCCESS".encode(), clientAddr)
        else:
            serverSocket.sendto("FAILURE".encode(), clientAddr)


    elif(init == "query-lists"):
        # queries the server for the names of the contact lists
        # returns code equal to number of contact lists and names
        serverSocket.sendto("{} {}".format(len(contactList),contactList.keys()).encode(), clientAddr)
        serverSocket.sendto("SUCCESS".encode(), clientAddr)


    elif(init == "join"):
        # we need the list name and the person that wants to join
        contactListName = command_split[1]
        contactName = command_split[2]

        # conditions for if the person cannot join
        if((contactName not in registerList.keys()) or (contactListName not in contactList.keys()) or len(contactList[contactListName]) == 3 or contactName in contactList[contactListName]):
            serverSocket.sendto("\nFAILURE".encode(), clientAddr)
        else:
            # adding the name to the contact list
            contactList[contactListName].add(contactName)

            # send a success to the client
            serverSocket.sendto("\nSUCCESS".encode(), clientAddr)


    elif(init == "leave"):
        contactListName = command_split[1]
        contactName = command_split[2]
        if( contactListName not in contactList or contactName not in contactList[contactListName]):
            serverSocket.sendto("\nFAILURE".encode(), clientAddr)
            return

        contactList[contactListName].remove(contactName)
        serverSocket.sendto("\nSUCCESS".encode(), clientAddr)


    # removing a user from all contact list and putting them to unactive
    elif(init == "exit"):
        # we take in the contact name
        contactName = command_split[1]


        # check to see if the name is in a current on going text
        for key,value in activeText.items():
            if(contactName in contactList[key]):
                serverSocket.sendto("\nFAILURE".encode(), clientAddr)

                # deregister the user
                return
                
        del registerList[contactName]

        # remove the user from all contactLists
        for key, value in contactList.items():
            if contactName in value:
                value.remove(contactName)

        serverSocket.sendto("\nSUCCESS".encode(), clientAddr)


    elif(init == "im-start"):
        contactListName = command_split[1]
        contactName = command_split[2]

        if(contactName not in contactList[contactListName] or contactListName in activeText.keys()):
            serverSocket.sendto("\nFAILURE".encode(), clientAddr)
            serverSocket.sendto("0".encode(), clientAddr)
            return

        # we prompt the user for a message
        # here we need to make a json object that can hold the message
        activeText[contactListName] = contactName
        serverSocket.sendto("\nType msg as next command".encode(), clientAddr)
        # we capture the msg they want to send
        message, clientAddress = serverSocket.recvfrom(2048)
        actMsg = message.decode()

        # for each person in the list we're going to print out their details.


        serverSocket.sendto(("\n{}".format(len(contactList[contactListName]))).encode(), clientAddr)
        for person in contactList[contactListName]:
            if(contactName == person):
                personInfo = registerList[person]
                line = "{} {} {}".format(personInfo["name"], personInfo["ip"], personInfo["port"])
                serverSocket.sendto(("{}".format(line)).encode(), clientAddr)
                break


        for person in contactList[contactListName]:
            if(contactName != person):
                personInfo = registerList[person]
                line = "{} {} {}".format(personInfo["name"], personInfo["ip"], personInfo["port"])
                serverSocket.sendto(("{}".format(line)).encode(), clientAddr)

            # print(line)
            # add personal details to linesPrinted so it can get printed

            
        # we find the group of people they want to send the message to

        setOfGroupMembers = list(contactList[contactListName])
        ipForm = ["{}-{}".format(registerList[name]["ip"],registerList[name]["port"]) for name in setOfGroupMembers]

        tempList = ipForm

        # remove the caller and then add them to the end of the list, so it can make sure all messages have been sent
        tempList.remove('{}-{}'.format(clientAddr[0], clientAddr[1]))
        tempList.append('{}-{}'.format(clientAddr[0], clientAddr[1]))
        newStr = ";".join(ipForm)
        print(newStr)



        # create a header to send to users in the group
        header = "im-start =[{}] {}: {}`{}".format(contactListName,contactName,actMsg, newStr)
        print("Header sent: {}".format(header))

        # send the packaged header to the person requesting the im-start
        serverSocket.sendto(("{}".format(header)).encode(), clientAddr)




    elif(init == "im-complete"):
        contactListName = command_split[1]
        contactName = command_split[2]

        # we make a check to make sure the person requesting the im-complete is the one who use im-start
        if(contactName == activeText[contactListName]):

            del activeText[contactListName]
            serverSocket.sendto("\nSUCCESS".encode(), clientAddr)
        else:
            serverSocket.sendto("\FAILURE".encode(), clientAddr)


        # we remove the group from active




    # save IM structure to .txt file
    elif(init == "save"):
        # we add all the lines we want to print into the file into linesPrinted
        linesPrinted = []
        fileName = command_split[1]

        # we open the text file that the user passed in as a name
        saveFile = open(fileName,'w')

        # get the string amount of people in the register
        activeUsers = str(len(registerList))

        # get the string amount of how many contact lists there are
        numContactList = str(len(contactList))

        linesPrinted.append(activeUsers)

        # we're iterating through the registerlist and printing out everyone with their information aswell
        for key, value in registerList.items():
            line = "{} {} {}".format(value["name"], value["ip"], value["port"])
            # add eachline to the ist
            linesPrinted.append(line)

        linesPrinted.append(numContactList)

        # we iterate through the contactList map and print
        for key,value in contactList.items():
            line = "{} {}".format(key, len(value))

            # we're adding the contact list name and the amo;unt of users it contains
            linesPrinted.append(line)

            # for each person in the list we're going to print out their details.
            for person in value:
                personInfo = registerList[person]
                line = "{} {} {}".format(personInfo["name"], personInfo["ip"], personInfo["port"])
                # add personal details to linesPrinted so it can get printed
                linesPrinted.append(line)

        # for each line we've added we want them to be on their own independent line so we add "\n"
        linesPrinted = [line + "\n" for line in linesPrinted]
        saveFile.writelines(linesPrinted)

        # we return success
        serverSocket.sendto("SUCCESS".encode(), clientAddr)

    else:
        serverSocket.sendto("This command was not found".encode(), clientAddr)



def main():
    print("PORT NUM: {}".format(serverPort))

    serverSocket.bind(('', serverPort))


    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        realMsg = message.decode()
        # print out the message received
        print("Server receives string: {}".format(realMsg))
        # and where the message came from
        print("Server handling client: {} PORT: {}".format(clientAddress[0], clientAddress[1]))
        readCommand(realMsg, clientAddress)
        # serverSocket.sendto("Completed request".encode(),clientAddress)
        # time.sleep(3)


main()



