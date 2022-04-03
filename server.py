#!/usr/bin/env python3
import sys
import os
import socket
import concurrent.futures
import time
import psutil

conn = None
s = None

PORT = 7777
HOSTNAME = '0.0.0.0'
EXIT_MESSAGE = 'quitX'
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


def make_connection(s):
    while True:
        try:
            conn, addr = s.accept()
            print(f'[*]Connected to {addr}')
            return conn
        except:
            print(f"[*]Error connecting to a client!")
            sys.exit()


def send_msg():
    while True:
        if conn or not exit:
            try:
                msg = input(' ->')
                conn.send(msg.encode('utf-8'))
                if msg == EXIT_MESSAGE:
                    exit_program()
                    break
            except Exception as e:
                print(f'[*]Error sending msg! {str(e)}')
                exit_program()
                return
        else:
            break


def recv_msg():
    while True:
        if conn or not exit:
            msg ='ROXXi!@'
            try:
                msg = conn.recv(2048).decode('utf-8')
                if msg == EXIT_MESSAGE:
                    exit_program()
                    return
            except:
                print("[*]Error receiving msg!")
                exit_program()
                return
            if not msg == 'ROXXi!@':
                print(f'\n{RED}{msg}{ENDC}\n')

        else:
            break


def exit_program():
    current_system_pid = os.getpid()
    ThisSystem = psutil.Process(current_system_pid)
    ThisSystem.terminate()


def messenger():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(send_msg)
        executor.submit(recv_msg)


def main():
    global conn
    global s
    global exit

    exit = False

    try:
        s = make_socket()
        conn = make_connection(s)
        messenger()
    except Exception as e:
        exit_program()
        print(str(e))
        conn.close()
        s.close()

try:
    main()
except:
    if conn:
        conn.send(EXIT_MESSAGE.encode('utf-8'))
    exit_program()
