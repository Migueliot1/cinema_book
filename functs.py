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
