class AccountException(Exception):
    pass


class Account:
    def __init__(self, name):
        self.name = name
        self.balance = 0

    def make_deposit(self, amount):
        self.balance += amount

    def make_withdrawal(self, amount):
        if amount > self.balance:
            raise AccountException(
                f"Withdrawal amount {amount} is greater than balance {self.balance}"
            )
        self.balance -= amount


class Bank:
    def open_account(self, name):
        return Account(name)
