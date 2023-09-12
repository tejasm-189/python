import random
import json

# Sample user data (you can replace this with your own user data storage)
user_data = {
    "1234567890": {
        "pin": "1234",
        "balance": 1000.0,
        "transactions": []
    },
    "9876543210": {
        "pin": "4321",
        "balance": 500.0,
        "transactions": []
    }
}

# Function to load user data from a JSON file (optional)
def load_user_data():
    try:
        with open("user_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return user_data

# Function to save user data to a JSON file (optional)
def save_user_data(data):
    with open("user_data.json", "w") as file:
        json.dump(data, file, indent=4)

class ATM:
    def __init__(self):
        self.user_data = load_user_data()

    def authenticate_user(self):
        user_id = input("Enter User ID: ")
        pin = input("Enter PIN: ")

        if user_id in self.user_data and self.user_data[user_id]["pin"] == pin:
            self.current_user = user_id
            return True
        else:
            print("Authentication failed. Invalid User ID or PIN.")
            return False

    def display_menu(self):
        while True:
            print("\nWelcome to Your Bank ATM")
            print("Please select an option:")
            print("1. Transactions")
            print("2. History")
            print("3. Withdraw")
            print("4. Deposit")
            print("5. Transfer")
            print("6. Balance")
            print("7. Quit")

            choice = input("Enter the number of your choice: ")

            if choice == "1":
                self.view_transactions()
            elif choice == "2":
                self.view_transaction_history()
            elif choice == "3":
                self.withdraw()
            elif choice == "4":
                self.deposit()
            elif choice == "5":
                self.transfer()
            elif choice == "6":
                self.balance_inquiry()
            elif choice == "7":
                self.quit()
                break
            else:
                print("Invalid choice. Please select a valid option.")

    def view_transactions(self):
        print("\nRecent Transactions:")
        for transaction in self.user_data[self.current_user]["transactions"]:
            print(transaction)

    def view_transaction_history(self):
        print("\nTransaction History:")
        for transaction in self.user_data[self.current_user]["transactions"]:
            print(transaction)

    def withdraw(self):
        amount = float(input("Enter the amount to withdraw: "))
        if amount <= 0:
            print("Invalid amount. Please enter a positive value.")
        elif amount > self.user_data[self.current_user]["balance"]:
            print("Insufficient balance.")
        else:
            self.user_data[self.current_user]["balance"] -= amount
            transaction = f"Withdraw: ${amount:.2f}"
            self.user_data[self.current_user]["transactions"].append(transaction)
            save_user_data(self.user_data)
            print(f"Withdrawal successful. Current balance: ${self.user_data[self.current_user]['balance']:.2f}")

    def deposit(self):
        amount = float(input("Enter the amount to deposit: "))
        if amount <= 0:
            print("Invalid amount. Please enter a positive value.")
        else:
            self.user_data[self.current_user]["balance"] += amount
            transaction = f"Deposit: ${amount:.2f}"
            self.user_data[self.current_user]["transactions"].append(transaction)
            save_user_data(self.user_data)
            print(f"Deposit successful. Current balance: ${self.user_data[self.current_user]['balance']:.2f}")

    def transfer(self):
        recipient = input("Enter recipient's User ID: ")
        if recipient not in self.user_data:
            print("Recipient not found.")
            return

        amount = float(input("Enter the amount to transfer: "))
        if amount <= 0:
            print("Invalid amount. Please enter a positive value.")
        elif amount > self.user_data[self.current_user]["balance"]:
            print("Insufficient balance.")
        else:
            self.user_data[self.current_user]["balance"] -= amount
            self.user_data[recipient]["balance"] += amount

            sender_transaction = f"Transfer to {recipient}: ${amount:.2f}"
            self.user_data[self.current_user]["transactions"].append(sender_transaction)

            recipient_transaction = f"Transfer from {self.current_user}: ${amount:.2f}"
            self.user_data[recipient]["transactions"].append(recipient_transaction)

            save_user_data(self.user_data)
            print(f"Transfer successful. Current balance: ${self.user_data[self.current_user]['balance']:.2f}")
    
    def balance_inquiry(self):  # New method for balance inquiry
        current_balance = self.user_data[self.current_user]["balance"]
        print(f"Your current balance is: ${current_balance:.2f}")

    def quit(self):
        print("Thank you for using Your Bank ATM.")

if __name__ == "__main__":
    atm = ATM()
    authenticated = atm.authenticate_user()
    
    if authenticated:
        atm.display_menu()
    else:
        print("Authentication failed. Exiting ATM.")
