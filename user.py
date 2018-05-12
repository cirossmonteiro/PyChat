import socket, sys, time

HOST = "140.82.27.108"
PORT = 50007

ROOM = "ufrj"
PASSW = "fundao"
USER = "coresh"

friends = []

class Connection():

    def __init__(self, host, port = None):
        
        self.__host = host
        self.__port = port
        self.__skt = None

    def test(self):
        """implementar teste de conexão"""
        return 

    def __exit__(self):
        
        if self.__skt != None:
            print("inside exit method")
            self.__skt.close()
            del self.__skt

    def __send_cmd(self, cmd):
        
        print("client: here1")
        
        for i in range(20):
            
            for res in socket.getaddrinfo(self.__host, self.__port, socket.AF_UNSPEC, socket.SOCK_STREAM):
                af, socktype, proto, canonname, sa = res
                
                try:
                    self.__skt = socket.socket(af, socktype, proto)
                    
                except socket.error as msg:
                    continue
                
                try:
                    self.__skt.connect(sa)
                    
                except socket.error as msg:
                    self.__skt.close()
                    self.__skt = None
                    continue
                
                break
            
            if self.__skt == None:
                print("qq")
                time.sleep(1)
                
            else:
                break
            
        if self.__skt is None:
            print ('could not open socket')
            return
        
        print("client: here2")
        self.__skt.sendall(bytearray(str(cmd).encode("utf-8")))
        print("here3")
        data = self.__skt.recv(1024)
        print("here4")
        self.__skt.close()
        print("closed")
        return eval(data.decode("utf-8"))
    

    def checkin_room(self, room, passw, user):
        cmd = ["checkin", room, passw, user]
        ret = self.__send_cmd(cmd)
        
        if ret == 1:
            print("Room's been created.")

        elif ret == 0:
            print("Wrong password.")

        elif type(ret) == list:
            if ret == []:
                print("Only you in the room.")
            else:
                friends += ret

        else:
            print("Can't read result.")

"""
def send_server(host, port, cmd):
    s = None
    print("client: here1")
    for i in range(20):
        for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
            except socket.error as msg:
                s = None
                continue
            try:
                s.connect(sa)
            except socket.error as msg:
                s.close()
                s = None
                continue
            break
        if s == None:
            print("qq")
            time.sleep(1)
        else:
            break
    if s is None:
        print ('could not open socket')
        return
    print("client: here2")
    s.sendall(bytearray(str(cmd).encode("utf-8")))
    print("here3")
    data = s.recv(1024)
    print("here4")
    s.close()
    print("closed")
    return eval(data.decode("utf-8"))


def checkin_room(room, passw, user):
    cmd = ["checkin", room, passw, user]
    ret = send_server(HOST, PORT, cmd)
    
    if ret == 1:
        print("Room's been created.")

    elif ret == 0:
        print("Wrong password.")

    elif type(ret) == list:
        if ret == []:
            print("Only you in the room.")
        else:
            friends += ret

    else:
        print("Can't read result.")
        
checkin_room(ROOM, PASSW, USER)
"""

ligar = Connection(HOST, PORT)
ligar.checkin_room(ROOM, PASSW, USER)
