from socket import *
from threading import *
from tkinter import *
import selectinwindow
import sys
import cv2  # Opencv ver 3.1.0 used
import numpy as np

# set up the rectangle notes and window
sys.setrecursionlimit(10 ** 9)

windowName = 'named window'
wName = "select region"
imageWidth = 320
imageHeight = 240
image = np.ones([imageHeight, imageWidth, 3], dtype=np.uint8)  # OR read an image using imread()
image *= 255

# set up the client connection
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

hostIp = "127.0.0.1"
portNumber = 7500

clientSocket.connect((hostIp, portNumber))

window = Tk()
window.title("Connected To: "+ hostIp+ ":"+str(portNumber))

txtMessages = Text(window, width=50)
txtMessages.grid(row=0, column=0, padx=10, pady=10)

txtYourMessage = Entry(window, width=50)
txtYourMessage.insert(0,"Your message")
txtYourMessage.grid(row=1, column=0, padx=10, pady=10)

def sendMessage():
    clientMessage = txtYourMessage.get()
    txtMessages.insert(END, "\n" + "You: "+ clientMessage)
    clientSocket.send(clientMessage.encode("utf-8"))

def drawRect():
    rectI = selectinwindow.DragRectangle(image, windowName, imageWidth, imageHeight)
    cv2.namedWindow(rectI.wname)
    cv2.setMouseCallback(rectI.wname, selectinwindow.dragrect, rectI)
    cv2.imshow(wName, rectI.image)

btnSendMessage = Button(window, text="Send", width=20, command=drawRect)
btnSendMessage.grid(row=2, column=0, padx=10, pady=10)

def recvMessage():
    while True:
        serverMessage = clientSocket.recv(1024).decode("utf-8")
        print(serverMessage)
        txtMessages.insert(END, "\n"+serverMessage)

recvThread = Thread(target=recvMessage)
recvThread.daemon = True
recvThread.start()

window.mainloop()


