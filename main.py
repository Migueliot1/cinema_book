from functs import CinemaUser
from functs_seat import Seat_in_db
from functs_card import Card_in_db
from pdf_maker import PdfReport

# An introduction
print('Hey! Welcome to the Cinema ticket booking app!')
print('Follow the instructions and you\'ll be able to book the seat you want!\n')

inp = input('Enter \'start\' to start: ')

while inp == 'start':

    name = input('Your full name: ')
    seat = input('Preferred seat number: ')
    card_type = input('Your card type (Visa, MasterCard, UnionPay): ')
    card_num = input('Your card number: ')
    card_cvc = input('Your card CVC: ')
    card_name = input('Card holder name (type \'y\' if it\' the same as your full name): ')
    if card_name == 'y':
        card_name = name

    # Make user instance from input
    user = CinemaUser(name, seat)
    user.add_card(card_type, card_num, card_cvc, card_name)

    seat_db = Seat_in_db(user.seat)

    # Check if the seat is free
    if not seat_db.check_seat():
        print('The seat is occupied. Please choose another.')
        inp = input('If you want to continue, type \'start\': ')
        if inp == 'start':
            continue # quit out of loop
        else:
            quit()

    # Try to reserve the seat if there's enough money for purchase
    ticket_price = seat_db.get_seat_price()
    card_db = Card_in_db(user.card, ticket_price)
    
    print('The seat', user.seat, 'costs', ticket_price, '. You ok with this?')
    confirm = input('Type \'y\' if yes or anything else if no: ')

    if confirm != 'y':
        print('Abrupting operation...')
        continue

    reserve_try = card_db.withdraw()
    seat_id = None

    if reserve_try:
        seat_id = seat_db.reserve_seat()
        print('\nYour seat has been successfully reserved.')
        # print('Generating PDF ticket...')
    else:
        print('\nSeems like there was a problem in reserving. Try again.')
        inp = input('If you want to continue, type \'start\': ')
        continue
    
    if seat_id != None:
        pdf = PdfReport('ticket.pdf')
        pdf.generate(name=user.name, seat_num=user.seat, seat_id=seat_id, price=ticket_price)

    inp = input('If you want to book another ticket, type \'start\': ')