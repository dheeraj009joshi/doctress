class Service:
    def __init__(self, username, email, password, profile_image, age, gender, phone, address, about,
                 city, state, country, adhar_card, company_name, company_address, account_status="pending",
                 membership=0, tickets=None, membership_trx=None, all_trx=None):
        self.username = username
        self.email = email
        self.password = password
        self.profile_image = profile_image
        self.age = age
        self.gender = gender
        self.phone = phone
        self.address = address
        self.about = about
        self.city = city
        self.state = state
        self.country = country
        self.adhar_card = adhar_card
        self.company_name = company_name
        self.company_address = company_address
        self.account_status = account_status
        self.membership = membership
        self.tickets = tickets if tickets is not None else []
        self.membership_trx = membership_trx if membership_trx is not None else {}
        self.all_trx = all_trx if all_trx is not None else []

    @staticmethod
    def from_dict(service_dict):
        return Service(
            service_dict['username'],
            service_dict['email'],
            service_dict['password'],
            service_dict['profile_image'],
            service_dict['age'],
            service_dict['gender'],
            service_dict['phone'],
            service_dict['address'],
            service_dict['about'],
            service_dict['city'],
            service_dict['state'],
            service_dict['country'],
            service_dict['adhar_card'],
            service_dict['company_name'],
            service_dict['company_address'],
            service_dict.get('account_status', "pending"),
            service_dict.get('membership', 0),
            service_dict.get('tickets', []),
            service_dict.get('membership_trx', {}),
            service_dict.get('all_trx', [])
        )

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'profile_image': self.profile_image,
            'age': self.age,
            'gender': self.gender,
            'phone': self.phone,
            'address': self.address,
            'about': self.about,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'adhar_card': self.adhar_card,
            'company_name': self.company_name,
            'company_address': self.company_address,
            'account_status': self.account_status,
            'membership': self.membership,
            'tickets': self.tickets,
            'membership_trx': self.membership_trx,
            'all_trx': self.all_trx
        }
