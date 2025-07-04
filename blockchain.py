from .transaction import Transaction
from .block import Block

class Blockchain:
    def __init__(self):
        self.blocks: List[Block] = [self.genesis_block()]
        self.pending_transactions: List[Transaction] = []
        self.difficulty = 4

    def genesis_block(self):
        block = Block(previous_hash="0", transactions=[], nonce=0, difficulty=self.difficulty)

    def get_latest_block(self):
        return self.chain[-1]

    def create_new_block(self) -> Block:
        """Crée un nouveau bloc avec les transactions en attente"""
        if not self.pending_transactions:
            print("Aucune transaction en attente")
            return None
        
        new_block = Block(
            transactions=self.pending_transactions.copy(),
            previous_hash=self.get_latest_block().hash
        )
        
        # Miner le bloc
        new_block.mine_block(self.difficulty)
        
        # Ajouter le bloc à la chaîne
        self.chain.append(new_block)
        
        # Vider les transactions en attente
        self.pending_transactions = []
        
        return new_block

    def calculate_difficulty(self, old_difficulty, actual_time_seconds, target_time_seconds=30 * 100):
        """Calcule la difficulté du minage en fonction du temps écoulé"""
        min_adjustment_factor = 0.25
        max_adjustment_factor = 4.0

        adjustment_factor = actual_time_seconds / target_time_seconds
        adjustment_factor = max(min_adjustment_factor, min(adjustment_factor, max_adjustment_factor))

        new_difficulty = old_difficulty * adjustment_factor
        return new_difficulty

    def add_transaction():
        """Ajoute une transaction à la liste des transactions en attente"""
        if not transaction:
            raise ValueError("Transaction cannot be None")
        
        self.pending_transactions.append(transaction)

         
    
          