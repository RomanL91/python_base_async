# реализация корутин(сопрограмм) с помощью генераторов
# будет много работы в консоле Python
# чтобы открыть консоль в интерактивном режиме используй команду Python3 -i <имя файла>.py 

# кастомное исключение
class CustomExcept(Exception):
    pass


# декоратор для быстрой 
def coroutine(func):
    def inner(*args, **kwargs):
        gen = func(*args, **kwargs)
        gen.send(None)
        return gen
    return inner    


def sungen():
    message = yield
    print(f'subgen receive: {message}')

    # python3 -i <имя файла>.py 
    # >>> g = sungen()                              создание генератора
    # >>> from inspect import getgeneratorstate     импорт функции
    # >>> getgeneratorstate(g)                      просмотр статуса генератора
    # 'GEN_CREATED'                                 статус генератора
    # >>> g.send(None)                              инициация генератора(можно использовать функцию next())
    # >>> getgeneratorstate(g)                      просмотр стауса генератора
    # 'GEN_SUSPENDED'                               статус генератора

    # >>> g.send('...OK...')                        передаем сообщение(строку)
    # subgen receive: ...OK...                      yield принял аргумент от send, записал в переменую и вывел на печать
    # Traceback (most recent call last):
    # File "<stdin>", line 1, in <module>
    # StopIteration


# yield в функции ничего не отдает
# следующий вариат где  yield что-либо отдает
def sungen_1():
    value = 'Ready to accept message'
    message = yield value
    print(f'subgen receive: {message}')

    # >>> g = sungen_1()                            создание генератора
    # >>> g.send(None)                              инициация генератора
    # 'Ready to accept message'                     отданное значение от yield value и остановка выполнения(или возрат управления)
    # >>> g.send('...OK...')                        повторная передача
    # subgen receive: ...OK...                      продолжение выполнения
    # Traceback (most recent call last):
    # File "<stdin>", line 1, in <module>
    # StopIteration
    # >>> 


# определение среднего арифмитического
@coroutine
def average():
    count = 0
    summ = 0
    average = None

    while True:
        try:
            x = yield average
        except StopIteration:
            print('--->>> StopIteration')
        except CustomExcept:
            print('--->>> CustomExcept')
        else:
            count += 1
            summ += x
            average = round(summ / count, 2)

    # >>> g = average()                         создание генератора
    # >>> g.send(None)                          инициализация генератора, вывод не получаем
    # >>> g.send(4)                             
    # 4.0
    # >>> g.send(5)
    # 4.5
    # >>> g.send(10)
    # 6.33
    # >>> g.throw(StopIteration)                прокидываем исключение
    # --->>> StopIteration                      типа полезный код
    # 6.33                                      получаем значение так как цикл не обрывался
        # >>> g.throw(CustomExcept)                 прокидываем исключение
        # --->>> CustomExcept                       типа полезный код


# испльзование return в генераторах
@coroutine
def average_1():
    count = 0
    summ = 0
    average = None

    while True:
        try:
            x = yield average
        except StopIteration:
            print('--->>> StopIteration')
            break
        except CustomExcept:
            print('--->>> CustomExcept')
            break
        else:
            count += 1
            summ += x
            average = round(summ / count, 2)

    return average

    # >>> g = average_1()
    # >>> 
    # >>> g.send(5)
    # 5.0
    # >>> g.send(8)
    # 6.5
    # >>> g.send(2)
    # 5.0
    # >>> g.send(1)
    # 4.0
    # >>> g.send(1)
    # 3.4
    # >>> try:
    # ...     g.throw(StopIteration)            прокидываю исключение
    # ... except StopIteration as e:            отлавливаю его и сохраняю в переменную
    # ...     print(f'Average {e.value}')       вывожу значение return через атрибут value класса StopIteration
    # ... 
    # --->>> StopIteration
    # Average 3.4
    # >>> 

# =======================================================================================
                    # ==== ДЕЛЕГИРУЮЩИЕ ГЕНЕРАТОРЫ ====

def subgen():
    for i in 'ABCD':
        yield i


def delegator_gen(subgen):
    for i in subgen:
        yield i
        

# >>> sg = subgen()
# >>> dg = delegator_gen(sg)
# >>> next(dg)
# 'A'
# >>> next(dg)
# 'B'
# >>> next(dg)
# 'C'
# >>> next(dg)
# 'D'
# >>> next(dg)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# StopIteration

# =======================================================================================

# задача пробросить на обработку данные в подгенератор через делегирующий генератор
# @coroutine                                    yield from сама проинициализирует генератор subgen_1, потому декоратор не нужен
def subgen_1():
    while True:
        try:
            message = yield
        except CustomExcept:                    # задача пробросить обьект исключения в подгенератор
            print('--->>> CustomExcept')
        else:
            print(f'---->>> {message}')

@coroutine
def delegator_gen_1(subgen):
    while True:
        try:
            data = yield
            subgen.send(data)
        except CustomExcept as e:               # задача пробросить обьект исключения в подгенератор
            subgen.throw(e)


@coroutine                    
def delegator_gen_2(subgen):
    yield from subgen                           # заменили одной строкой конструкцию предыдущего примера delegator_gen_1 
                                                # делегирующего генератора, в том числе передача аргументов и исключений

# =======================================================================================

def subgen_3():
    while True:
        try:
            message = yield
        except StopIteration:                    # задача пробросить обьект исключения в подгенератор
            print('--->>> StopIteration')
            break
        else:
            print(f'---->>> {message}')
    return '=== RETURN VALUE ==='


@coroutine                    
def delegator_gen_3(subgen):
    result = yield from subgen                  # await
    print(f'result --->>> {result}')
