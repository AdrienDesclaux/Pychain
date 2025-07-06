from transaction import Transaction
from block import Block
import time
from typing import List


class Blockchain:
    def __init__(self):
        self.difficulty = 6
        self.blocks: List[Block] = [self.genesis_block()]
        self.pending_transactions: List[Transaction] = []

    def genesis_block(self):
        block = Block(previous_hash="0", transactions=[], nonce=0, difficulty=self.difficulty)
        block.mine_block(self.difficulty)
        return block

    def get_latest_block(self):
        return self.blocks[-1]

    def create_new_block(self) -> Block:
        """Crée un nouveau bloc avec les transactions en attente"""
        if not self.pending_transactions:
            print("Aucune transaction en attente")
            return None
        
        new_block = Block(
            transactions=self.pending_transactions.copy(),
            previous_hash=self.get_latest_block().hash,
            difficulty=self.difficulty
        )
        
        # Miner le bloc
        new_block.mine_block(self.difficulty)
        
        # Ajouter le bloc à la chaîne
        self.blocks.append(new_block)
        
        # Vider les transactions en attente
        self.pending_transactions = []
        
        return new_block

    def calculate_difficulty(self, old_difficulty, actual_time_seconds, target_time_seconds=30 * 100):

        min_adjustment_factor = 0.25
        max_adjustment_factor = 4.0

        adjustment_factor = actual_time_seconds /   target_time_seconds
        adjustment_factor = max (min_adjustment_factor, min  (adjustment_factor, max_adjustment_factor))

        new_difficulty = old_difficulty *   adjustment_factor
        return new_difficulty

    def add_transaction(self, transaction):  # ✅ Corrigé: ajout de self et parameter
        """Ajoute une transaction à la liste des transactions en attente"""
        if not transaction:
            raise ValueError("Transaction cannot be None")
        
        self.pending_transactions.append(transaction)
        print(f"Transaction ajoutée: {transaction.sender} -> {transaction.recipient}: {transaction.amount}")

    def validate_chain(self):
        """Valide l'intégrité de la blockchain"""
        for i in range(1, len(self.blocks)):
            current_block = self.blocks[i]
            previous_block = self.blocks[i - 1]
            
            # Vérifier le hash du bloc actuel
            if current_block.hash != current_block.calculate_hash():
                print(f"Hash invalide pour le bloc {i}")
                return False
            
            # Vérifier la liaison avec le bloc précédent
            if current_block.previous_hash != previous_block.hash:
                print(f"Liaison invalide entre les blocs {i-1} et {i}")
                return False
        
        return True

    def get_balance(self, address):
        """Calcule le solde d'une adresse"""
        balance = 0
        
        for block in self.blocks:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.recipient == address:
                    balance += transaction.amount
        
        return balance

    def display_chain(self):
        """Affiche la blockchain complète"""
        print("\n" + "="*50)
        print("BLOCKCHAIN COMPLÈTE")
        print("="*50)
        
        for i, block in enumerate(self.blocks):
            print(f"\nBLOC {i}:")
            print(f"  Hash: {block.hash}")
            print(f"  Hash précédent: {block.previous_hash}")
            print(f"  Timestamp: {time.ctime(block.timestamp)}")
            print(f"  Nonce: {block.nonce}")
            print(f"  Transactions ({len(block.transactions)}):")
            
            for j, tx in enumerate(block.transactions):
                print(f"    {j+1}. {tx.sender} -> {tx.recipient}: {tx.amount}")

    def is_last_block_mined(self):
        """Vérifie si le dernier bloc a été miné
        
        Returns:
            bool: True si le dernier bloc a été miné et qu'il n'y a pas de transactions en attente,
                  False s'il y a des transactions en attente à miner
        """
        # Vérifie si le dernier bloc a un hash valide (commence par des zéros selon la difficulté)
        last_block = self.get_latest_block()
        if not last_block.hash.startswith('0' * self.difficulty):
            return False
            
        return True