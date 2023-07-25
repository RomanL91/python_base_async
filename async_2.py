# создание обычного событийного цикла 

import socket
from select import select   # системная функция, которая отслеживает состояние изменения
                            # файловых объектов из сокетов. Select работает с любыми обьетами
                            # у которых есть метод  .fileno() - он возращает файловый дискиптоа(номер файла)

to_monitor = [] # переменная для мониторинга(пустой список)


server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen()


def accept_connection(server_socket):
    # while True: # изюавляемся от цикла, так как мы уже будем в цикле событий event loop
        client_socket, addr = server_socket.accept()
        print(f'Connection from {addr}')
        # send_message(client_socket)
        to_monitor.append(client_socket) # добавялем в список монитора клиентский сокет



def send_message(client_socket):
    # while True: # так же убираем цикл, так как будем в цикле в event loop
        request = client_socket.recv(4096)

        if request:                                 # даанный блок изменяем, убираем операто break 
            respnse = f'Hello World\n'.encode()     # так как нет никакого цикла
            client_socket.send(respnse)
        else:    
            client_socket.close()


def event_loop():
    while True:
        ready_to_read, _, _ = select(to_monitor, [], []) # передаем для отслеживания в select список сокетов
                                                            # и когда в их входящем буфере что-либо будет ->
                                                            # получим в переменную
                                                            # read,  write, errors 
        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else: # предпологаем, что сокет может быть клиенстким, так как строка 22
                send_message(sock)

if __name__ == "__main__":
    to_monitor.append(server_socket)
    event_loop()
    # accept_connection(server_socket=server_socket)


# код с предыдущего файла разнесли по функция.
# работает он так же синхронно.
# из за наличия вызова функции в 16 строке send_message
# имеется связанность, от нее нужно уйти => закоментируем.
# 
# стоит отметить основные моменты -> код изменен так, по сравнению с предыдущей
# версией, что сначала, все было разнесено по функциям, и одно из самых важных,
# функции имеют минимальную связанность. Другими словами, мы можем вызывать эти функции
# в любом порядке. В новой функции event loop и есть управление, какая функция должна сейчас работать.
# Стоит так же обратить внимание на архитектуру данной программы, как переместились циклы к примеру.
