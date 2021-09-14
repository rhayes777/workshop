import pytest

from bank.bank import Bank, AccountException


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


def test_make_withdrawal(
        account
):
    account.balance = 100
    account.make_withdrawal(
        20
    )
    assert account.balance == 80


def test_make_bad_withdrawal(
        account
):
    account.balance = 10
    with pytest.raises(
            AccountException
    ):
        account.make_withdrawal(20)

    assert account.balance == 10


def test_overdraft_limit(
        account
):
    account.overdraft_limit = 10

    assert account.available_funds == 10

    account.make_withdrawal(10)

    assert account.balance == -10
    assert account.available_funds == 0


def test_set_balance(
        account
):
    with pytest.raises(
            AccountException
    ):
        account.balance = -10
