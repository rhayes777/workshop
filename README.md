# Testing Tutorial

An amazing tool for achieving well written code is Test Driven Development. 

Whilst TDD means that your code is well tested so you can be confident it does what you think it should, there's loads more advantages:

- It means you can write as fast as you can without having to deal with a bunch of bugs at the end before your code works.
- It means that you have to understand what you are coding before you start writing it rather than afterwards.
- The code you write ends up better structured. It has a clean interface. It’s modular.
- Code can be refactored without fear of breaking it by you and by people you collaborate with.

I'm going to show how I would approach writing some software with an example I hope is pretty familiar to everyone - bank accounts. 

I'll use [pytest](https://docs.pytest.org/en/6.2.x/) to do this. Python comes with a default test framework called unittest but I prefer pytest. You may need to install pytest `pip install pytest` and set it as the default test running for your IDE.

# Basics

Ok so let's try to model a bank with some bank accounts. What might that look like? I'll start by writing a test of how I think I might want my API to look.

> API = Applications Programming Interface. That's the surface of the code that we're going to present to the world.

```python
from bank.bank import Bank

def test_open_account():
    bank = Bank()

    account = bank.open_account(
        name="Richard"
    )
    assert account.name == "Richard"
```

So I'm going to make an account. That should have a name - maybe it's the name of the account holder - and it's going to be associated with a bank. 

I've written this idea down as a unit test. A unit test tests a single part of my code. When using pytest unit tests must start with the word "test_". If my IDE is set up correctly then I can run each test by pressing the little run button next to it. Otherwise, I can run them on the command line using the pytest command:

```bash
pytest tests/test_account.py
```

The statement at the bottom is an assertion. What it says is that the name attribute of the account instance must equal "Richard". If it does not the test will fail.

What happens when I run this? It fails because I haven't made a class called Bank yet. That's actually what we want - a key principal of TDD is to ensure that a test fails *before* we implement some new changes. That way, if the test passes we know those changes had the effect we wanted them to.

Let's go ahead and create our Bank class.

```python
class Bank:
    def open_account(self, name):
        pass
```

This has created a definition for the Bank class with a single function which is yet to be implemented.

> If you haven't used classes before don't worry! They're a way of defining a new type. Much like an integer, string, list etc.

We should also create two init files. Our project structure will look like this:

```bash
bank/
  __init__.py
  bank.py
tests/
  __init__.py
  test_account.py
```

That's got rid of our lint errors.

> Lint errors or warnings are how an editor shows us we're doing something wrong. The Bank class didn't exist so the editor gave us a red warning. It's worth listening to and correcting editor lint warnings because they show you how to code better and more idiomatically.

Let's run our test again. It's still failing. That's because we haven't actually implemented the function. I'll do that now.

```python
class Account:
    def __init__(self, name):
        self.name = name

class Bank:
    def open_account(self, name):
        return Account(name)
```

Great our test passes. 

We've also created an Account class with a constructor that takes a name as an argument.

> Account is another class but this time it has a constructor. A constructor is an argument that is called when we create the class instance. Account("richard") really calls the `__init__` function with "richard" as the value for name. The self argument refers to the specific instance of the class. So when we make our account called richard it creates a new instance of account with an attribute called name that has a value of "richard". Phew.

# Fixtures

What next? An account ought to have some money. Let's add a new test for making a deposit.

```python
def test_make_deposit():
    bank = Bank()

    account = bank.open_account(
        name="Richard"
    )
    account.make_deposit(
        100
    )
    assert account.balance == 100
```

I've copied this from another test. That's not great. I should adhere to DRY and find a way to avoid repetition.

> DRY - Don't Repeat Yourself. Within reason, avoiding repetition is incredibly important. It reduces the chance of having bugs, can make code clearer to read and makes it much easier to edit and reuse our code later.

Pytest has a great feature called fixtures. These allow us to define a variable once and then reuse it in whatever tests we like. The variable gets created again for every single test so if we change it in one test it won't have an impact on other tests.

```python
import pytest

from bank.bank import Bank

@pytest.fixture(
    name="account"
)
def make_account():
    bank = Bank()

    return bank.open_account(
        name="Richard"
    )

def test_open_account(
        account
):
    assert account.name == "Richard"

def test_make_deposit(
        account
):
    account.make_deposit(
        100
    )
    assert account.balance == 100
```

Here we make an account using the open_account function. We've imported pytest and used a decorator to tell pytest that our open_account function makes a variable called "account". Now I can add that variable to the arguments for any function and pytest will pass it in when it calls the test.

