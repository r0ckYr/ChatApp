#!/usr/bin/env python3
import sys
import os
import socket
import time
import concurrent.futures
import psutil


PORT = 7777
SERVER = 'YOUR_SERVER_IP'
EXIT_MESSAGE = 'quitX'

GREEN = '\033[92m'
RED = '\033[93m'
ENDC = '\033[0m'


def make_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        print('[*]Error makeing socket object')
        sys.exit()

    return s


def make_connection(s):
    while True:
        try:
            s.connect((SERVER, PORT))
            print(f"[*]Connected to {SERVER}:{PORT}")
            break
        except:
            time.sleep(5)


def send_msg():
    while True:
        if s and not exit:
            try:
                msg = input(' ->')
                s.send(msg.encode('utf-8'))
                if msg == EXIT_MESSAGE:
                    exit_program()
                    break
            except Exception as e:
                exit_program()
                print("[*]Error sending message to server")
                break
        else:
            break


def recv_msg():
    while True:
        msg = "ROXXXi!@"
        if s and not exit:
            try:
                msg = s.recv(1024).decode('utf-8')
                if msg == EXIT_MESSAGE:
                    exit_program()
                    return
            except Exception as e:
                print("[*]Error receiving msg!")
                exit_program()
                return
            if 'ROXXXi!@' not in msg:
                print(f'\n{RED}{msg}{ENDC}\n\n ->', end='')
        else:
            break


def exit_program():
    current_system_pid = os.getpid()
    ThisSystem = psutil.Process(current_system_pid)
    ThisSystem.terminate()


def messenger():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(recv_msg)
        executor.submit(send_msg)


def main():
    global s
    global exit
    exit = False

    s = make_socket()
    make_connection(s)
    messenger()

try:
    main()
except:
    if s:
        s.send(EXIT_MESSAGE.encode('utf-8'))
    exit_program()
