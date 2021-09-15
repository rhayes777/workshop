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
