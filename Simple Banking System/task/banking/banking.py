import random
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS card (
    id INTEGER PRIMARY KEY,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
);""")
conn.commit()



class Card:

    @staticmethod
    def random_numbers(n):
        random_number = ""
        for i in range(n):
            random_number += str(random.randint(0, 9))
        return random_number

    def __init__(self, *args):
        if len(args) > 0:
            self.card_number = args[0]
            self.pin = args[1]
            self.balance = args[2]
        else:
            self.card_number = Card.gen_acc_id()
            self.pin = str(self.random_numbers(4))
            self.balance = 0
            cur.execute("INSERT INTO card (number,pin,balance) VALUES(?,?,?)",(self.card_number,self.pin,self.balance))
            conn.commit()



    @staticmethod
    def get_info_db(card_number,pin):
        cur.execute("SELECT * FROM card WHERE number= \"{0}\" and pin= \"{1}\" ;".format(card_number, pin))

        rows = cur.fetchall()
        tab = []
        for row in rows:
            tab.append(row)
        if len(tab) == 0:
            return None
        else:
            retcard = Card(tab[0][1], tab[0][2], tab[0][3])
            return retcard



    @staticmethod
    def print_cards():
        pass
        # for i in Card.card_data:
        #     print(i.card_number)
        #     print(i.pin)

    @staticmethod
    def check_if_exist(card_number):
        cur.execute("SELECT * FROM card WHERE number= \"{0}\" ;".format(card_number))

        rows = cur.fetchall()
        tab = []
        for row in rows:
            tab.append(row)
        return len(tab) != 0

        # for i in Card.card_data:
        #     if i.card_number == answer_card and i.pin == answer_pin:
        #         return True
        # return False

    @staticmethod
    def gen_acc_id():
        card_number = "400000" + Card.random_numbers(9)
        return Card.validate_luhn(card_number)

    @staticmethod
    def validate_luhn(card_number): #zwraca o 1 dłuższy numer zgodny z algorytmem luhna
        lst_num = [int(d) for d in str(card_number)]
        suma = 0
        checksum = 0
        for i in range (len(lst_num)):
            if i % 2 == 0:
                suma += lst_num[i] * 2
                if lst_num[i] * 2 > 9:
                    suma -= 9
            else:
                suma += lst_num[i]
        if suma % 10 != 0:
            checksum = 10 - (suma % 10)
        card_number += str(checksum)
        return card_number

    def transfer(self,transfer_number,transferred_money):
        self.balance -= transferred_money
        cur.execute("UPDATE card SET balance = {0} WHERE number = \"{1}\";".format(self.balance, self.card_number))
        conn.commit()
        cur.execute("UPDATE card SET balance = balance + {0} WHERE number = \"{1}\";".format(transferred_money, transfer_number))
        conn.commit()
        print("Success!")





    def login(self):
        while True:
            print("""1. Balance
    2. Add income
    3. Do transfer
    4. Close account
    5. Log out
    0. Exit""")
            choice = input()
            if choice == "1":
                print("Balance: ",self.balance)
            if choice == "2":
                added_cash = int(input("Enter income: "))
                self.balance += added_cash
                cur.execute("UPDATE card SET balance= {0} WHERE number = \"{1}\";".format(self.balance, self.card_number))
                conn.commit()
                print("Income was added!")
            if choice == "3":
                print("Transfer")
                cn = input("Enter card number: ")
                if Card.validate_luhn(cn[:-1]) == cn:
                    if Card.check_if_exist(cn):
                        if cn == self.card_number:
                            print("You can't transfer money to the same account!")
                        else:
                            h = int(input("Enter how much money you want to transfer:"))
                            if h > self.balance:
                                print("Not enough money!")
                            else:
                                self.transfer(cn,h)
                    else:
                        print("Such a card does not exist.")
                else:
                    print("Probably you made a mistake in the card number. Please try again!")

            if choice == "4":
                cur.execute("DELETE FROM card WHERE number = \"{0}\";".format(self.card_number))
                conn.commit()
                print("The account has been closed!")
                return 0
            if choice == "5":
                print("You have successfully logged out!")
                return 0
            if choice == "0":
                print("Bye!")
                quit()

def menu():
    while True:
        print("""1. Create an account
2. Log into account
0. Exit
""")
        choice = input()
        if choice == "1":
            card = Card()
            print("""Your card has been created
        Your card number: """)
            print(card.card_number)
            print("Your card PIN: ")
            print(card.pin)
        if choice == "2":
            # #Card.print_cards()
            in_answer_card_nr = input("Enter your card number: ")
            in_answer_pin = input("Enter your pin number: ")
            # if Card.check(in_answer_card_nr, in_answer_pin):
            #     print("You have successfully logged in!")
            # card.login()
            # else:
            #     print("Wrong card number or PIN!")
            a = Card.get_info_db(in_answer_card_nr, in_answer_pin)
            if a == None:
                print("Wrong card number or PIN!")
            else:
                print("You have successfully logged in!")
                a.login()
        if choice =="3":
            in_answer_card_nr = input("Enter your card number: ")
            in_answer_pin = input("Enter your pin number: ")
            Card.get_info_db(in_answer_card_nr, in_answer_pin)
        if choice == "0":
            print("Bye!")
            quit()

menu()
