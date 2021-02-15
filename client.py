import sys
from socket import *



serverIP = sys.argv[1]
serverPort = int(sys.argv[2])


while True:
    # SOCK_DGRAM means it's a UDP socket
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message = input("Enter a command: ")

    # using .encode() to convert the messages to bytes
    clientSocket.sendto(message.encode(), (serverIP, serverPort))

    # when a packet arrives at the client socket the data is put into
    # modifiedMessage and the address it was sent from
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

    # prints out the decoded message we have received
    print(modifiedMessage.decode())
