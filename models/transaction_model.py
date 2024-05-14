class Transaction:
    def __init__(self, trx_id="", trx_amount=""):
        self.trx_id = trx_id
        self.trx_amount = trx_amount

    @staticmethod
    def from_dict(transaction_dict):
        return Transaction(
            transaction_dict.get('trx_id', ""),
            transaction_dict.get('trx_amount', "")
        )

    def to_dict(self):
        return {
            'trx_id': self.trx_id,
            'trx_amount': self.trx_amount
        }
