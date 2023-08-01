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

