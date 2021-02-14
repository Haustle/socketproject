from socket import *
# serverName = '127.0.0.1'
serverName = '192.168.1.118'
serverPort = 4501


while True:
    # SOCK_DGRAM means it's a UDP socket
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message = input("Enter a command: ")

    # using .encode() to convert the messages to bytes
    clientSocket.sendto(message.encode(),(serverName, serverPort))

    # when a packet arrives at the client socket the data is put into
    # modifiedMessage and the address it was sent from
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

    # prints out the decoded message we have received
    print(modifiedMessage.decode())
