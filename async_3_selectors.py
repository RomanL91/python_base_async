# асинхронность на callback

import socket
import selectors # более астрактный класс, чем функция select из предыдушего файла
                    # кроссплатформенная. selectors.DefaultSelector() - можно узнать какой используется.

selector = selectors.DefaultSelector() # получаем дефолтный селектор


def server():
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    # selectors выполняет такой же мониторинг над файлами и сокетами(всем что имеет файловый дискриптор)
    # при помощи метода  register - отдаем на мониторинг сокет
    # три аргумента - файловый обьект за которым будем наблюдать, событие которое интересует, любые связанный данные
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
        client_socket, addr = server_socket.accept()
        print(f'Connection from {addr}')
        
        # Cделано тоже самое, что в функции server 
        selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)



def send_message(client_socket):
        request = client_socket.recv(4096)

        if request:                                 
            respnse = f'Hello World\n'.encode()  
            client_socket.send(respnse)
        else:   
            selector.unregister(client_socket) # перед закрытием сокета, снимаем с регистрации(с мониторинга)
            client_socket.close()


def event_loop():
    while True:
        # получаем выборку обьектов, которые готовы для чтения и для записи
        events = selector.select() # (key, events)
        # print(f'events ---->>>> {events}')

        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == "__main__":
    server()
    event_loop()