> decorator - a decorator is a neat concept in python that's a bit advanced but really powerful. A decorator is a function that takes a function as an argument and returns a function. Sometimes it does something before or after calling the function. It takes a bit of work to understand them but they're worth reading about.

Ok let's run our tests again. If all has gone well you should find that one test passes and the other fails. We need to implement our make_deposit function.

```python
class Account:
    def __init__(self, name):
        self.name = name
        self.balance = 0

    def make_deposit(self, amount):
        self.balance += amount
```

Running our tests reveals that everything works.

What about withdrawing? 

```python
def test_make_withdrawal(
        account
):
    account.balance = 100
    account.make_withdrawal(
        20
    )
    assert account.balance == 80
```

We've used the account fixture again. I've manually set the balance to 100. 

We run the test and see it fails. Then we implement the function:

```python
class Account:
    def __init__(self, name):
        self.name = name
        self.balance = 0

    def make_deposit(self, amount):
        self.balance += amount

    def make_withdrawal(self, amount):
        self.balance -= amount
```

All our tests should pass. 
This is the basic pattern of TDD:

1. Write a test
2. Check it fails
3. Write an implementation
4. Check it passes

# Exceptions

You may have noticed something a bit suspicious about our withdrawal function - you could withdraw infinite funds! Obviously that shouldn't be allowed.

When a function doesn't execute as expected or tries to do something it shouldn't we should raise an exception. We can use the inbuilt exceptions Python comes with or even create our own.

Rather than a withdrawal occurring for an empty account it should raise an exception and leave the balance unaffected.

```python
def test_make_bad_withdrawal(
        account
):
    account.balance = 10
    with pytest.raises(
            AccountException
    ):
        account.make_withdrawal(20)

    assert account.balance == 10
```

The pytest.raises function is a context manager. If the exception isn't raised within the context then the test will fail. We've also checked that the balance didn't change.

> Context Managers - using the with statement we can provide some resource that will be cleaned up at the end of the scope. This is a good pattern to use with the 'open' function for opening files as it closes the file implicitly.

```python
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
```

We've made an exception by defining a class that inherits from the Exception class. We check if the amount is greater than the balance and if it is we raise our AccountException. No more of the function is executed so the balance doesn't change.

Once we've imported AccountException into our test module all our tests should pass.

# Properties

Normally accounts would have an overdraft limit. Let's write a test for changing overdraft limits.

```python
def test_overdraft_limit(
        account
):
    account.overdraft_limit = 10
    account.make_withdrawal(10)

    assert account.balance == -10
```

We've attached a new attribute to our account called overdraft_limit and then tried to make a withdrawal that would bring us right to that limit. Running our test gives us an AccountException which is what we'd expect.

Let's implement this functionality.

```python
class Account:
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.overdraft_limit = 0

    def make_deposit(self, amount):
        self.balance += amount

    def make_withdrawal(self, amount):
        if amount > self.balance + self.overdraft_limit:
            raise AccountException(
                f"Withdrawal amount {amount} is greater than balance {self.balance}"
            )
        self.balance -= amount
```

That was easy! 

As the account holder we might also want to know how much money we can take out rather than what our current balance is. Let's add that to our test.

```python
def test_overdraft_limit(
        account
):
    account.overdraft_limit = 10

    assert account.available_funds == 10

    account.make_withdrawal(10)

    assert account.balance == -10
    assert account.available_funds == 0
```

Let's try to implement that.

```python
class Account:
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.overdraft_limit = 0
        self.available_funds = 0

    def make_deposit(self, amount):
        self.balance += amount
        self.available_funds = self.overdraft_limit + self.balance

    def make_withdrawal(self, amount):
        if amount > self.balance + self.overdraft_limit:
            raise AccountException(
                f"Withdrawal amount {amount} is greater than balance {self.balance}"
            )
        self.balance -= amount
        self.available_funds = self.overdraft_limit + self.balance
```

Running the test shows that it didn't work. It's because we modified the overdraft limit without calling make_deposit or make_withdrawal. Fortunately our test caught it!

This is a really common class of bug. available_funds is just the difference between the balance and overdraft_limit so we've used three values to describe a state which could have been defined by two. The bug is really an inconsistency between those values.

Python has a really powerful feature we can use here: **properties**.

```python
class Account:
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.overdraft_limit = 0

    @property
    def available_funds(self):
        return self.overdraft_limit + self.balance

    def make_deposit(self, amount):
        self.balance += amount

    def make_withdrawal(self, amount):
        if amount > self.balance + self.overdraft_limit:
            raise AccountException(
                f"Withdrawal amount {amount} is greater than balance {self.balance}"
            )
        self.balance -= amount
```

