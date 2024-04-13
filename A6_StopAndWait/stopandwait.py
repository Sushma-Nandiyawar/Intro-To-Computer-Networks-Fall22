import socket
import sys
from typing import BinaryIO
"""
Defining a splitter which will be used to separate the data
"""
splitter = b':->'

"""
Server Side Code
"""
def stopandwait_server(iface:str, port:int, fp:BinaryIO) -> None:
    """
    SOCK_DGRAM as we are using UDP
    AF_INET as we will be using IPV4
    """
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    """
    Remove the sock which is already in use
    """
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
    """
    Get client address
    """  
    client_address = ((socket.gethostbyname(iface)),port) 
    """
    Bind socket to client address 
    """               
    server_socket.bind(client_address)    
    """
    Print the message when server started
    """                                       
    print("Hello, I am a server")
    bits_sequence_serial = b'0'                                                              
    while True:
        received_data,addr = server_socket.recvfrom(256)   
        """
        Get the sequence number, next binary sequence and data from the 
        data received from the client on server side
        As the data is separated by the the  separator get data 
        """                    
        sequence_no,next_binary_sequence,received_data = received_data.split(splitter) 

        print(sequence_no)
        print(next_binary_sequence)
        print(received_data)
        print(bits_sequence_serial)

        if sequence_no==bits_sequence_serial:                                      
            server_socket.sendto(sequence_no,addr)  
            """
            Set the bits sequence
            """                               
            if bits_sequence_serial==b'0':                                  
                bits_sequence_serial = b'1'
            else:
                bits_sequence_serial = b'0'
        """
        Write the data received from client into file
        """
        print("Writing the data to file.....")
        fp.write(received_data)  
        """
        Checking if next data is available
        """
        next_binary_sequence=int(next_binary_sequence)  
        """
        if no data available break the loop
        """                  
        if next_binary_sequence==0:                                        
            break
    sys.exit()

""""
Client side code
"""
def stopandwait_client(host:str, port:int, fp:BinaryIO) -> None:
    """
    SOCK_DGRAM as we are using UDP
    AF_INET as we will be using IPV4
    """
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    """
    Remove the sock which is already in use
    """
    client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  
    """
    Get host address
    """
    host_address = (socket.gethostbyname(host),port)
    print("Hello, I am a client")
    bits_sequence = b'0'                                       
    total_data =  fp.read()   
    """
    Get length of whole data so that it can be read and will help to send data
    """                           
    all_data_length = len(total_data)                                         
    data_size = 248                                        
    binary_next = 1     
    """
    While lopp untill we have data
    """  
    fpointer=0    
    """
    Run loop till end of the file by comparing the length
    """
    while fpointer<all_data_length:                        
        if fpointer+data_size>=all_data_length:
            binary_next=0
        """
        Create header
        """
        header=bits_sequence+splitter+str(binary_next).encode()+splitter 
        """
        Create the data to be sent to the server which is header and actual data 
        """
        x = fpointer+data_size
        data_to_send = header+total_data[fpointer:x]
        print("Sending data to server.....")
        client_socket.sendto(data_to_send,host_address)
        """
        Set the timer to check if acknowlegement will be received in given specific time
        """
        client_socket.settimeout(0.03)  
        """
        Put into try and catch block 
        """                  
        try:
            response,addr = client_socket.recvfrom(256)   
            response = response.decode()    
            # print(response)      
        except:
            continue
        """
        Checking bits sequence
        """
        if bits_sequence==b'0':
            bits_sequence = b'1'                      
        else:
            bits_sequence=b'0'
        """
        Increment the pointer to get next data
        """
        fpointer = fpointer + data_size 
    sys.exit() 
