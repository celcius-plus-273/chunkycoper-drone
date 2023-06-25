# the machine module contains functions related to the hardware on a particular board
# think of it as HAL (Hardware Abstraction Layer)
import machine

# time module contains time related functions e.g. time.sleep()
import time

# allows connection to the internet using the WLAN interface
import network

# used for socket programming -> UDP/TCP connections
import socket

# multi-threading 
import _thread 

# system functions
import sys

# set to True to enable debug prints
verbosity = False

# execute contents of file if file is being run as main (a.k.a. not as a library)
if __name__ == '__main__':

    # initialize built in LED as an output pin
    myLed = machine.Pin('LED', machine.Pin.OUT)

    # network information
    ssid = 'LarryTheLion'
    password = '2074brightleafway'

    #######################
    ### connect to wifi ###
    #######################
    
    wlan = network.WLAN(network.STA_IF) # creates a WLAN interface object in station (client) mode

    # wlan = network.WLAN(network.AP_IF) # creates a WLAN interface object in access point mode
    
    wlan.active(True) # activate WLAN interface
    wlan.connect(ssid, password) # connect to desired network
    
    if verbosity:
        print(f'Attempting to connect to {ssid}')

    while (wlan.isconnected() == False): 
        time.sleep_ms(2000)
        if verbosity:
            print(f'connecting...')
    
    if verbosity:
        print(f'Succesfully connected to {ssid}')
    
    MY_IP = wlan.ifconfig()[0] # store IP obtained

    if verbosity:
        print(f'My IP is: {MY_IP}') # print IP to serial port



    ##################
    ### TCP server ###
    ##################
    # defines a port number for a TCP socket
    PORT = 5000

    try:
        # create a TCP socket (AF_INET -> IPv4) and (SOCK_STREAM -> TCP)
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        print('Socket initialization failed')
        sys.exit()

    try:
        # bind to IP and PORT
        serverSocket.bind((MY_IP, PORT))
    except:
        print(f'Socket could not succesfullt bind with IP: {MY_IP} and PORT: {PORT}')
        sys.exit()
        
    # start listening for incoming connections
    serverSocket.listen(1)
    if verbosity:
        print(f'Server started on PORT {PORT}. Accepting connections')



    ##########################
    ### accept connections ###
    ##########################

    while True:
        myLed.on()
        clientSocket, clientAddress = serverSocket.accept()
        
        time.sleep(5)

        clientSocket.close()
        myLed.off()

        time.sleep(5)

    serverSocket.close()


