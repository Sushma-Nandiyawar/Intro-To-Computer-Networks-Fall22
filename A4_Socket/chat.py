import threading, os
import socket

"""
==================================================================================================
"""
# function to handle multithreading
# this handler is used for different replies from server to client in case of tcp connections
"""
    arg1: connection: connection of client
    arg2: address: address of client
    arg3: socket: server socket
    arg4: conn_dict: dictionary of all connections
"""
def thread_handler_tcp(addr, sock, conn, conn_dict):
    # connection established
    print("Connection {} from {} has been established".format(len(conn_dict) - 1, addr))
    while True:
        # receiving the message from client -> 256 bytes
        data = conn.recv(256)
        data = data.decode().replace("\n","")
        print("got message from {}".format(addr))

        # if the message is goodbye server will respond with farewell and terminate this client connection
        if data == 'goodbye':
            conn.send('farewell\n'.encode())
            break
        # if message is exit server will respond with ok and then terminate
        elif data == 'exit':
            conn.send('ok\n'.encode())
            for connection_tcp in conn_dict.values():
                connection_tcp.close()
            sock.close()
            os._exit(1)
        # if message is hello server will respond with world and wait for other messages
        elif data == 'hello':
            conn.send('world\n'.encode())
        # if other messages are sent server will respond with echo i.e return same messages
        else:
            data = f"{data}\n"
            conn.send(data.encode())

    # closing connections
    conn.close()

    # deleting the particular connection using address key
    del conn_dict[addr]

"""
==================================================================================================
"""
# ==============================================================
# server function for chatroom
"""
    arg1: iface: str
    arg2: port: integer
    arg3: use_udp: boolean
"""
def chat_server(iface: str, port: int, use_udp: bool) -> None:
    
    sock = socket.getaddrinfo(iface, port)
    try:
        if use_udp:    # if True: use UDP else TCP
            SOCK = socket.SOCK_DGRAM
        else:
            SOCK = socket.SOCK_STREAM
        server_socket = socket.socket(socket.AF_INET, SOCK)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # to avoid bindaddress already in use error
        server_socket.bind((iface,port))

    except Exception as e:
        pass

    print("Hello, I am a server")

    """
    if message:
        1. goodbye : server responds with farewell and terminate this client connection
        2. exit : server responds with ok and then terminate
        3. hello : server responds with world and wait for other messages
        4. other : server responds with echo i.e return same messages
    """
    # if using udp we directly receive the packets
    if use_udp:  
        while True:
            # receiveing the message and address from client -> 256 bytes
            data, addr = server_socket.recvfrom(256)
            data = data.decode().replace("\n","")

            # printing required statement as stated in assignment
            print("got message from {}".format(addr))

            if data == 'goodbye': 
                server_socket.sendto('farewell\n'.encode(), addr)
            elif data == 'hello':
                server_socket.sendto('world\n'.encode(), addr)
            elif data == 'exit':
                server_socket.sendto('ok\n'.encode(), addr)
                break 
            else:
                data = f"{data}\n"
                server_socket.sendto(data.encode(), addr)

        server_socket.close()   # closing connection
        return

    # if using tcp 
    # listen from incoming connections
    server_socket.listen()  

    # a dictory to store connections list
    # dict_key: address
    # dict_value: connection
    conn_dict = {}    

    while True:
        connection, addr = server_socket.accept()  # accepting the connection
        conn_dict[addr] = (connection)    # storing the value of connection and its adress

        # using multi threading to accept multiple clients
        thread = threading.Thread(target=thread_handler_tcp, args=(addr, server_socket, connection, conn_dict))
        thread.start()

def chat_client(host: str, port: int, use_udp: bool) -> None:
    compare_reply = ['goodbye', 'exit'] #for comparison

    if use_udp: # UDP requires DGRAM socket
        S = socket.SOCK_DGRAM
    else: # TCP requires STREAM socket
        S = socket.SOCK_STREAM

    # Creating client socket
    cli_sock = socket.socket(socket.AF_INET, S)

    # getting the address of client
    cli_addr = (socket.gethostbyname(host), port)
    print('Hello, I am a client')

    # TCP socket we need to connect to server
    # UDP No connection required as it is connectionless
  
    if use_udp:
        while True:
            message = input()
            
            if message in compare_reply: # sending udp packets to server
                message += "\n"
                cli_sock.sendto(message.encode(),cli_addr)
                data,addr = cli_sock.recvfrom(256)
                print(data.decode().replace("\n",""))
                break
            else:
                message += "\n"
                cli_sock.sendto(message.encode(),cli_addr)
                data,addr = cli_sock.recvfrom(256)
                print(data.decode().replace("\n",""))
        cli_sock.close()
        return
    # tcp connection
    cli_sock.connect(cli_addr)
    while True:
        message = input().lower()
        if message in compare_reply:   # sending tcp packets to server
            cli_sock.send(message.encode())
            data = cli_sock.recv(256)
            print(data.decode().replace("\n",""))
            
            break
        else:
            cli_sock.send(message.encode())
            data = cli_sock.recv(256)
            print(data.decode().replace("\n",""))
    cli_sock.close()