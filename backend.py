class Backend:
    def __init__(self):
        self.accounts = {}

    def create_account(self, cart, password, balance):
        if cart in self.accounts:
            return False
        self.accounts[cart] = {"password": password, "balance": balance}
        return True

    def check_login(self, cart, password):
        if cart in self.accounts and self.accounts[cart]["password"] == password:
            return True
        return False

    def get_balance(self, cart):
        return self.accounts[cart]["balance"]

    def deposit(self, cart, amount):
        self.accounts[cart]["balance"] = self.accounts[cart]["balance"] + amount

    def withdraw(self, cart, amount):
        if amount > self.accounts[cart]["balance"]:
            return False
        self.accounts[cart]["balance"] = self.accounts[cart]["balance"] - amount
        return True