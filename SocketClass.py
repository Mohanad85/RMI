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
        self.ConnectButton.grid(row = 0,column = 0,sticky='E',padx=10)
        #FRC_ConnectButton
        self.FRC_ConnectButton = tk.Button(self.right_frame, 
                           text="FRC_Connect", 
                           command=self.FRC_Connect_function,
                           background = 'red')
        self.FRC_ConnectButton.grid(row = 1,column = 0,sticky='E',padx=10)
        
        # Read POS REG Button 
        self.FRC_GetPosRegButton = tk.Button(self.right_frame, 
                           text="Get Pos Reg", 
                           command=self.read_POSREG_command,
                           background = 'red')
        self.FRC_GetPosRegButton.grid(row = 2,column = 0,sticky='E',padx=10)
        
         # Write POS REG Button 
        self.FRC_GetPosRegButton = tk.Button(self.right_frame, 
                           text="Write Pos Reg", 
                           command=self.write_POSREG_command,
                           background = 'red')
        self.FRC_GetPosRegButton.grid(row = 3,column = 0,sticky='E',padx=10)
          # Disconnect 
        self.FRC_DisconnectButton = tk.Button(self.right_frame, 
                           text="FRC_Disconnect", 
                           command=self.FRC_Disconnect_function,
                           background = 'red')
        self.FRC_DisconnectButton.grid(row = 4,column = 0,sticky='E',padx=10)
        
        # left side 
        self.label_PosRegNum = tk.Label(self.left_frame, fg="black",text="Enter POS Reg Number to read/write")
        self.label_PosRegNum.grid(row = 0,column = 0,sticky='W',padx=10)
        
        self.entry_PosRegNum_str = tk.StringVar()
        self.entry_PosRegNum = tk.Entry(self.left_frame, textvariable=self.entry_PosRegNum_str,width = 5)
        self.entry_PosRegNum.grid(row = 1,column = 0,sticky='W',padx=10)
        self.entry_PosRegNum_str.set("1")
        
        self.label_PosReg = tk.Label(self.left_frame, fg="black",text="Enter POS Reg Values here")
        self.label_PosReg.grid(row = 2,column = 0,sticky='W',padx=10)
        
        self.entry_PosReg_str = tk.StringVar()
        self.entry_PosReg = tk.Entry(self.left_frame, textvariable=self.entry_PosReg_str,width = 80)
        self.entry_PosReg.grid(row = 3,column = 0,sticky='W',padx=10)
        self.entry_PosReg_str.set("Example: X10.1,Y20.1,Z30.5,W40.4,P50.5,R60.6,")

        
       
        
         
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
     RMI_Connect Command
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
    RMI_DisConnect Command
    """
    def FRC_Disconnect_function(self):
        m = {'Communication':'FRC_Disconnect'}
        jsonObj=json.dumps(m)
        try:
            msg=jsonObj+'\r\n'
            self.Connection.sendall(msg.encode('utf-8'))
            # Receive data from the server and shut down
            received = self.Connection.recv(1024)
            received = received.decode("utf-8")
            print (received)
            self.close_client()
        except Exception as e:
            print('Error in FRC_Disconnect')
        return 
    
    """
    Read POSREG Command
    """
    def read_POSREG_command(self):
        PosRegNumm=self.entry_PosRegNum_str.get()
        m = {'Command':'FRC_ReadPositionRegister','RegisterNumber': PosRegNumm}
        jsonObj=json.dumps(m)
        try:
            msg=jsonObj+'\r\n'
            self.Connection.sendall(msg.encode('utf-8'))
            # Receive data from the server and shut down
            received = self.Connection.recv(1024)
            received = received.decode("utf-8")
            print (received)
        except Exception as e:
            pass
        return
    
    """
    FRC_WritePositionRegister
    """
    def write_POSREG_command(self):
        PosRegNumm=self.entry_PosRegNum_str.get()
        entered=self.entry_PosReg_str.get()
        X= self.extract(entered,'X')
        Y= self.extract(entered,'Y')
        Z= self.extract(entered,'Z')
        W= self.extract(entered,'W')
        P= self.extract(entered,'P')
        R= self.extract(entered,'R')
        
        m = {
            'Command'          : 'FRC_WritePositionRegister',
             'RegisterNumber'   : PosRegNumm,
             'Configuration'    : {
                 'UToolNumber'  : 1,
                 'UFrameNumber' : 1,
                 'Front'        : 1,
                 'Up'           : 1,
                 'Left'         : 1,
                 'Flip'         : 0,
                 'Turn4'        : 0,
                 'Turn5'        : 0,
                 'Turn6'        : 0},
             'Position'         : { 
                 'X'            : X, 
                 'Y'            : Y,
                 'Z'            : Z, 
                 'W'            : W, 
                 'P'            : P,
                 'R'            : R, 
                 'Ext1'         : 0.0,
                 'Ext2'         : 0.0, 
                 'Ext3'         : 0.0 },
             'Group': 1
             }
        jsonObj=json.dumps(m)
        try:
            msg=jsonObj+'\r\n'
            self.Connection.sendall(msg.encode('utf-8'))
            # Receive data from the server and shut down
            received = self.Connection.recv(1024)
            received = received.decode("utf-8")
            print (received)
        except Exception as e:
            pass
        return
    
    def extract(self,inputStr,value):
        startidx=inputStr.find(value)
        endidx=inputStr[startidx:].find(',')
        foundvalue=inputStr[startidx+1:startidx+endidx]
        return foundvalue
        