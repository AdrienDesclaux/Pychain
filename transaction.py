import time

class Transaction:
    def __init__(self, sender, recipient, amount, timestamp=None):
        if not sender or not recipient or amount <= 0:
            raise ValueError("Invalid transaction parameters")
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp or time.time()
        # Pas de block_hash ici - la transaction existe avant d'être dans un bloc

    def get_details(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp
        }
    
    def to_string(self):
        """Convertit la transaction en string pour le hachage"""
        return f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"