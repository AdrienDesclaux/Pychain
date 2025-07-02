
class Block:
    def __init__(self, previous_hash, transaction=None, ):
        self.transaction = None
        self.timestamp = None
        self.previous_hash = previous_hash
        self.nonce = None
        self.hash = self.calculate_hash()

    def add_transaction(self, transaction):
        if transaction is None:
            raise ValueError("Transaction cannot be None")
        self.transaction.append(transaction)


