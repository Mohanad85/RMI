from SocketClass import *
import time
import os
# Define robot IP Address and port number
RobotIP = '127.0.0.1'
PortNum = 16001
# initialize a connection
RMI_Conn=SocketClass(RobotIP,PortNum)