import sqlite3

from hidden import get_tickets_db


class Seat_in_db:
    '''Handles doing stuff with seat inside of a database when 
    user wants to reserve this seat or check if it's free.'''

    tickets_db = get_tickets_db()

    def __init__(self, seat):
        '''Instantiate with number of a seat user wants to reserve.'''

        self.seat = seat
    

    def check_seat(self):
        '''Checks if the given seat is taken or not.
        Returns True if the seat is free and False if it's not.'''

        conn = sqlite3.connect(self.tickets_db)
        cursor = conn.cursor()

        cursor.execute('SELECT taken FROM Seat WHERE seat_id = ?', (self.seat, ))

        value = cursor.fetchone()[0]

        conn.commit()

        cursor.close()
        conn.close()

        if value == 1:
            return False
        elif value == 0:
            return True


    def get_seat_price(self):
        '''Returns a price for reserving the given seat.'''

        conn = sqlite3.connect(self.tickets_db)
        cursor = conn.cursor()

        cursor.execute('SELECT price FROM Seat WHERE seat_id = ?', (self.seat, ))

        price = cursor.fetchone()[0]

        conn.commit()

        cursor.close()
        conn.close()

        return price


    def reserve_seat(self):
        '''Reserves seat after successfull check if it's free and returns 
        a seat code which generates randomly.'''

        check = self.check_seat()

        if not check:
            print('Sorry, your seat is occupied. Choose another one.')
            return
        
        if check:
            conn = sqlite3.connect(self.tickets_db)
            cursor = conn.cursor()

            cursor.execute('UPDATE Seat SET taken = ? WHERE seat_id = ?', (1, self.seat))

            conn.commit()

            cursor.close()
            conn.close()
