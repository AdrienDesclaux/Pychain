import time

class Block:
    def __init__(self, previous_hash, transactions, nonce, difficulty):
        self.transactions = transactions
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
        self.difficulty = difficulty

    def add_transaction(self, transaction):
        if transaction is None:
            raise ValueError("Transaction cannot be None")
        self.transaction.append(transaction)

    def calculate_hash(self):
        import hashlib
        block_string = f"{self.previous_hash}{self.timestamp}{self.nonce}{self.transactions}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def calculate_difficulty(self, old_difficulty, actual_time_seconds, target_time_seconds=30 * 100):  #ajoustement tout les les 30 minutes
        min_adjustment_factor = 0.25
        max_adjustment_factor = 4.0

        adjustment_factor = actual_time_seconds / target_time_seconds
        adjustment_factor = max(min_adjustment_factor, min(adjustment_factor, max_adjustment_factor))

        new_difficulty = old_difficulty * adjustment_factor
        return new_difficulty
    
    def get_timestamp(self):
        return self.timestamp
    
    