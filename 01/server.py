#!/usr/bin/python3

import socket
import threading
from typing import List, Set

from config import getConfig, isManager


class ThreadedServer(object):
    def __init__(self, host, port, stop):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.data = {}
        self.threads: List[threading.Thread] = []
        self.stop = stop
        self.timeOut = getConfig("timeOut")
        self.auth: Set[int] = set()

    def listen(self):
        self.sock.listen(5)
        print(f"Listening on....{self.host}:{self.port}")
        while True:
            client, address = self.sock.accept()
            client.settimeout(self.timeOut)
            t = threading.Thread(target=self.listenToClient,
                                 args=(client, address))
            self.threads.append(t)
            t.start()

    def listenToClient(self, client, address):
        print(address, "connected")
        a = address[1]
        size = 1024
        self.data[a] = {}
        while True:
            try:
                data: str = client.recv(size).decode()
                if data and data != "exit" and not self.stop():
                    arr = data.split(" ")
                    response = ""
                    if(arr[0] == "get"):
                        if(len(arr) < 2):
                            response = "Lesser number of arguments than expected"
                        else:
                            response = self.processCommands(a, arr[0], arr[1])
                    elif(arr[0] in ["put", "auth"]):
                        if(len(arr) < 3):
                            response = "Lesser number of arguments than expected"
                        else:
                            response = self.processCommands(
                                a, arr[0], (arr[1], arr[2]))
                    elif(arr[0] in ["manage"]):
                        if(len(arr) < 4):
                            response = "Lesser number of arguments than expected"
                        else:
                            response = self.processCommands(
                                a, arr[0],
                                (arr[1], arr[2], (arr[3], False if len(arr) < 5 else arr[4])))
                    else:
                        response = "Illegal command"
                    client.send(response.encode())
                else:
                    client.send("ok disconnect".encode())
                    raise Exception('Client disconnected')
            except Exception as e:
                # print(e)
                if a in self.auth:
                    self.auth.remove(a)
                del self.data[a]
                print(address, "disconnected")
                if(e == "Client disconnected"):
                    try:
                        client.send("ok disconnect".encode())
                    except:
                        pass
                client.close()
                return False

    def processCommands(self, a: int, command: str, op, managed=False) -> str:
        if managed and a not in self.data:
            return "Address not present"
        if(command == "get"):
            return self.data[a].get(op) if (op in self.data[a]) else "<blank>"
        elif(command == "put"):
            self.data[a][op[0]] = op[1]
            return f'Successfully set {op[0]} as {op[1]}'
        elif(command == "auth"):
            if isManager(op[0], op[1]):
                self.auth.add(a)
                return "Authentication success"
            else:
                if a in self.auth:
                    self.auth.remove(a)
                return "Failed to elevate privilege"
        elif(command == "manage"):
            if(a in self.auth):
                try:
                    accessAddress = int(op[0])
                    assert op[1] in ["get", "put"]
                except Exception:
                    return "Illegal structure of command"
                if(op[1] == "get"):
                    if(len(op) < 3):
                        return "Lesser number of arguments than expected"
                    else:
                        return self.processCommands(accessAddress, op[1], op[2][0], True)
                else:
                    if(len(op) < 3 or not op[2][1]):
                        return "Lesser number of arguments than expected"
                    else:
                        return self.processCommands(
                            accessAddress, op[1], (op[2][0], op[2][1]), True)
            else:
                return "Illegal access"
        return "Illegal command"


if __name__ == "__main__":
    host_name = getConfig("serverHostName")
    port_num = getConfig("serverPort")
    stop_threads = False

    server = ThreadedServer(host_name, port_num, lambda: stop_threads)

    try:
        server.listen()
    except KeyboardInterrupt:
        stop_threads = True
        print(
            f"\nStopping..waiting for clients to disconnect...may wait for at max {server.timeOut} seconds")
        for thread in filter(lambda t: t.is_alive(), server.threads):
            thread.join()
        print("Bye 👋👋👋👋👋👋")
