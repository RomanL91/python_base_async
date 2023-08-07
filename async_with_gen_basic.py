from time import sleep


queue = []

def counter():
    counters = 0

    while True:
        print(f'===== def counter --->>> {counters} =====')
        counters += 1
        yield


def printer():
    counter = 0

    while True:
        if counter % 3 == 0:
            print(f'===== def printer =====')
        counter += 1
        yield


def main():
    # карусель
    while True:
        gen = queue.pop(0)
        next(gen)
        queue.append(gen)
        sleep(.5)           # блок метод, для того чтобы успеть анализировать вывод в консоле


if __name__ == '__main__':
    gen_counter = counter()
    queue.append(gen_counter)
    gen_printer = printer()
    queue.append(gen_printer)

    main()