from abc import ABC, abstractmethod

class Account(ABC):
    bankname = "Mutual Trust Bank"
    branch = "Kaliganj, Gazipur"

    def __init__(self, username, pin, address):
        self.username = username
        self.pin = pin
        self.address = address
        self.balance = 0.0
        self.transaction_history = []
        print(f'Hello {self.username}, Congratulations! Your account created successfully.')

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    def ministatement(self):
        print(f'Your account balance is {self.balance}')
        print("Transaction History:")
        for transaction in self.transaction_history:
            print(transaction)

    @abstractmethod
    def calculate_interest(self):
        pass

    def close_account(self):
        print("Closing account...")
        self.balance = 0.0
        self.transaction_history.clear()
        print("Account closed successfully.")

    @abstractmethod
    def transfer_funds(self, amount, recipient_account):
        pass

    @abstractmethod
    def update_account_info(self, username=None, address=None, pin=None):
        pass


class SavingsAccount(Account):
    interest_rate = 0.05

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(f'Deposit: +{amount}')
        print(f'{amount} deposited successfully. Your account balance is {self.balance}')

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f'Withdrawal: -{amount}')
            print(f'{amount} withdrawn successfully.')
        else:
            print("Insufficient Funds")

    def calculate_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        self.transaction_history.append(f'Interest: +{interest}')
        print(f'Interest calculated and added: {interest}')

    def transfer_funds(self, amount, recipient_account):
        if amount <= self.balance:
            self.balance -= amount
            recipient_account.balance += amount
            self.transaction_history.append(f'Transfer: -{amount} to {recipient_account.username}')
            print(f'{amount} transferred successfully to {recipient_account.username}')
        else:
            print("Insufficient Funds for transfer")

    def update_account_info(self, username=None, address=None, pin=None):
        if username:
            self.username = username
        if address:
            self.address = address
        if pin:
            self.pin = pin
        print("Account information updated successfully.")


class CurrentAccount(Account):
    overdraft_limit = 1000

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(f'Deposit: +{amount}')
        print(f'{amount} deposited successfully. Your account balance is {self.balance}')

    def withdraw(self, amount):
        available_balance = self.balance + self.overdraft_limit
        if amount <= available_balance:
            self.balance -= amount
            self.transaction_history.append(f'Withdrawal: -{amount}')
            print(f'{amount} withdrawn successfully.')
        else:
            print("Exceeded available balance")

    def calculate_interest(self):
        print("Current account does not earn interest.")

    def transfer_funds(self, amount, recipient_account):
        if amount <= (self.balance + self.overdraft_limit):
            self.balance -= amount
            recipient_account.balance += amount
            self.transaction_history.append(f'Transfer: -{amount} to {recipient_account.username}')
            print(f'{amount} transferred successfully to {recipient_account.username}')
        else:
            print("Exceeded available balance for transfer")

    def update_account_info(self, username=None, address=None, pin=None):
        if username:
            self.username = username
        if address:
            self.address = address
        if pin:
            self.pin = pin
        print("Account information updated successfully.")


def create_account():
    print(f'Welcome to {Account.bankname}, {Account.branch}')
    print("********Account Creation********")
    username = input("Enter your username: ")
    pin = input("Enter your pin: ")
    address = input("Enter your address: ")
    account_type = input("Enter account type (Savings/Current): ")

    if account_type.lower() == 'savings':
        return SavingsAccount(username, pin, address)
    elif account_type.lower() == 'current':
        return CurrentAccount(username, pin, address)
    else:
        print("Invalid account type")
        return None


def authenticate(account, pin):
    if account.pin == pin:
        return True
    else:
        print("Incorrect PIN.")
        return False


def transfer_funds(sender, recipient, amount, pin):
    if authenticate(sender, pin):
        sender.transfer_funds(amount, recipient)
        print("Transfer complete.")
    else:
        print("Transfer failed due to incorrect PIN.")


def update_account_info(account, username, address, pin, old_pin):
    if authenticate(account, old_pin):
        account.update_account_info(username, address, pin)
    else:
        print("Authentication failed. Account information not updated.")


B = create_account()

if B:
    while True:
        print("Please select any option: ")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Mini statement")
        print("4. Calculate Interest")
        print("5. Transfer Funds")
        print("6. Update Account Information")
        print("7. Close Account")
        print("8. Stop")
        option = int(input(" "))

        if option == 1:
            amount = float(input("Enter deposit amount: "))
            B.deposit(amount)
        elif option == 2:
            amount = float(input("Enter withdrawal amount: "))
            B.withdraw(amount)
        elif option == 3:
            B.ministatement()
        elif option == 4:
            B.calculate_interest()
        elif option == 5:
            recipient_username = input("Enter recipient username: ")
            recipient_account = input("Enter recipient account type (Savings/Current): ")
            amount = float(input("Enter transfer amount: "))
            recipient = SavingsAccount if recipient_account.lower() == 'savings' else CurrentAccount
            transfer_funds(B, recipient(recipient_username, "", ""), amount, B.pin)
        elif option == 6:
            username = input("Enter new username (leave blank to keep current): ")
            address = input("Enter new address (leave blank to keep current): ")
            pin = input("Enter new PIN (leave blank to keep current): ")
            old_pin = input("Enter current PIN: ")
            update_account_info(B, username, address, pin, old_pin)
        elif option == 7:
            pin = input("Enter your PIN to close account: ")
            if authenticate(B, pin):
                B.close_account()
        elif option == 8:
            print("Thanks for using Mutual Trust Bank...")
            break
      
               
