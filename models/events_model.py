class Event:
    def __init__(self, event_title="", event_date="", event_start_time="", event_price="", event_location="", event_thumbnail="", event_video="", event_ticket_template=""):
        self.event_title = event_title
        self.event_date = event_date
        self.event_start_time = event_start_time
        self.event_price = event_price
        self.event_location = event_location
        self.event_thumbnail = event_thumbnail
        self.event_video = event_video
        self.event_ticket_template = event_ticket_template

    @staticmethod
    def from_dict(event_dict):
        return Event(
            event_dict.get('event_title', ""),
            event_dict.get('event_date', ""),
            event_dict.get('event_start_time', ""),
            event_dict.get('event_price', ""),
            event_dict.get('event_location', ""),
            event_dict.get('event_thumbnail', ""),
            event_dict.get('event_video', ""),
            event_dict.get('event_ticket_template', "")
        )

    def to_dict(self):
        return {
            'event_title': self.event_title,
            'event_date': self.event_date,
            'event_start_time': self.event_start_time,
            'event_price': self.event_price,
            'event_location': self.event_location,
            'event_thumbnail': self.event_thumbnail,
            'event_video': self.event_video,
            'event_ticket_template': self.event_ticket_template
        }
