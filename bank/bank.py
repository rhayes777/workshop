class AccountException(Exception):
    pass


class Account:
    def __init__(self, name):
        self.name = name
        self._balance = 0
        self.overdraft_limit = 0

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, balance):
        if balance < -self.overdraft_limit:
            raise AccountException(
                f"Negative balance {balance} is not allowed"
            )
        self._balance = balance

    @property
    def available_funds(self):
        return self.overdraft_limit + self.balance

    def make_deposit(self, amount):
        self.balance += amount

    def make_withdrawal(self, amount):
        self.balance -= amount


class Bank:
    def open_account(self, name):
        return Account(name)
