import time
import hashlib
from typing import List
from transaction import Transaction

class Block:
    def __init__(self, previous_hash, transactions, nonce=0, difficulty=4):
        self.transactions: List[Transaction] = transactions or []
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.difficulty = difficulty
        self.hash = self.calculate_hash()

    def add_transaction(self, transaction):
        if transaction is None:
            raise ValueError("Transaction cannot be None")
        self.transactions.append(transaction)

    def calculate_hash(self):
        """Calcule le hash du bloc"""
        # Convertir les transactions en string pour le hachage
        transactions_string = "".join([tx.to_string() for tx in self.transactions])
        block_string = f"{self.previous_hash}{self.timestamp}{self.nonce}{transactions_string}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty=None):
        """
        Mine le bloc en cherchant un nonce qui produit un hash avec le préfixe requis
        """
        if difficulty is None:
            difficulty = self.difficulty
            
        self.nonce = 0
        target = '0' * difficulty
        
        print(f"Minage du bloc... Difficulté: {difficulty}")
        
        while True:
            self.hash = self.calculate_hash()
            if self.hash.startswith(target):
                print(f"Bloc miné! Nonce: {self.nonce}, Hash: {self.hash}")
                break
            self.nonce += 1
            
            # Affichage du progrès
            if self.nonce % 10000 == 0:
                print(f"Tentative {self.nonce}...")
    
    def get_timestamp(self):
        return self.timestamp