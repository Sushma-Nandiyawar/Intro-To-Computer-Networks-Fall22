'''
import all the packages needed
'''
from typing import BinaryIO
import pickle
import socket
'''
Server side of code
'''
def gbn_server(iface:str, port:int, fp:BinaryIO) -> None:
    print("server Started.........")
    print("Hello, I am a server_connection_socket.................")
    '''
    Creating socket
    '''
    server_connection_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    '''binding socket'''
    server_connection_socket.bind((iface, port))
    '''variable to track packets sequence number'''
    sequence_number_packet = 0

    while True:

        '''dictionary to store packet which is received'''
        receiving_packet = {}
        '''get the mesage value and the address from which message is received'''
        mesage_value, recv_from_address = server_connection_socket.recvfrom(612)
        '''extract proper message'''
        datagram = pickle.loads(mesage_value)

        '''if data present'''
        if datagram['packed_data'] and datagram['data_sequence_number'] == sequence_number_packet and datagram['packed_data'] != 'sushma_fileends':
            receiving_packet['data_sequence_number'] = datagram['data_sequence_number']
            '''set positive ack to 0 which will be checked on the client side '''
            receiving_packet['positive_acknowledgement'] = 0
            '''  writing data to file in server side '''
            fp.write(datagram['packed_data'])
            server_connection_socket.sendto(pickle.dumps(receiving_packet), recv_from_address)
            sequence_number_packet+=1
            '''if packed data is set as file enends'''
        elif datagram['packed_data'] == "sushma_fileends":
            receiving_packet['data_sequence_number'] = datagram['data_sequence_number']
            ''' setting negative ack '''
            receiving_packet['positive_acknowledgement'] = ""
            server_connection_socket.sendto(pickle.dumps(receiving_packet), recv_from_address)
            print("server under send to.....")
            print(receiving_packet)
            '''close filepointer'''
            fp.close()
            break
        else:
            continue
    '''close server connection '''
    server_connection_socket.close()
        
'''
Client side code
'''
def gbn_client(host:str, port:int, fp:BinaryIO) -> None:
    complete_packet = {}
    file_data_array = []
    '''aetting windw size 5'''
    slider_size = 5
    
    print("client_connection_socket side started...................")
    print("Hello, I am a client_connection_socket...........")
    ''' Establishing connection '''
    client_connection_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    '''
    get all the file data received from client into file_data_array
    '''
    while True:
        ''' read the data size of 256 bytes size '''
        file_data = fp.read(256)
        ''' If data is present add to file_data_array'''
        if file_data:
            file_data_array.append(file_data)
            ''' else break '''
        else:
            break
    '''set window interval same as slider size'''
    window_slider_interval = slider_size
    packet_incoming_num = 0
    ''' calculate the size of data received from client side which is dumped into file_data_array'''
    length_of_data = len(file_data_array)
    ''' set timeout to 0.05 '''
    stop = 0.05
    packet_tag = 0

    while True:
        try:
            '''set socket timeout'''
            client_connection_socket.settimeout(stop)
            if(packet_tag + slider_size > length_of_data):
                temp_interval = length_of_data - packet_tag
                '''set counter to zero'''
                tiktok = 0
                while temp_interval>tiktok:
                    window_slider_interval = length_of_data - packet_tag
                    '''making data to be sent to server'''
                    complete_packet['packed_data'] = file_data_array[packet_tag + tiktok]
                    complete_packet['data_sequence_number'] = packet_tag+tiktok
                    '''send the complete data to server'''
                    client_connection_socket.sendto(pickle.dumps(complete_packet), (host,port))
                    print("client_connection_socket side ")
                    print(complete_packet)
                    '''increment the counter'''
                    tiktok+=1
            else:
                slider_window_cnt = 0
                while slider_window_cnt < slider_size:
                    '''making data to be sent to server'''
                    complete_packet['packed_data'] = file_data_array[packet_tag + slider_window_cnt]
                    complete_packet['data_sequence_number'] = packet_tag+slider_window_cnt 
                    '''send data to server'''
                    client_connection_socket.sendto(pickle.dumps(complete_packet), (host,port))
                    print("client_connection_socket side ")
                    print(complete_packet)
                    '''increase the window count'''
                    slider_window_cnt += 1

            '''if the length of data is equal to the incoming packets num break the loop'''
            if (packet_incoming_num == length_of_data):
                break
            
            counter_temp = 0
            while counter_temp < window_slider_interval:
                '''check the acknowledgement'''
                dataval_client, recv_from_address = client_connection_socket.recvfrom(256)
                received_data = pickle.loads(dataval_client)
                ''' if positive ack '''
                if received_data['data_sequence_number'] == packet_incoming_num and received_data['positive_acknowledgement'] == 0:
                    packet_incoming_num += 1
                '''increase slider size'''
                slider_size = 2 * slider_size
            
        except socket.timeout:
            ''' checking congestion '''
            if slider_size > 5:
                slider_size = slider_size // 2
            packet_tag = packet_incoming_num
            continue

    for i in range(30):
        complete_packet['packed_data'] = "sushma_fileends"
        '''set sequence number'''
        complete_packet['data_sequence_number'] = packet_tag + i
        client_connection_socket.sendto(pickle.dumps(complete_packet), (host,port))
        print("client_connection_socket side ")
        print(complete_packet)
        '''close client connection '''
    client_connection_socket.close()
    '''end filepointer'''
    fp.close()
