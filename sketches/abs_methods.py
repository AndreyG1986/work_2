from abc import ABC, abstractmethod

class Employee(ABC):

    @abstractmethod
    def work(self):
        pass

class Developer(Employee):

    def work(self):
        print("Пишет код")

class Accountant(Employee):

    def work(self):
        print("Считает зарплату")

# Удалите эти строки:
# emp = Employee()
# emp.work()

dev = Developer()
acc = Accountant()

dev.work()  # Выведет: Пишет код
acc.work()  # Выведет: Считает зарплату