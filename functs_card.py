import sqlite3

from hidden import get_cards_db


class Card_in_db:
    '''Handles doing stuff with a card inside of a database when 
    user wants to withdraw a specific amount.'''

    cards_db = get_cards_db()

    def __init__(self, card, amount):
        '''Instantiante with a bank card and amount user wants 
        to withdraw.'''

        self.card = card
        self.amount = amount
    

    def check_money(self):
        '''Checks if the card has enough money to pay.
        Returns True if there's enough and False if there's not.'''

        conn = sqlite3.connect(self.cards_db)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT Card.balance FROM Card JOIN Types 
        ON Card.type_id = Types.id 
        WHERE Card.number = ? AND Card.cvc = ? AND Card.holder = ? AND Types.type = ?
        ''', (self.card.num, self.card.cvc, self.card.name, self.card.type))

        try:
            balance = cursor.fetchone()[0]
        except:
            balance = None

        conn.commit()

        cursor.close()
        conn.close()

        if balance == None:
            print('Sorry, there was a problem with your operation. Maybe your crenditals are incorrect.')
            return False

        if balance >= self.amount:
            return True
        else:
            print('Not enough balance to perform the operation.')
            return False


    def withdraw(self):
        '''Withdraws a given amount of money after succesful check if 
        there is enough money on the balance.

        Returns True if the operation was succesful and False if it was not.
        '''

        check = self.check_money()

        # Abrupt the operation if credentials are wrong 
        # or there isn't enough money on the balance
        if not check:
            return False
        
        if check:
            conn = sqlite3.connect(self.cards_db)
            cursor = conn.cursor()

            # Get current card's balance
            cursor.execute('SELECT balance FROM Card WHERE number = ?', 
                            (self.card.num, ))
            balance = cursor.fetchone()[0]
            
            # Withdraw a given amount and save updated balance in a variable
            upd_balance = balance - self.amount

            # Set new updated balance
            cursor.execute('UPDATE Card SET balance = ? WHERE number = ?', 
                            (upd_balance, self.card.num))
            conn.commit()

            cursor.close()
            conn.close()

            print('Operation was successful.')
            return True
