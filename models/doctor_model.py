class Doctor:
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
    def from_dict(doctor_dict):
        return Doctor(
            doctor_dict['username'],
            doctor_dict['email'],
            doctor_dict['password'],
            doctor_dict['profile_image'],
            doctor_dict['fname'],
            doctor_dict['phone'],
            doctor_dict['address'],
            doctor_dict['about'],
            doctor_dict.get('tickets', []),
            doctor_dict.get('all_trx', [])
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
