import socket

def connection(cache)->socket:
    server = socket.socket()
    if cache == '':
        host = input('H:')
    else:
        host = cache
    server.connect((host,42424)) 
    return server, host
        

if __name__ == '__main__':
    cache = ''
    while True:
        server, cache = connection(cache)
        command = input("C: ")
        if command == '.conn':
            server.close()
            cache = ''
        elif command.endswith('.txt'):
            server.send(command.encode())
            with open(command, "wb") as file:
                while True:
                    bytes_reads = server.recv(1024)
                    if not bytes_reads:    
                        break
                    file.write(bytes_reads)
        else:
            server.send(command.encode())
            print ("R: ")
            while True:
                bytes_reads = server.recv(1024)
                if not bytes_reads:    
                    break
                print(str(server.recv(1024).decode("unicode_escape")))
        server.close()