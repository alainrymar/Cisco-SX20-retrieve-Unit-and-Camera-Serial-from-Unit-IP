#This code allows to retrieve the Camera serials from multiple Cisco SX20 codecs
################################################################################
#
# Codec_IP_List.txt file must be a text file that contains
#all the Codec IP addresses, one IP per line
#
#Codec_Camera_Serial.txt will be the output file
#
#This piece of code assumes that python 3+ is installed: https://www.python.org/downloads/
#Library SSH from Paramiko is loaded from http://www.paramiko.org/
#
#SX20.py file must be in same directory than Codec_IP_List.txt
#
#The Code Assume that Username and password are the same on all Codec Units !!
# Change here under line 31 and 32 with your Codec user and password !!
#
# To run the code, type: python SX20.py
#
#Written by Alain Rymar
#arymar@cisco.com
#2nd July 2018



import sys
import time
import select
import paramiko

#host = "192.168.1.74"
user = "yourUserName"    #Username
Mdp = "YourPassword"  #Password
response = ""
response2 = ""
response3 = ""
func_return = False


def CameraSerial(host, i):
#
# Try to connect to the host.
# Retry a few times if it fails.
#   
    while True:
          print ("Trying to connect to %s (%i/2)" % (host, i))

          try:
              ssh = paramiko.SSHClient()
              ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
              ssh.connect(host, username=user, password=Mdp)
              print ("Connected to %s" % host)
              break
          except paramiko.AuthenticationException:
              print ("Authentication failed when connecting to %s" % host)
              sys.exit(1)
          except:
              print ("Could not SSH to %s, waiting for it to start" % host)
              i += 1
              time.sleep(2)

          # If we could not connect within time limit
          if i == 3:
              print ("Could not connect to %s. Giving up" % host)
              #print("No answer from Codec:" + host)
              #with open('Codec_Camera_Serial.txt','a') as f:
                 #f.write("Codec: "+ host + "  Camera Serial: not found as Codec not answering !" + '\n')
                 #f.close()
              #sys.exit(1)
              return(False)

    channel = ssh.invoke_shell()
    channel.send('\n')
    time.sleep(2)
    response = (channel.recv(200).decode("utf-8"))
    print(response)

    if "OK" in response: 
         #Request SX20 Unit Serial Number
         channel.send('xStatus SystemUnit Hardware Module SerialNumber\n')
         time.sleep (2)
         response3 = (channel.recv(300).decode("utf-8"))
         print (response3) 
         MyList2 = response3.split()
         
         #request SX20 Camera Serial Number
         channel.send('xStatus Camera 1 SerialNumber\n')
         time.sleep (1)
         response2 = (channel.recv(200).decode("utf-8"))
         print (response2) 
         MyList = response2.split()
         print("Codec: "+ host + " SX20 Unit Serial: "+ MyList2[10] + "  Camera Serial: " + MyList[8])
         with open('Codec_Camera_Serial.txt','a') as f:
             f.write("Codec: "+ host + " SX20 Unit Serial: "+ MyList2[10] + " Camera Serial: " + MyList[8] + '\n')
             #print(lines[2])
             f.close()
    else:
         return(False)
         #print("No answer from Codec:" + host)
         #with open('Codec_Camera_Serial.txt','a') as f:
             #f.write("Codec: "+ host + "  Camera Serial: not found as Codec not answering !" + '\n')
             
             #f.close()

    #
    # Disconnect from the host
    #
    print ("Disconnecting from Host: ", host )
    stdin, stdout, stderr = ssh.exec_command("bye\n")
    print ("Command done, closing SSH connection")
    ssh.close()   
    return(True)          




#Load the CODEC IP @ from file
#file should be setup for :
#ONE IP @ per line
with open('Codec_IP_List.txt') as f:
          lines = (f.readlines())
          #print the first line in file to test access.
          #print(lines[0])
          f.close()

# Loop
#CameraSerial(lines[0])
#print("Codec to get Serial from camera: ", lines[0].rstrip('\n'))
#print("Codec to get Serial from camera: ", lines[1].rstrip('\n'))
for index, item in enumerate(lines): 
     func_return = CameraSerial(lines[index].rstrip('\n'), 1)
     if func_return == True:
             print("Codec: "+ lines[index].rstrip('\n')+ "  Done !")
     else:
             print("Codec: "+ lines[index].rstrip('\n')+ "  NOT Done, connection error, check reachability !")
             #print("No answer from Codec:" + lines[index].rstrip('\n'))
             with open('Codec_Camera_Serial.txt','a') as f:
                 f.write("Codec: "+ lines[index].rstrip('\n') + "  Camera Serial: not found as Codec not answering !" + '\n')
                 f.close()
# End Of Loop



