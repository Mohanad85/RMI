from SocketClass import *
import time
import os
# Define robot IP Address and port number
RobotIP = '127.0.0.1'
PortNum = 16001
# initialize a connection
RMI_Conn=SocketClass(RobotIP,PortNum)



''' 
# initialize a connection
RMI_Conn=SocketClass(RobotIP,PortNum)
Command='FRC_Connect'
# Send Connection command to the robot 
RMI_Conn.send_RMI_Connection_command(Command)
time.sleep(2)
# after reciving the new port number, we have to diconnect and connect again using the new port number
# disconnect the connection
#enter new port number manually: 
PortNum = 16002
RMI_Conn2=SocketClass(RobotIP,PortNum)
time.sleep(2)
# Read POSREG1  
RMI_Conn2.read_POSREG_command(1)
time.sleep(2)
# Send Disconnection command to the robot 
Command='FRC_Disconnect'
RMI_Conn2.send_RMI_Connection_command(Command)
 '''