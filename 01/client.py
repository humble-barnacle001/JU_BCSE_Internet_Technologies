#!/usr/bin/python3
import socket

from config import getConfig

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = getConfig("serverHostName")
    port = getConfig("serverPort")
    sock.connect((host, port))
    print(sock)
    try:
        while True:
            data = input("input: ")
            sock.send(data.encode())
            resp = sock.recv(1024).decode()
            if resp == "ok disconnect":
                raise Exception('disconnect')
            print("response:", resp)
    except (Exception, KeyboardInterrupt) as e:
        if(e.__class__.__name__ == "BrokenPipeError"):
            print("Socket hang up, bye 👋👋")
            exit(1)
        try:
            print("\ndisconnecting.....")
            if e != "disconnect":
                sock.send("exit".encode())
                sock.recv(1024)
            sock.close()
        except:
            pass
        finally:
            print("Bye 👋")
