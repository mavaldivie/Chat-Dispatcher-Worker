import threading as th
import socket
import time

class MessengerServer:
    def __init__(self, address):
        self.address = address
        self.messages = []

        self.expACK = {}
        self.semaphore = th.Semaphore()

        self.socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
        self.socket.bind(self.address)

        print('starting to listen')
        self.socket.listen()

        th.Thread(target=self.getIncomingConnections).start()

    def getIncomingConnections(self):
        while True:
            client, address = self.socket.accept()
            print(f'accepted conection from {address}')
            self.enqueue(f'Server: {address} has joined the net'.encode('utf8'))

            self.semaphore.acquire()
            self.expACK[address] = len(self.messages)
            self.semaphore.release()

            th.Thread(target=self.manageClient, args=(client, address,)).start()
            th.Thread(target=self.broadcast, args=(client, address,)).start()

    def manageClient(self, client, address):
        while True:
            message = client.recv(1024)
            message = self.decodeMessage(message)

            if message['isACK'] and message['timeStamp'] == self.expACK[address]:
                self.semaphore.acquire()
                self.expACK[address] += 1
                print(f'ACK from {address}')
                self.semaphore.release()

            elif not message['isACK']:
                self.enqueue(message['message'])
                print(f'message from {address}')

    def enqueue(self, message):
        message = self.encodeMessage(len(self.messages), False, message)
        self.messages.append(message)

    def broadcast(self, client, address):
        while True:
            if self.expACK[address] < len(self.messages):
                client.send(self.messages[self.expACK[address]])
            time.sleep(1)

    def decodeMessage(self, message):
        dic = {}
        dic['timeStamp'] = int.from_bytes(message[:32], byteorder='big')
        dic['isACK'] = bool.from_bytes(message[32:33], byteorder='big', signed=True)
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
    parser.add_argument('--address', required=True, help='Adress to bind')
    args = parser.parse_args()

    host, port = args.address.split(':')
    if host == '': host = 'localhost'
    port = int(port)
    address = (host, port)

    server = MessengerServer(address)


if __name__ == '__main__':
    main()