import sys
from socket import *
import pickle
import time
import multiprocessing

serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(('', int(sys.argv[3])))


def somefun():
    while True:
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        actualMsg = (modifiedMessage.decode())
        if(actualMsg.startswith('im-start')):

            msgAndIps = (actualMsg.split("=")[1]).split('`')
            msg2send = msgAndIps[0]
            ips2send = msgAndIps[1].split(";") # we get the ip string and split by the delimeter I made

            print(msg2send)

            # If there are no more Ips
            if(len(msgAndIps) == 1):
                continue

            # We just need to send it to the first ip so use [0] and we just split -
            # because the delimeter is a - (i.g ip-port)
            ipMsgReceiver = ips2send[0].split("-")
            if(len(ipMsgReceiver) < 2):
                continue
            recIp = ipMsgReceiver[0]
            recPort = int(ipMsgReceiver[1])
            print("msg being sent to: {}".format(ipMsgReceiver))

            # we remove the ip that we're sending to for the new header
            rePackedHeader = "im-start={}`{}".format(msg2send,";".join(ips2send[1:]))
            clientSocket.sendto(rePackedHeader.encode(),(recIp,recPort))
            continue

        print(actualMsg)


def main():
    
    multiprocessing.Process(target=somefun).start()

    # p1.start()
    while True:
        message = input("Enter a command: ")
        if(message != ""):
            clientSocket.sendto(message.encode(), (serverIP, serverPort))







main()