available_funds is actually a method but using a property makes it look like an attribute! Whenever we need to get the value for it it gets computed again on the fly. This is great for reducing the likelihood our code will have bugs.

> In object oriented programming a method is a function that belongs to a class.

We might also be concerned that it's currently possible to set the balance of the account lower than it should be allowed to. If whoever is using our Account class uses make_withdrawal it's fine, but they might decide to access the balance directly. How can we make sure they don't put the account in more of an overdraft than it should be in?

First we should write a test and show that it fails.

```python
def test_set_balance(
        account
):
    with pytest.raises(
            AccountException
    ):
        account.balance = -10
```

Fortunately properties provides us a way of making this work.

```python
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
```

There's a few different things going on here to unpack. 

Firstly, I've used a *private attribute* to make it impossible to directly access the balance from outside the instance. This is done by adding an underscore to the start. _balance can still be referenced from inside methods in the instance but your IDE will warn you if you try to access it from any other code.

> If you use two underscores then Python will actually change the name of the attribute at runtime causing an error if you try to access it.

Secondly, I've used a property to allow balance to be accessed. This is just like available funds but all it does is return the private attribute.

Thirdly, I've used a setter. This method checks that the balance is valid before updating the _balance attribute. If the balance is lower than the withdrawal limit then an exception is thrown.

Finally, there's no longer any need to check if the withdrawal amount is valid in the make_withdrawal function.

> Some of the detail in the previous exception message has been lost. It could make sense to catch the AccountException in make_withdrawal and then raise a new exception with more detail.

It's a good idea to run all of the tests we've written so far here as we've changed a lot of code. Here's where TDD really comes into its own. We can make all these changes and still be confident we haven't broken anything. If a test does fail it will help us figure out what we've done wrong.

# Parametrize

Let's look again at one of our tests.

```python
def test_overdraft_limit(
        account
):
    account.overdraft_limit = 10

    assert account.available_funds == 10

    account.make_withdrawal(10)

    assert account.balance == -10
    assert account.available_funds == 0
```

We've tested what effect a single withdrawal has on the available funds. But to be safe it might be sensible to add some more tests with different number.

```python
def test_overdraft_limit(
        account
):
    account.overdraft_limit = 10

    assert account.available_funds == 10

def test_withdrawal_10(
        account
):
    account.overdraft_limit = 10

    account.make_withdrawal(10)

    assert account.balance == -10
    assert account.available_funds == 0

def test_withdrawal_5(
        account
):
    account.overdraft_limit = 10

    account.make_withdrawal(5)

    assert account.balance == -5
    assert account.available_funds == 5
```

This works and shows that even with different numbers our code functions but it's very repetitive. Fortunately pytest has another really useful feature: parametrize.

```python
@pytest.mark.parametrize(
    "limit, withdrawal, balance, funds",
    [
        (10, 10, -10, 0),
        (10, 5, -5, 5),
        (20, 5, -5, 15),
    ]
)
def test_withdrawal(
        account,
        limit,
        withdrawal,
        balance,
        funds
):
    account.overdraft_limit = limit
    account.make_withdrawal(withdrawal)

    assert account.balance == balance
    assert account.available_funds == funds
```

This replaces the test_withdrawal_5 and test_withdrawal_10 functions. 

It's a decorator. The first argument defines four arguments that are passed into our test function: limit, withdrawal, balance, funds. 

The second argument gives a list of tuples of values for those arguments. For example:

(10, 10, -10, 0)

means

limit = 10
withdrawal = 10
balance = -10
funds = 0

Each entry in this list corresponds to another test. The first and second entries are the tests we had before. The third entry is a new test I've written to check what happens if I change the overdraft_limit.

This means we wrote one test but got three! We can easily add additional entries to our list of other scenarios we want to test.

# Interest Rates

What else should bank accounts do? We might want to give those people saving some interest and charge those who aren't. To keep things simple we'll consider a single interest rate and not worry about what time period its applied over.

What do we expect to happen? If an account has some money in it then it should get a little more money and if its in an overdraft it should lose a little money.

```python
def test_pay_interest(
        account,
        bank
):
    account.balance = 10
    bank.interest_rate = 0.1

    account.step()

    assert account.balance == 11
```

I've put £10 into the account and set the bank's interest rate at 10%. That might seem an unrealistic interest rate but it helps keep out test simple!

I've decided that a function called **step** will be used to apply interest to the account. You could imagine that's saying a given time period has passed. Finally, I check the balance has gone up to the expected £11.

Running the test shows our first problem - there is no bank fixture! We defined our bank object inside the account fixture. Fortunately we can use fixtures inside other fixtures.

