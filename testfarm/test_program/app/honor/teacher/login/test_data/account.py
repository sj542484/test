import random

# data base of account
# we can add a or multiple account in it, like this '{'account': 'xxxxxxxxxxx', 'password': 'yyyyyyyy'},'
_VALID_ACCOUNT = (
    # {'username': '18711111144', 'password': '456789'},
    # {'username': '18000000140', 'password': '123123'},
    {'username': '18711111234', 'password': '456789'},
    # {'username': '18000000018', 'password': '000018'},
)


class Account:
    def __init__(self):
        self.valid_account = _VALID_ACCOUNT[random.randint(0, len(_VALID_ACCOUNT)) - 1]

    def account(self):
        return self.valid_account['username']

    def password(self):
        return self.valid_account['password']


# global variable
# a instance of account
# it can be used in any place via 'from App.teacher.test_data.account import VALID_ACCOUNT'
VALID_ACCOUNT = Account()
VALID_ACCOUNT.account()
VALID_ACCOUNT.password()
