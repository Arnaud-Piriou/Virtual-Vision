import socket
import sys
import multiprocessing as mp
import json
import os
sys.path.append("../Utils")
from Logger import Logger

class Socket :

    def connect(self) :

        Logger.printInfo("Connecting to cloud platform at " + str(self.address) + ":" + str(self.port) + " ...")
        self.socket.connect((self.address, int(self.port)))
        Logger.printSuccess("Successfully connected to cloud platform at " + str(self.address) + ":" + str(self.port) + " !")

        return True



    def initConfig(self, answer) :

        if answer == "Config file size ?" :
            #Send config file size
            with open(os.path.join(self.projectDirectory, "rconfig.json")) as file:
                    configFile = json.load(file)

            self.socket.send(str(len(str(configFile))).encode("UTF-8"))
            #Receive ACK for config file size
            answer = self.socket.recv(1024).decode("UTF-8")

        if answer == "ACK CF Size" :
            #Send config file
            self.socket.send(str(configFile).encode("UTF-8"))
            Logger.printSuccess("Configuration file successfully sent !")
            #Receive ACK for config file
            answer = self.socket.recv(1024).decode("UTF-8")

        if answer == "ACK CF" :
            #Send intrinsics file size
            with open(os.path.join(self.projectDirectory, "Intrinsics.json")) as file:
                    intrinsicsFile = json.load(file)

            self.socket.send(str(len(str(intrinsicsFile))).encode("UTF-8"))
            #Receive ACK for intrinsics file size
            answer = self.socket.recv(1024).decode("UTF-8")

        if answer == "ACK IF Size" :
            #Send intrinsics file
            self.socket.send(str(intrinsicsFile).encode("UTF-8"))
            Logger.printSuccess("Intrinsics file successfully sent !")
            #Receive ACK for intrinsics file
            return self.socket.recv(1024).decode("UTF-8")

        

    def sendImages(self, answer) :

        count = 0
        logCount = 0
            
        depthPath = os.path.join(self.projectDirectory, "Depth")
        colorPath = os.path.join(self.projectDirectory, "Color")
        depthFileList = sorted(os.listdir(depthPath), key = lambda x : int(x.split(".png")[0]))
        colorFileList = sorted(os.listdir(colorPath), key = lambda x : int(x.split(".jpg")[0]))

        while answer != "End" :
            #Load images
            with open(os.path.join(depthPath, depthFileList[count]), "rb") as image :
                depthImage = image.read()
            with open(os.path.join(colorPath, colorFileList[count]), "rb") as image :
                colorImage = image.read()
                
            #Send depth image size
            self.socket.send(str(len(depthImage)).encode("UTF-8"))
            #Receive ACK for depth image size
            answer = self.socket.recv(1024).decode("UTF-8")

            if answer == "ACK Depth Size" :
                #Send depth image
                self.socket.sendall(depthImage)
                logCount += 1
                progress = round(float(logCount) / (len(depthFileList) + len(colorFileList)) * 100.0, 2)
                Logger.printProgress("Successfully sending frame " + str(logCount) + "/" + str(len(depthFileList) + len(colorFileList)) + " -> " + str(progress) + "%")
                #Receive ACK for depth image
                answer = self.socket.recv(1024).decode("UTF-8")
                    
                if answer == "ACK Depth" :
                    #Send color image size
                    self.socket.send(str(len(colorImage)).encode("UTF-8"))
                    #Receive ACK for color image size
                    answer = self.socket.recv(1024).decode("UTF-8")

                    if answer == "ACK Color Size" :
                        #Send color image
                        self.socket.sendall(colorImage)
                        logCount += 1
                        progress = round(float(logCount) / (len(depthFileList) + len(colorFileList)) * 100.0, 2)
                        Logger.printProgress("Successfully sending frame " + str(logCount) + "/" + str(len(depthFileList) + len(colorFileList)) + " -> " + str(progress) + "%")

            count += 1
            
            answer = self.socket.recv(1024).decode("UTF-8")



    def newReconstruction(self) :
        
        Logger.printOperationTitle("RECONSTRUCTION")
        self.socket.send("New Reconstruction".encode("UTF-8"))
        answer = self.socket.recv(1024).decode("UTF-8")

        answer = self.initConfig(answer)

        if answer == "New image ?" :
            self.sendImages(answer)



    def run(self) :
        
        connected = self.connect()

        if connected :

            self.newReconstruction()
            Logger.printInfo("Closing connection ...")
            self.socket.send("Disconnect".encode("UTF-8"))
            self.socket.close()
            Logger.printSuccess("Connection successfully closed !")



    def __init__(self, address, port, projectDirectory) :

        self.address = address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.projectDirectory = projectDirectory