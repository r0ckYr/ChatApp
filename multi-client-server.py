#!/usr/bin/env python3
import sys
import os
import socket
import concurrent.futures
import time
import psutil


connections = []
addresses = []
s = None
conLength = 0

PORT = 7777
HOSTNAME = '0.0.0.0'
EXIT_MESSAGE = 'quitX'
TESTING_MESSAGE = 'ROXXXi!@'.encode('utf-8')
MAX_CONNECTIONS = 5

GREEN = '\033[92m'
RED = '\033[93m'
ENDC = '\033[0m'

def make_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except Exception as e:
        print("[*]Error making socket object")
        sys.exit()

    try:
        s.bind((HOSTNAME, PORT))
    except Exception as e:
        print('[*]Error binding host and port '+str(e))
        sys.exit()

    try:
        s.listen(MAX_CONNECTIONS)
        print("[*]Started listener on port 7777")
    except Exception as e:
        print('[*]Error starting listener on port 7777'+str(e))
        sys.exit()

    return s


def make_connection():
    while True:
        try:
            conn, addr = s.accept()
            print(f'[*]Connected to {addr}')
            connections.append(conn)
            addresses.append(addr)
        except:
            print(f"[*]Error connecting to a client!")
            exit_program()


def is_command(msg):
    try:
        exclude = []
        if msg == 'listall':
            for i in range(len(connections)):
                try:
                    connections[i].send(TESTING_MESSAGE)
                    connections[i].send(TESTING_MESSAGE)
                    print(str(addresses[i]))
                except:
                    exclude.append(connections[i])

            for ex in exclude:
                remove_client(ex)

            return True

        return False
    except Exception as e:
        print('[*]Error in is_command! '+ str(e))



def check_connection(conn):
    try:
        conn.send(TESTING_MESSAGE)
        conn.send(TESTING_MESSAGE)
        return True
    except:
        return False


def send_msg():
    while True:
        try:
            msg = input(' ->')
            if is_command(msg):
                continue
            for conn in connections:
                conn.send(msg.encode('utf-8'))
            if msg == EXIT_MESSAGE:
                exit_program()
                break
        except Exception as e:
            print(f'[*]Error sending msg! {str(e)}')
            remove_client(conn)


def send_received_msg(exclude, msg):
    try:
        for conn in connections:
            if not conn == exclude:
                conn.send(msg.encode('utf-8'))
    except Exception as e:
        print(f'[*]Error sending msg r! {str(e)}')


def recv_msg(conn):
    try:
        print('recv_start')
        while True:
            msg = TESTING_MESSAGE
            if check_connection(conn):
                try:
                    msg = conn.recv(2048).decode('utf-8')
                    if msg == EXIT_MESSAGE:
                        remove_client(conn)
                        sys.exit()
                except Exception as e:
                    print("[*]Error receiving msg! "+str(e))
                    remove_client(conn)
                    sys.exit()
                if not msg == TESTING_MESSAGE:
                    print(f'\n{RED}{msg}{ENDC}\n')
                send_received_msg(conn, msg)
            else:
                remove_client(conn)
                sys.exit()
    except Exception as e:
        print('[*]Error in recv_msg '+ str(e))


def remove_client(conn):
    try:
        addresses.remove(addresses[connections.index(conn)])
    except Exception as e:
        print('[*]Error in remove_client '+str(e))

    try:
        connections.remove(conn)
    except Exception as e:
        print('[*]Error in remove_client '+str(e))


def exit_program():
    try:
        for conn in connections:
            conn.send(EXIT_MESSAGE.encode('utf-8'))
    except:
        pass
    current_system_pid = os.getpid()
    ThisSystem = psutil.Process(current_system_pid)
    ThisSystem.terminate()


def receiver():
    conLength = 0
    new = []
    try:
        with concurrent.futures.ThreadPoolExecutor() as executorP:
            while True:
                if (len(connections) - conLength) >  0:
                    new = connections[conLength:]
                    executorP.map(recv_msg, new)
                    conLength = len(connections)
    except Exception as e:
        print('[*]Error in receiver '+str(e))


def start():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(make_connection)
        executor.submit(send_msg)
        executor.submit(receiver)


def main():
    global s
    global conn

    try:
        s = make_socket()
        start()
    except Exception as e:
        print(str(e))
        for conn in connections:
            conn.close()
        s.close()
        exit_program()


try:
    main()
except:
    exit_program()
