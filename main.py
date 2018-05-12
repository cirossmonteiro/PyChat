import socket
import sys
import multiprocessing as mp
import time
import psycopg2 as psy

print("server is on!")
HOST = None
PORT = 50007


class Connection:

    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__process = []

    def __checkin_room(self, room, passw, user, ip, port):
        print("main:checkin_room")
        conn = psy.connect("host=localhost dbname=pychat user=root password=codigo64")
        cr = conn.cursor()
        cr.execute("select * from rooms where name = '%s';"%(room))
        row = cr.fetchone()
        print(row)
        print("main: here")
        
        if row == None: # room doesn't exist
            cr.execute("insert into rooms (name,hashpw) values ('%s','%s');"%(room,passw))
            cr.execute("select id from rooms where name = '%s';"%(room))
            rid = cr.fetchone()[0]
            cr.execute("insert into users (rid,name,ip,port) values (%d,'%s','%s',%d);"%(rid,user,ip,port))
            print("new room")
            return 1 # room created
        
        else:
            # checking password
            cr.execute("select id from rooms where name = '%s' and hashpw = '%s';"%(room,passw))
            rid = cr.fetchone()
            
            if rid == None:
                print("wrong password for room")
                return 0 # wrong password
            
            else:
                # by now, the room is right
                cr.execute("select ip, port from users where rid = %d and ip != '%s';"%(row[0],ip))
                row = cr.fetchall()
                if row == None:
                    print("no users in room")
                    r = []
                else:
                    print("other users in room")
                    r = row # correct password: return ip and ports of users from room
                cr.execute("insert into users (rid,name,ip,port) values(%d,'%s','%s',%d);"%(rid[0],user,ip,port))
                cr.execute("commit;")
                cr.execute("select * from users where name = '%s';"%(user))
                print("adding user: ",cr.fetchone())
                return r
            
    
    def __start(self):
        
        print("Socket's being checked.")
        while True:
            s = None
            for res in socket.getaddrinfo(self.__host, self.__port, socket.AF_UNSPEC,
                                          socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
                af, socktype, proto, canonname, sa = res
                try:
                    s = socket.socket(af, socktype, proto)
                except OSError as msg:
                    s = None
                    continue
                try:
                    s.bind(sa)
                    s.listen(1)
                except OSError as msg:
                    s.close()
                    s = None
                    continue
                break
    ##        if s is None:
    ##            print('could not open socket')
    ##            sys.exit(1)
            if s != None:
                conn, addr = s.accept()
                try:
                    ip, port = addr
                except:
                    print("problem: ",addr)
                    s.close()
                    s = None
                    continue
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        cmd = eval(data.decode("utf-8"))
                        if cmd[0] == "checkin":
                            ret = self.__checkin_room(cmd[1],cmd[2],cmd[3],ip,port)
                            conn.sendall(str(ret).encode("utf-8"))
                s.close()
            time.sleep(1)

    def start(self):

        self.__process.append(mp.Process(target = self.__start))
        self.__process[-1].start()
        print("process started...")
        time.sleep(1)
        print("Command line ready for use.")
        
        while True:
            cmd = input()
            if cmd == "end":
                for p in self.__process:
                    p.terminate()
                break
        print("Program's over.")

daily = Connection(HOST, PORT)
daily.start()

"""
def checkin_room(room, passw, user, ip, port):
    print("main:checkin_room")
    conn = psy.connect("host=localhost dbname=pychat user=root password=codigo64")
    cr = conn.cursor()
    cr.execute("select * from rooms where name = '%s';")
    row = cr.fetchone()
    print("main: here")
    if row == None:
        cr.execute("insert into rooms (name,hashpw) values ('%s','%s');"%(room,passw))
        cr.execute("select id from rooms where name = '%s';"%(room))
        rid = cr.fetchone()[0]
        cr.execute("insert into users (rid,name,ip,port) values (%d,'%s','%s',%d);"%(rid,user,ip,port))
        print("new room")
        return 1 # room created
    else:
        cr.execute("select * from rooms where name = '%s' and hashpw = '%s';"%(room,passw))
        row = cr.fetchone()
        if row == None:
            print("wrong password for room")
            return 0 # wrong password
        else:
            cr.execute("select ip, port from users where rid = %d and ip != '%s';"%(row[0],ip))
            row = cr.fetchall()
            if row == None:
                print("no users in room")
                return []
            print("other users in room")
            return row # correct password: return ip and ports of users from room
    

def check_socket():
    print("Socket's being checked.")
    while True:
        s = None
        for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                                      socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
            except OSError as msg:
                s = None
                continue
            try:
                s.bind(sa)
                s.listen(1)
            except OSError as msg:
                s.close()
                s = None
                continue
            break
##        if s is None:
##            print('could not open socket')
##            sys.exit(1)
        if s != None:
            conn, addr = s.accept()
            try:
                ip, port = addr
            except:
                print("problem: ",addr)
                s.close()
                s = None
                continue
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    cmd = eval(data.decode("utf-8"))
                    if cmd[0] == "checkin":
                        ret = checkin_room(cmd[1],cmd[2],cmd[3],ip,port)
                        conn.sendall(str(ret).encode("utf-8"))
            s.close()
        time.sleep(1)
                    

process.append(mp.Process(target = check_socket))
process[-1].start()
print("process started...")
time.sleep(1)
print("Command line ready for use.")
while True:
    cmd = input()
    if cmd == "end":
        for p in process:
            p.terminate()
        break
print("Program's over.")
"""
