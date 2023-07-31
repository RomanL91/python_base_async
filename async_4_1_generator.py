# асинхронность на генераторах, применение к сокетам.
# что у нас есть? - серверный и клиентский сокеты, у клиентского 2 состояния: чтение и запись(отправка).
# методы accept(), recv(), send() - блокирующие.
# исходя из этого вытекают 2 задачи: 1)определить какие сокеты уже готовы для чения/записи и  вызвать у них соотвествующие методы
# 2)нужен механим для переключения управления между функциями server и client
# 
# первую задачу решаем через seletc, а для решения 2 задачи - генераторы и событийный цикл
# 
# пометим что возращаем через инструкцию yield. сделано так, потому что у клиентского сокета 2 состояния.
# 
# расставили инструкию yield в определенных местах. Этим добились того, что перед блокирующими
# методами вернем контроль выполнения программы и не "зависаем". то есть выполнять блокирующий метод
# будем, только при следующем выполнении функции next(), то есть тогда, когда будем готовы выполнить этот  
# метод без задержек. Отдадим данный кортеж в функию select, которая сделает выборку тех сокетов, которые 
# уже готовы и  вызовем функцию next у соотвествующего генератора, чтобы продолжить исполнение.


import socket

from select import select


tasks = []                                              # используем простой список

to_read = {}
to_write = {}


def server():
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        yield ('read', server_socket)                   # пометили флагом "read" 
        client_socket, addr = server_socket.accept() 
        print(f'Connection from {addr}')
        tasks.append(client(client_socket))


def client(client_socket):
    while True:
        yield ('read', client_socket)                   # пометили флагом "read" 
        request = client_socket.recv(4096)

        if not request:
            break
        else:
            respnse = f'Hello World\n'.encode()
            yield ('write', client_socket)              # пометили флагом "write" 
            client_socket.send(respnse)
    
    client_socket.close()


def event_loop():
    while any([tasks, to_read, to_write]):              # если что-то из списка не пустое -> True
        while not tasks:                                # обеспечивает событийный цикл субстратом для работы
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])
                                                        # select дает выборку фаловых дескрипторов, готовых для чтения/записи
            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.pop(0)
            reason, sock = next(task)

            if reason == 'read':
                to_read[sock] = task
            if reason == 'write':
                to_write[sock] = task
        except StopIteration:
            pass

if __name__ == "__main__":
    tasks.append(server())
    event_loop()
