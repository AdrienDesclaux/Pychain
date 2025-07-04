
class Transaction:
    def __init__(self, sender, recipient, amount, timestamp, block_hash):
        if not sender or not recipient or amount <= 0:
            raise ValueError("Invalid transaction parameters")
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp
        self.block_hash = block_hash

    def get_details(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "block_hash": self.block_hash
        }


