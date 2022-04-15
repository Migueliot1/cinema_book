from fpdf import FPDF 

class PdfReport:
    '''Represents a pdf ticket file which would be generated 
    after successfull reserving of the given seat.'''

    def __init__(self, filename):
        '''Create an instance with a filename as a paramete.r'''

        self.filename = filename

    def generate(self, name, seat_num, seat_id, price):
        '''Generate a pdf file from given data: name, 
        seat number, ticket id, and ticket price.'''

        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        # Add a title
        pdf.set_font(family='Arial', size=28, style='B')
        pdf.cell(w=0, h=80, txt='Your Digital Ticket', border=1, align='C', ln=1)

        # Add Name label and its value
        pdf.set_font(family='Arial', size = 18, style='B')
        pdf.cell(w=150, h=40, txt='Name', border=1,)
        pdf.set_font(family='Arial', size = 18)
        pdf.cell(w=0, h=40, txt=name, border=1, ln=1)

        # Add Seat Number
        pdf.set_font(family='Arial', size = 18, style='B')
        pdf.cell(w=150, h=40, txt='Seat Number', border=1)
        pdf.set_font(family='Arial', size = 18)
        pdf.cell(w=0, h=40, txt=seat_num, border=1, ln=1)

        # Add TicketID 
        pdf.set_font(family='Arial', size = 18, style='B')
        pdf.cell(w=150, h=40, txt='Ticket ID', border=1)
        pdf.set_font(family='Arial', size = 18)
        pdf.cell(w=0, h=40, txt=seat_id, border=1, ln=1)

        # Add Price
        pdf.set_font(family='Arial', size = 18, style='B')
        pdf.cell(w=150, h=40, txt='Price', border=1)
        pdf.set_font(family='Arial', size = 18)
        pdf.cell(w=0, h=40, txt=price, border=1, ln=20)

        print('New PDF file', self.filename, 'was succesfully generated :)')
        pdf.output(self.filename)
