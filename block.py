import time

class Block:
    def __init__(self, previous_hash, transactions, nonce, difficulty):
        self.transaction: List[Transaction] = transactions
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
        block_string = f"{self.previous_hash}{self.timestamp}{self.nonce}{self.transaction}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self):
        """
        Mines the block by finding a nonce that produces a hash with a prefix of '0' * difficulty.
        """
        self.nonce = 0
        computed_hash = self.calculate_hash()
        target = '0' * self.difficulty
        while not computed_hash.startswith(target):
            self.nonce += 1
            computed_hash = self.calculate_hash()
        self.hash = computed_hash
    
    def get_timestamp(self):
        return self.timestamp