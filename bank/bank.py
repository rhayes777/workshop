class AccountException(Exception):
    pass


class Account:
    def __init__(
            self,
            name,
            bank
    ):
        self.name = name
        self._balance = 0
        self.overdraft_limit = 0
        self.bank = bank

    def step(self):
        self._balance *= (1 + self.bank.interest_rate)

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
        self._balance += amount

    def make_withdrawal(self, amount):
        self.balance -= amount


class StudentAccount(Account):
    def step(self):
        if self.balance > 0:
            super().step()


class Bank:
    def __init__(
            self,
            interest_rate=0.1
    ):
        self.interest_rate = interest_rate
        self.accounts = list()

    def open_account(self, name):
        account = Account(
            name,
            bank=self
        )
        self.accounts.append(
            account
        )
        return account

    def step(self):
        for account in self.accounts:
            account.step()