```python
@pytest.fixture(
    name="bank"
)
def make_bank():
    return Bank()

@pytest.fixture(
    name="account"
)
def make_account(
        bank
):
    return bank.open_account(
        name="Richard"
    )
```

We make a bank and then use that bank to make an account. Each time we run a test that uses the account it will make a new bank and a new account. If that test uses both the bank and the account then one of each is made - the bank we are given is the same that was used to create the account. This is important because it means the objects created by the fixtures are related to one another.

Running our test shows it fails because we haven't implemented the step method. Let's do that now.

```python
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
        self.balance *= (1 + self.bank.interest_rate)
```

Each account now holds a reference to the bank to which it belongs and it uses that to calculate a new balance.

```python
class Bank:
    def __init__(self):
        self.interest_rate = 0.0

    def open_account(self, name):
        return Account(
            name,
            bank=self
        )
```

The bank now has an interest rate and passes a reference to itself when it creates the account.

Our test passes. What else should we test? We should check negative interest rates and maybe some other numbers.

```python
@pytest.mark.parametrize(
    "initial, interest, final",
    [
        (10, 0.1, 11),
        (-10, 0.1, -11),
        (-20, 0.1, -22),
    ]
)
def test_pay_interest(
        account,
        bank,
        initial,
        interest,
        final
):
    account.overdraft_limit = 20
    account.balance = initial
    bank.interest_rate = interest

    account.step()

    assert account.balance == final
```

The test with an initial balance of -20 fails because applying interest puts the balance below the overdraft limit! TDD has shown us something we haven't properly considered and motivated a new feature.

How could we handle this better? Maybe we should allow a balance below the overdraft limit after all.

```python
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
```

By accessing the private attribute directly we can circumvent the check. 

There might be another issue though - what if the balance is negative?

```python
def test_deposit_below_limit(
        account
):
    account._balance = -10
    account.make_deposit(5)

    assert account.balance == -5
```

This fails. But surely we should allow somebody to deposit money even if they're over their overdraft limit?

```python
    def make_deposit(self, amount):
        self._balance += amount
```

All our tests are passing again. This is the beauty of TDD - by enforcing certain behaviours using tests we ensure that we retain those behaviours as we add more functionality. We can change the implementation of our code to support all the functionality we need provided it provides the same behaviour stipulated by our tests. In some sense the code is defined by the tests we've written and not the implementation!

# conftest

So applying interest to one account is all well and good but surely we want to apply interest to all accounts at the same time?

```python
def test_pay_all(
        account,
        bank
):
    account_2 = bank.open_account(
        "Second"
    )

    account.balance = 10
    account_2.balance = 20
    bank.interest_rate = 0.1

    bank.step()

    assert account.balance == 11
    assert account_2.balance == 22
```

We're now asserting that calling a function called **step** on the bank will apply interest for each account.

```python
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
```

A bank now holds a reference to each of its accounts. New accounts are added as they are opened. The step function for a bank simply calls the step function for each of the accounts.

By default the bank has an interest rate of 0.1. We could decide to pass a different interest rate but because we've used a default argument we don't have to.

> The bank has a reference to a list which contains a reference to the account which contains a reference to the bank. This is a circular reference. In many programming languages this can cause these objects to stay in memory forever because the algorithm that works out what objects aren't being used anymore can't handle circular references. Fortunately Python is a bit smarter than that.

Our test file is getting a bit messy. Let's break it up.

We'll move our tests related to interest to a new test module.

```python
import pytest

@pytest.mark.parametrize(
    "initial, interest, final",
    [
        (10, 0.1, 11),
        (-10, 0.1, -11),
        (-20, 0.1, -22),
    ]
)
def test_pay_interest(
        account,
        bank,
        initial,
        interest,
        final
):
    account.overdraft_limit = 20
    account.balance = initial
    bank.interest_rate = interest

    account.step()

    assert account.balance == final

def test_pay_all(
        account,
        bank
):
    account_2 = bank.open_account(
        "Second"
    )

    account.balance = 10
    account_2.balance = 20

    bank.step()

    assert account.balance == 11
    assert account_2.balance == 22
```

Let's run all our tests to check we haven't broken anything.

We have a new error. The tests in test_interest.py can't see the fixtures in test_account.py. We could copy the fixtures over but that's not very elegant. Fortunately pytest has a feature called conftest.

We make a new file and move the fixtures we use in both the test modules to this file.

```python
import pytest

from bank.bank import Bank

@pytest.fixture(
    name="bank"
)
def make_bank():
    return Bank()

@pytest.fixture(
    name="account"
)
def make_account(
        bank
):
    return bank.open_account(
        name="Richard"
    )
```

