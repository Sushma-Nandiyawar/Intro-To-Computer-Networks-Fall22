import socket
from typing import BinaryIO
"""
==================================================================================================
"""
"""
    iface: str || port: integer || use_udp: boolean || fp : position of poiter for data to be copied
"""
def file_server(iface: str, port: int, use_udp: bool, fp: BinaryIO) -> None:
    """call getaddrinfo"""
    sock = socket.getaddrinfo(iface, port)
    try:
        if use_udp:         
            sockett = socket.SOCK_DGRAM
        else:                  
            sockett = socket.SOCK_STREAM
            
        socket_ser = socket.socket(socket.AF_INET, sockett)

        socket_ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_ser.bind((iface, port))

    except Exception as ex:
        pass

    print("Hello!, I am server")

    """
    UDP: receives data in form of packets
    TCP: Listen to client connections
    """

    if use_udp:  
        data, addr = socket_ser.recvfrom(256)
        while data:
            fp.write(data)
            data =socket_ser.recvfrom(256)[0]   
            print("Data from udp server received ......")
    else:       
        socket_ser.listen() 
        print("Listening!")
        '''Connect and get data'''
        cli_conn, addr = socket_ser.accept() 
        print('Got connection from', addr)
        data = cli_conn.recv(256)    
        '''
        get all data, each time size will be 256 and send data 
        '''
        while data:   
            fp.write(data)   
            data = cli_conn.recv(256)        
        """
        pass once all data is received
        """
        cli_conn.close() 
    """
    close client connection then file pointer and server 
    """
    fp.close()
    socket_ser.close()   

"""
==================================================================================================
"""
"""
    host: str || port: integer || use_udp: boolean || fpused to copy files from client
"""
def file_client(host: str, port: int, use_udp: bool, fp: BinaryIO) -> None:
    """
    UDP:DGRAM
    TCP:STREAM
    Initialize and create clien socket
    """
    if use_udp:
        sockett = socket.SOCK_DGRAM
    else:
        sockett = socket.SOCK_STREAM

    socket_cli = socket.socket(socket.AF_INET, sockett)
    print("Hello, I am client!")

    if use_udp:
        message = fp.read(256)       
        '''
        get all data, each time size will be 256 and send data 
        '''
        while message:            
            socket.sendto(message,(host,port)) 
            message = fp.read(256)         
            """Sending 0 byte"""        
        socket_cli.sendto("".encode(),(host,port))    
    else:
        """
        connect
        """
        socket_cli.connect((host,port))  
        message = fp.read(256)

        while message:              
            socket_cli.send(message)            
            message = fp.read(256)              
        socket_cli.send("".encode())      
    """
    close the file pointer and connection  
    """         
    socket_cli.close()
    fp.close()  