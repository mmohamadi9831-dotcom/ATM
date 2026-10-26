from tkinter import *
from tkinter import messagebox
from backend import Backend

BG = "#2E5781"

backend = Backend()
root = Tk()
root.title("ATM")
root.geometry("350x150")
root.configure(bg=BG)


class App:
    def __init__(self, master):
        self.master = master

        Label(master, text="CART NUMBER ->", bg=BG, fg="white").grid(row=0, column=0)
        self.cart_entry = Entry(master, bg="#4F364A", fg="white")
        self.cart_entry.grid(row=0, column=1)

        Label(master, text="PASSWORD ->", bg=BG, fg="white").grid(row=1, column=0)
        self.pass_entry = Entry(master, bg="#4F364A", fg="white", show="*")
        self.pass_entry.grid(row=1, column=1)

        Button(master, text="LOGIN", bg="#CC0000", command=self.login).grid(row=2, column=0, pady=20)
        Button(master, text="CREATE ACCOUNT", bg="#CC0000", command=self.open_create).grid(row=2, column=1, pady=20)

    def login(self):
        cart = self.cart_entry.get()
        password = self.pass_entry.get()

        if cart == "" or password == "":
            messagebox.showwarning("Error", "Please fill in all fields")
        elif not backend.check_login(cart, password):
            messagebox.showerror("Error", "Wrong cart number or password")
        else:
            self.open_account(cart)

    def open_account(self, cart):
        self.cart = cart

        window = Toplevel(self.master)
        window.title("Account")
        window.geometry("300x250")
        window.configure(bg=BG)

        Label(window, text="Cart : " + cart, bg=BG, fg="white").pack(pady=5)

        self.balance_label = Label(window, text="Balance : " + str(backend.get_balance(cart)),
                                   bg=BG, fg="white", font=("Arial", 14))
        self.balance_label.pack(pady=10)

        Label(window, text="Amount :", bg=BG, fg="white").pack()
        self.money_entry = Entry(window, bg="#4F364A", fg="white")
        self.money_entry.pack(pady=5)

        Button(window, text="Deposit money", bg="#CC0000", command=self.deposit).pack(pady=3)
        Button(window, text="Withdraw money", bg="#CC0000", command=self.withdraw).pack(pady=3)
        Button(window, text="Close", bg="#CC0000", command=window.destroy).pack(pady=3)

    def get_money(self):
        try:
            money = int(self.money_entry.get())
        except ValueError:
            messagebox.showerror("Error", "your number is false")
            return None

        if money <= 0:
            messagebox.showerror("Error", "The amount must be greater than zero.")
            return None

        return money

    def refresh(self):
        self.balance_label.config(text="Balance : " + str(backend.get_balance(self.cart)))
        self.money_entry.delete(0, END)

    def deposit(self):
        money = self.get_money()
        if money is not None:
            backend.deposit(self.cart, money)
            self.refresh()

    def withdraw(self):
        money = self.get_money()
        if money is None:
            return
        if backend.withdraw(self.cart, money):
            self.refresh()
        else:
            messagebox.showerror("Error", "There is not enough balance.")

    def open_create(self):
        self.create_window = Toplevel(self.master)
        self.create_window.title("Create Account")
        self.create_window.geometry("350x180")
        self.create_window.configure(bg=BG)

        Label(self.create_window, text="Cart Number:", bg=BG, fg="white").grid(row=0, column=0)
        self.new_cart = Entry(self.create_window, bg="#4F364A", fg="white")
        self.new_cart.grid(row=0, column=1)

        Label(self.create_window, text="Password :", bg=BG, fg="white").grid(row=1, column=0)
        self.new_pass = Entry(self.create_window, bg="#4F364A", fg="white", show="*")
        self.new_pass.grid(row=1, column=1)

        Label(self.create_window, text="Balance :", bg=BG, fg="white").grid(row=2, column=0)
        self.new_balance = Entry(self.create_window, bg="#4F364A", fg="white")
        self.new_balance.grid(row=2, column=1)

        Button(self.create_window, text="SAVE", bg="#CC0000", command=self.save).grid(row=3, column=0, columnspan=2, pady=20)

    def save(self):
        cart = self.new_cart.get()
        password = self.new_pass.get()
        balance_text = self.new_balance.get()

        if cart == "" or password == "" or balance_text == "":
            messagebox.showwarning("Error", "Please fill in all fields")
            return

        try:
            balance = int(balance_text)
        except ValueError:
            messagebox.showerror("Error", "The balance must be a number")
            return

        if balance < 0:
            messagebox.showerror("Error", "The balance cannot be negative.")
        elif not backend.create_account(cart, password, balance):
            messagebox.showerror("Error", "This card number has already been registered.")
        else:
            messagebox.showinfo("Successful", "The account has been created : " + cart)
            self.create_window.destroy()


app = App(root)
root.mainloop()