import os.path
from parsing import Parser
from storage_service import StorageService
from model_snacks import ListOfSnacks


class VendingMachine:
    def __init__(self, start=None):

        self.client_interface = ClientInterface()
        self.manager_interface = ManagerInterface()
        if start == None:
            print('Выберите товар, еслин не знаете его номер нажмите "?"')
            start = input()
            self.starting(start)
        else:
            print()
            self.starting(start)

    def starting(self, start=None):
        if start == 'admin':
            print('Введите номер команды:\n'
                  '1. Наполнить магазин,\n'
                  '2. Посмотреть остатки\n'
                  '3. Добавить товар\n'
                  '4. Удалить товар\n'
                  '5. Выйти из серв. режима')
            comand = input()
            if comand == '1':
                self.manager_interface.fill_the_machine()
            elif comand == '2':
                self.manager_interface.leftover_goods()
            elif comand == '3':
                self.manager_interface.add_snacks()
            elif comand == '4':
                self.manager_interface.delete_snacks()
            elif comand == '5':
                VendingMachine().starting()
            else:
                print('Недоступная команда')
        elif start == '?':
            self.client_interface.see_the_assortment()
        else:
            id_snacks = start
            self.client_interface.buy(id_snacks)


class ClientInterface:
    # Класс описывает интерфейс взаимодействия клиента с автоматом
    def __init__(self):
        self.storage_service = StorageService()

    def see_the_assortment(self):
        if os.path.exists('list_of_snacks.db'):
            session = self.storage_service.create_session()
            for item in session.query(ListOfSnacks.id, ListOfSnacks.title, ListOfSnacks.price):
                print(item.id, item.title, item.price)

            print('\n\nВведите номер товара, что бы его купить или "Выход", что бы закончить сеанс')
            self.buy()
        else:
            print('Магазин пуст, обратитесь к менеджеру')
            VendingMachine().starting()

    def buy(self, id_snacks=None):
        if os.path.exists('list_of_snacks.db'):
            if id_snacks == None:
                id_snacks = input()
                if id_snacks == 'Выход':
                    VendingMachine().starting()
                elif id_snacks == 'admin':
                    VendingMachine('admin').starting()
                else:
                    session = self.storage_service.create_session()
                    q = session.query(ListOfSnacks).get(id_snacks)
                    q.quantity -= 1
                    session.commit()
                    session.close()
                    print('Спасибо за покупку!')
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
            print('Магазин пуст, обратитесь к менеджеру')
            VendingMachine().starting()


class ManagerInterface:
    # Класс описывает интерфейс взаимодействия менеджера с автоматом
    def __init__(self):
        self.storage_service = StorageService()

    def fill_the_machine(self):
        pars = Parser()
        pars.parse()
        print('Магазин наполнен!')
        VendingMachine('admin').starting()

    def leftover_goods(self):
        session = self.storage_service.create_session()
        for item in session.query(ListOfSnacks.id, ListOfSnacks.title, ListOfSnacks.quantity):
            print(item.id, item.title+'\n', 'На остатке: '+str(item.quantity)+'шт')
        VendingMachine('admin').starting()

    def add_snacks(self):
        print('Введите "Название" "Цену в ₽" "Количество"')
        session = self.storage_service.create_session()
        title, price, quantity = map(str, input().split())
        list_of_snacks = ListOfSnacks(title, price + "₽", quantity)
        session.add(list_of_snacks)
        session.commit()
        session.close()
        print('Товар добавлен!')
        VendingMachine('admin').starting()

    def delete_snacks(self):
        print('Введите ID товара которого хотите удалить:')
        id_snacks = input()
        session = self.storage_service.create_session()
        q = session.query(ListOfSnacks).get(id_snacks)
        session.delete(q)
        session.commit()
        session.close()
        print('Товар удален!')
        VendingMachine('admin').starting()
