import block

class Blockchain:
    def __init__(self):
        self.chain = [self.genesis_block()]
        self.pending_transactions = []

    def genesis_block(self):
        block = Block(previous_hash="0", transactions=[], nonce=0, difficulty=4)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, block):
        if block.previous_hash != self.get_latest_block().hash:
            raise ValueError("Invalid block: previous hash does not match")
        self.chain.append(block)

    def add_transaction():

         
    
          