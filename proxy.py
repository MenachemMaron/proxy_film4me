'''
proxy for 'Film4me' to fix problems with it
v1.0.0
created by Menachem Maron :)
'''

import socket


LISTEN_PORT = 9090
LISTEN_ADDR = '127.0.0.111'
REQUEST_PORT = 92
REQUEST_ADDR = '54.71.128.194'


# get client request and then get reponse from server [using getServerResponse()]
def performClientRequest():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_sock:
        listen_server_data = (LISTEN_ADDR, LISTEN_PORT)
        # print(listen_server_data)
        listening_sock.bind(listen_server_data)

        listening_sock.listen(1)

        client_soc, client_address = listening_sock.accept()
        # print(client_soc, client_address)

        client_msg = (client_soc.recv(1024)).decode()
        # print(client_msg)

        if(banFrance(client_msg)):
            server_response = getServerResponse(client_msg)
            client_soc.send((server_response).encode())
        else:
            client_soc.send('ERROR#"France is banned!"'.encode())


# get response to request from server
def getServerResponse(client_msg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as requesting_sock:
        request_server_data = (REQUEST_ADDR, REQUEST_PORT)
        # print(request_server_data)
        requesting_sock.connect(request_server_data)

        request_msg = client_msg
        requesting_sock.sendall((request_msg).encode())

        server_msg = (requesting_sock.recv(1024)).decode()

        fixed_server_msg = fixResponseMistakes(server_msg)
        # print(fixed_server_msg)

        return fixed_server_msg


# fix mistakes in response
def fixResponseMistakes(server_msg):
    # mistake 1: image link is incorrect
    fixed_server_msg = (server_msg[:server_msg.find('jpg')] + '.' + server_msg[server_msg.find('jpg'):])

    # mistake 2: sometimes error message is in the wrong syntax
    split_msg = fixed_server_msg.split('#')
    if split_msg[0] != ('MOVIEDATA' or 'ERROR'):
        split_msg[0] = 'ERROR'
    fixed_server_msg = '#'.join(split_msg)

    # mistake 3: ?

    return fixed_server_msg


def banFrance(client_request):
    split_client_request = client_request.split(':')
    if split_client_request[-1].upper() == 'FRANCE':
        return False
    return True


# main
def main():
    while True:
        performClientRequest()


if __name__ == '__main__':
    main()
