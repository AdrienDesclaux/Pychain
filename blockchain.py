from transaction import Transaction
from block import Block
import time
from typing import List


class Blockchain:
    def __init__(self):
        self.difficulty = 4
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
            # print("Aucune transaction en attente")
            return None

        print(f"Nombre de transactions en attente: {len(self.pending_transactions)}")    
        print(f"Premières transactions: {[f'{tx.sender[:10]}...-> {tx.recipient[:10]}...: {tx.amount}' for tx in self.pending_transactions[:5]]}")
        
        transactions_copy = self.pending_transactions.copy()
        print(f"Nombre de transactions copiées: {len(transactions_copy)}")
        
        new_block = Block(
            transactions=transactions_copy,
            previous_hash=self.get_latest_block().hash,
            difficulty=self.difficulty
        )

        print(f"Nouveau bloc créé avec {len(new_block.transactions)} transactions")
        
        # Miner le bloc
        new_block.mine_block(self.difficulty)
        
        print(f"Après minage, le bloc contient {len(new_block.transactions)} transactions")
        
        # Ajouter le bloc à la chaîne
        self.blocks.append(new_block)

        # Retirer les transactions qui sont passés dans le block
        self.pending_transactions = [tx for tx in self.pending_transactions if tx not in transactions_copy]
        
        return new_block

    def calculate_difficulty(self, old_difficulty, actual_time_seconds, target_time_seconds=30 * 100):

        min_adjustment_factor = 0.25
        max_adjustment_factor = 4.0

        adjustment_factor = actual_time_seconds /   target_time_seconds
        adjustment_factor = max (min_adjustment_factor, min  (adjustment_factor, max_adjustment_factor))

        new_difficulty = old_difficulty *   adjustment_factor
        return new_difficulty

    def add_transaction(self, transaction):
        """Ajoute une transaction à la liste des transactions en attente"""
        if not transaction:
            raise ValueError("Transaction cannot be None")
        
        self.pending_transactions.append(transaction)
        print(f"Transaction ajoutée: {transaction.sender} -> {transaction.recipient}: {transaction.amount}")
        print(f"Nombre de transactions en attente: {len(self.pending_transactions)}")

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

    def create_fake_transactions(self):
        """Créer des transactions aléatoires et les ajouter à la liste des transactions en attente
        Génère un nombre aléatoire entre 1 et 100 de transactions avec des montants et adresses aléatoires
        """
        import random
        import string
        
        # Générer un nombre aléatoire de transactions entre 1 et 100
        num_transactions = random.randint(1, 100)
        print(f"Génération de {num_transactions} transactions aléatoires...")
        
        # Liste d'adresses aléatoires pour simulation
        addresses = [
            "0x" + ''.join(random.choices(string.hexdigits, k=40)).lower() for _ in range(10)
        ]
        
        # Ajouter des adresses communes pour voir des soldes qui évoluent
        common_addresses = [
            "0xce8413cb205c0603269a283b0b4c46f5721a1f98",
            "0x19a762e00dd1F5F0fcC308782b9ad2A7B127DF93",
            "0x3a1d2d9f35472542c9a3a9a9dd0e1a4cb5c83787",
            "0xbd8cca1c56a35731d1ab7d0e24a45523fb30778a",
            "0x7cd5e2913b1ea3035f823c53fc8bc17f224c71e3"
        ]
        
        addresses.extend(common_addresses)
        
        for _ in range(num_transactions):
            sender = random.choice(addresses)
            recipient = random.choice([addr for addr in addresses if addr != sender])
            amount = random.randint(1, 1000)
            
            tx = Transaction(sender, recipient, amount)
            self.add_transaction(tx)
        
        print(f"{len(self.pending_transactions)} transactions aléatoires ajoutées")
        return num_transactions

    def is_last_block_mined(self):
        """Vérifie si le dernier bloc a été miné
        
        Returns:
            bool: True si le dernier bloc a été miné et qu'il n'y a pas de transactions en attente,
                  False s'il y a des transactions en attente à miner
        """
        last_block = self.get_latest_block()
        if not last_block.is_mined:
            return False
            
        return True