import socket
import tkinter as tk
import json
import pickle
from functools import partial

class SocketClass(object):
    def __init__(self,IPAdress, PortNum):
        # connections
        self.IPAdress=IPAdress
        self.PortNum=PortNum
        self.IsConnected = False
        self.Connection = 0
        # GUI
        self.root = tk.Tk()
        self.root.title('FANUC RMI, Mohanad tool')
        self.left_frame = tk.Frame(self.root)
        self.left_frame.grid(row = 0,column = 0)
        self.right_frame = tk.Frame(self.root)
        self.right_frame.grid(row = 0,column = 1)
        # Connect Button
        self.ConnectButton = tk.Button(self.right_frame, 
                           text="Connect", 
                           command=self.connect_client,
                           background = 'red')
        self.ConnectButton.grid(row = 0,column = 0)
        #FRC_ConnectButton
        self.FRC_ConnectButton = tk.Button(self.right_frame, 
                           text="FRC_Connect", 
                           command=self.FRC_Connect_function,
                           background = 'red')
        self.FRC_ConnectButton.grid(row = 1,column = 0)
        
        # Read POS REG Button 
        self.FRC_GetPosRegButton = tk.Button(self.right_frame, 
                           text="Get Pos Reg", 
                           command=lambda: self.read_POSREG_command(1),
                           background = 'red')
        self.FRC_GetPosRegButton.grid(row = 2,column = 0)
        
       
        
         
        self.root.mainloop()

    """
    Connect Cleint Socket
    """   
    def connect_client(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ServerAddress = (self.IPAdress, self.PortNum)
            s.connect(ServerAddress)
            self.Connection = s
            self.IsConnected = True
            print ('Connected to %s port %s' % ServerAddress)
        except Exception as e:
            print ('Error in Connecting to %s port %s' % ServerAddress)
        return True 

    """
    Close Cleint Socket
    """
    def close_client(self):
        try:
            self.Connection.close()
            self.isConnectet = False
            print ('Socket disconnected')
            
        except Exception as e:
            print ('Error in socket clsoing')
        return 



    """
    Send RMI Command
    """
    def FRC_Connect_function(self):
        m = {'Communication':'FRC_COnnect'}
        jsonObj=json.dumps(m)
        try:
            # Connect to server and send data
            msg=jsonObj+'\r\n'
            self.Connection.sendall(msg.encode('utf-8'))
            # Receive data from the server and shut down
            received = self.Connection.recv(1024)
            received = received.decode("utf-8")
            print (received)
            sNewPort=received[64:69]
            iNewPort=int(sNewPort)
            self.close_client()
            self.PortNum=iNewPort
            self.connect_client()
        except Exception as e:
            pass
        return 
    
    """
    Read POSREG Command
    """
    def read_POSREG_command(self,PosRegNumm):
        m = {'Command':'FRC_ReadPositionRegister','RegisterNumber': PosRegNumm}
        jsonObj=json.dumps(m)
        try:
            msg=jsonObj+'\r\n'
            print(msg)
            self.Connection.sendall(msg.encode('utf-8'))
            # Receive data from the server and shut down
            received = self.Connection.recv(1024)
            received = received.decode("utf-8")
            print (received)
        except Exception as e:
            pass
        return