import pytest

from bank.bank import Bank, Account


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
    return Account(
        name="Richard",
        bank=bank
    )
