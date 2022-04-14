import sqlite3

from hidden import get_tickets_db, get_cards_db

tickets_db = get_tickets_db
cards_db = get_cards_db

class Card:
    '''Represents Debit Card with card's type, number, 
    CVC, and name of its holder.'''

    def __init__(self, card_type, num, cvc, name):
        '''Instantiate with card's type, number, CVC, 
        and name of holder.'''

        self.type = card_type
        self.num = num
        self.cvc = cvc
        self.name = name
    
    def change_params(self, card_type, num, cvc, name):
        '''Change parameters of the card.'''

        self.type = card_type
        self.num = num
        self.cvc = cvc
        self.name = name


class CinemaUser:
    '''Represents a User in the app with name, seat he's chosen, 
    and his card.'''

    def __init__(self, name, seat):
        '''Instantiate with cinema app user name and number of seat.'''

        self.name = name
        self.seat = seat
    
    def add_card(self, card_type, card_num, card_cvc, card_name):
        '''Adds a Card instance object with given card's type, number,
        CVC, and name of its holder.'''

        self.card = Card(card_type, card_num, card_cvc, card_name)


def check_seat(seat_id):
    '''Checks if the given seat is taken or not.
    Returns True if the seat is free and False if it's not.'''

    conn = sqlite3.connect(tickets_db)
    cursor = conn.cursor()

    cursor.execute('SELECT taken FROM Seat WHERE seat_id = ?', (seat_id, ))

    value = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    if value == 1:
        return False
    elif value == 0:
        return True


def reserve_seat(seat_id):
    '''Reserves seat after successfull check if it's free and returns 
    a seat code which generates randomly.'''

    check = check_seat(seat_id)

    if not check:
        print('Sorry, your seat is occupied. Choose another one.')
        return
    
    if check:
        conn = sqlite3.connect(tickets_db)
        cursor = conn.cursor()

        cursor.execute('UPDATE Seat SET taken WHERE seat_id = ?', (seat_id, ))

        conn.commit()

        cursor.close()
        conn.close()


def get_seat_price(seat_id):
    '''Returns a price for reserving the given seat.'''

    conn = sqlite3.connect(tickets_db)
    cursor = conn.cursor()

    cursor.execute('SELECT price FROM Seat WHERE seat_id = ?', (seat_id, ))

    price = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return price


def check_money(card, amount):
    '''Checks if the card has enough money to pay.
    Returns True if there's enough and False if there's not.'''

    conn = sqlite3.connect(cards_db)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT Card.balance FROM Card JOIN Types 
    ON Card.type_id = Types.id 
    WHERE Card.number = ? AND Card.cvc = ? AND Card.holder = ? AND Types.type = ?
    ''', (card.num, card.cvc, card.name, card.type))

    try:
        balance = cursor.fetchone()[0]
    except:
        balance = None

    conn.commit()

    cursor.close()
    conn.close()

    if balance == None:
        return False

    if balance > amount:
        return True
    else:
        return False


def withdraw(card, amount):
    '''Withdraws a given amount of money after succesful check if 
    there is enough money on the balance.'''

    check = check_money(card, amount)

    if not check:
        print('Sorry, there was a problem with your operation.')
        return
    
    if check:
        conn = sqlite3.connect(cards_db)
        cursor = conn.cursor()

        # Get current card's balance
        cursor.execute('SELECT balance FROM Card WHERE number = ?', (card.num, ))
        balance = cursor.fetchone()[0]
        
        # Withdraw a given amount and save updated balance in a variable
        upd_balance = balance - amount

        # Set new updated balance
        cursor.execute('UPDATE Card SET balance = ? WHERE number = ?', (upd_balance, card.num))
        conn.commit()

        cursor.close()
        conn.close()

        print('Operation was successful.')
