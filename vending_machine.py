from model_snacks import ListOfSnacks
from parsing import Parser

from storage_service import StorageService


class VendingMachine:
    def __init__(self):

        self.client_interface = ClientInterface()
        self.manager_interface = ManagerInterface()
        print('Выберите товар, еслин не знаете его номер нажмите "?"')
        self.start = input()
        self.starting()

    def starting(self):
        if self.start == 'admin':
            print('Доступные действия:\n'
                  'Наполнить магазин,\n'
                  'Посмотреть остатки\n'
                  'Добавить товар')
            comand = input()
            if comand == 'Наполнить магазин':
                self.manager_interface.fill_the_machine()
            elif comand == 'Посмотреть остатки':
                self.manager_interface.leftover_goods()
            elif comand == 'Добавить товар':
                self.manager_interface.add_snacks()
            else:
                print('Недоступная команда')
        elif self.start == '?':
            self.client_interface.see_the_assortment()
        else:
            id_snacks = self.start
            self.client_interface.buy(id_snacks)


class ClientInterface:
    # Класс описывает интерфейс взаимодействия клиента с автоматом
    def __init__(self):
        self.storage_service = StorageService()

    def see_the_assortment(self):
        session = self.storage_service.create_session()
        for item in session.query(ListOfSnacks.id, ListOfSnacks.title, ListOfSnacks.price):
            print(item.id, item.title, item.price)

        print('\n\nВведите номер товара, что бы его купить или "Выход", что бы закончить сеанс')
        self.buy()

    def buy(self, id_snacks=None):
        if id_snacks == None:
            id_snacks = input()
            if id_snacks == 'Выход':
                VendingMachine().starting()
            else:
                session = self.storage_service.create_session()
                q = session.query(ListOfSnacks).get(id_snacks)
                q.quantity -= 1
                session.commit()
                session.close()
                print('Спасибо за покупку!')
                VendingMachine().starting()
        else:
            if id_snacks == 'Выход':
                VendingMachine().starting()
            else:
                session = self.storage_service.create_session()
                q = session.query(ListOfSnacks).get(id_snacks)
                q.quantity -= 1
                session.commit()
                session.close()
                print('Спасибо за покупку!')
                VendingMachine().starting()



class ManagerInterface:
    # Класс описывает интерфейс взаимодействия менеджера с автоматом
    def fill_the_machine(self):
        pars = Parser()
        pars.parse()

    def leftover_goods(self):
        pass

    def add_snacks(self):
        pass
