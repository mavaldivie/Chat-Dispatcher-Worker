import threading as th
import socket
import random
import time
import os


class MessengerClient:
    def __init__(self, serverAddress):
        self.serverAddress = serverAddress
        self.timeStamp = -1
        self.identifier = f'Unknown{random.randint(1, 1000000)}'

        print(f'stablishing connection')
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.socket.connect(self.serverAddress)
        self.socket.settimeout(1)

        th.Thread(target=self.receive).start()

    def receive(self):
        while True:
            try:
                message = self.socket.recv(2048)
            except:
                continue
            print('received message')
            message = self.decodeMessage(message)

            if self.timeStamp == -1 or self.timeStamp + 1 == message['timeStamp']:
                self.timeStamp = message['timeStamp']

                print(message['message'].decode('utf8'))

            self.socket.send(self.encodeMessage(self.timeStamp, True, b''))

    def rename(self, name):
        self.identifier = name

    def send(self, message):
        message = f'{self.identifier}: {message}'
        self.socket.send(self.encodeMessage(self.timeStamp, False, message.encode('utf8')))

    def decodeMessage(self, message):
        dic = {}
        dic['timeStamp'] = int.from_bytes(message[:32], byteorder='big', signed=True)
        dic['isACK'] = bool.from_bytes(message[32:33], byteorder='big')
        dic['message'] = message[33:]
        return dic

    def encodeMessage(self, timesStamp, isACK, message):
        ret = b''
        ret += int.to_bytes(timesStamp, 32, 'big', signed=True)
        ret += bool.to_bytes(isACK, 1, 'big')
        ret += message
        return ret


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--address', type=str, required=True, help='Adress to connect to')
    parser.add_argument('--name', type=str, required=False, help='Name of the client')
    args = parser.parse_args()

    host, port = args.address.split(':')
    if host == '': host = 'localhost'
    port = int(port)
    address = (host, port)

    client = MessengerClient(address)
    if args.name is not None:
        client.rename(args.name)

    while True:
        msg = input()
        client.send(msg)


if __name__ == '__main__':
    main()