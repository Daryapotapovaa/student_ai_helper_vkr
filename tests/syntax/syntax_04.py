# Задание: класс для работы с банковским счётом

class BankAccount
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Пополнение: {amount}")
        else:
            print("Сумма должна быть положительной")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Недостаточно средств")
        elif amount > 0:
            self.balance -= amount
            self.transactions.append(f"Снятие: {amount}")

    def get_history(self):
        return self.transactions

    def __str__(self):
        return f"Счёт {self.owner}: {self.balance} руб."


account = BankAccount("Иван", 1000)
account.deposit(500)
account.withdraw(200)
print(account)