Our project now has this structure:

```bash
bank/
  __init__.py
  bank.py
tests/
  __init__.py
  conftest.py
  test_account.py
  test_interest.py
```

# Interest

Perhaps we want different kinds of account. Business accounts, savings accounts or student accounts for example. These would need to have different behaviours. For example, we might want a student account to not be charged interest for entering their overdraft.

```python
def test_student_account(
        bank
):    
    account = StudentAccount(
        "Guy Young",
        bank=bank
    )

    account._balance = -10
    account.step()

    assert account._balance == -10
```

A student account is put in the red and then charged interest. We could modify the open_account function to create different kinds of account but that feels unnecessarily complicated.

Let's make our student account.

```python
class StudentAccount(Account):
    def step(self):
        pass
```

That was easy! We've used inheritance. A StudentAccount is just a kind of Account that doesn't get charged interest when its balance is negative. We've overridden the step function to stop it from doing anything.

Actually, we should probably check what happens if its balance is positive.

```python
@pytest.mark.parametrize(
    "initial, final",
    [
        (-10, -10),
        (-5, -5),
        (10, 11)
    ]
)
def test_student_account(
        bank,
        initial,
        final
):
    account = StudentAccount(
        "Guy Young",
        bank=bank
    )

    account._balance = initial
    account.step()

    assert account._balance == final
```

This fails because we've stopped the step function from being called whether the balance is positive or negative. 

```python
class StudentAccount(Account):
    def step(self):
        if self.balance > 0:
            super().step()
```

Now the step function in the Account class will be called only when the balance is positive. All of our tests pass!

It's not great having two ways of creating new accounts. Fortunately we have high test coverage so we can try removing a piece of code and see what happens.

> There are tools to analyse test coverage, often built into IDEs. These are really useful for ensuring that all your code gets run at least once by a test. Even so, full coverage does not mean that you have tested every possibility and found every bug!

```python
class Bank:
    def __init__(
            self,
            interest_rate=0.1
    ):
        self.interest_rate = interest_rate
        self.accounts = list()

    def step(self):
        for account in self.accounts:
            account.step()
```

I've removed the open_account function! Which tests fail?

First we need to fix our account fixture.

```python
@pytest.fixture(
    name="account"
)
def make_account(
        bank
):
    return Account(
        name="Richard",
        bank=bank
    )
```

That fixes almost all our tests. The only failing test complains about the function being missing because we open another account.

```python
def test_pay_all(
        account,
        bank
):
    account_2 = Account(
        name="Second",
        bank=bank
    )

    account.balance = 10
    account_2.balance = 20

    bank.step()

    assert account.balance == 11
    assert account_2.balance == 22
```

I've updated the creation of account_2 so it doesn't use the function we removed. However, it's still failing because no accounts have been added to the bank. We need to reimplement that functionality.

```python
class Account:
    def __init__(
            self,
            name,
            bank
    ):
        bank.accounts.append(
            self
        )
```

Now the account adds itself to the bank in the constructor and all our tests pass.

# Conclusions

Testing allows us to write code that is more reliable and better structured. 

- We showed how simple tests can be written to demonstrate the code has the behaviour we want.
- We can use fixtures to avoid repeated code in our tests.
- Throwing exceptions is a good way to communicate that something unexpected happened.
- Properties allow us to pretend functions are variables. This means we can compute values on the fly, stop other people changing those values and trigger other functions when those values are set.
- We can use parametrize to try out lots of different values for a single test.
- We can use conftest to reuse fixtures across different test modules.
- Inheritance is a powerful way to modify the behaviour of a class.
- With high test coverage we can refactor code by breaking things and seeing what happens.

# What Next?

There are loads of more techniques and ideas in pytest and Python. I'd encourage you to read the pytest documentation for some more ideas.

You can also try implementing some more features into our bank model:

- What if we wanted to deposit and withdraw money in different currencies?
- Can we compute some aggregate statistics across the bank?
- What if we wanted to track the history of accounts so we could generate bank statements?

Once I'm happy with some code I add [type annotations](https://docs.python.org/3/library/typing.html) and [numpy style doc strings](https://numpydoc.readthedocs.io/en/latest/format.html). They're out of scope for this tutorial but if you don't know much about them I'd encourage you to learn to use them. They help a lot when trying to communicate what our code does to others as well as our future selves.

Code from this tutorial can be found [here](https://github.com/rhayes777/workshop).

Please send any questions, comments or queries to richard@rghsoftware.co.uk
