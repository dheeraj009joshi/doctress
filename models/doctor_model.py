class DOCTOR:
    def __init__(self, username, email, password, profile_image, fname, phone, address, about, tickets=None, all_trx=None):
        self.username = username
        self.email = email
        self.password = password
        self.profile_image = profile_image
        self.fname = fname
        self.phone = phone
        self.address = address
        self.about = about
        self.tickets = tickets if tickets is not None else []
        self.all_trx = all_trx if all_trx is not None else []

    @staticmethod
    def from_dict(user_dict):
        return DOCTOR(
            user_dict['username'],
            user_dict['email'],
            user_dict['password'],
            user_dict['profile_image'],
            user_dict['fname'],
            user_dict['phone'],
            user_dict['address'],
            user_dict['about'],
            user_dict.get('tickets', []),
            user_dict.get('all_trx', [])
        )

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'profile_image': self.profile_image,
            'fname': self.fname,
            'phone': self.phone,
            'address': self.address,
            'about': self.about,
            'tickets': self.tickets,
            'all_trx': self.all_trx
        }
