class Ticket:
    def __init__(self, ticket_price="", ticket_name="", ticket_date="", ticket_template=""):
        self.ticket_price = ticket_price
        self.ticket_name = ticket_name
        self.ticket_date = ticket_date
        self.ticket_template = ticket_template

    @staticmethod
    def from_dict(ticket_dict):
        return Ticket(
            ticket_dict.get('ticket_price', ""),
            ticket_dict.get('ticket_name', ""),
            ticket_dict.get('ticket_date', ""),
            ticket_dict.get('ticket_template', "")
        )

    def to_dict(self):
        return {
            'ticket_price': self.ticket_price,
            'ticket_name': self.ticket_name,
            'ticket_date': self.ticket_date,
            'ticket_template': self.ticket_template
        }
