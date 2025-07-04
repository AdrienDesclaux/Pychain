# exemple_utilisation.py
from blockchain import Blockchain
from transaction import Transaction

def main():
    # Créer une blockchain
    blockchain = Blockchain()
    
    # Ajouter des transactions
    tx1 = Transaction("Alice", "Bob", 50)
    tx2 = Transaction("Bob", "Charlie", 25)
    
    blockchain.add_transaction(tx1)
    blockchain.add_transaction(tx2)
    
    # Miner un bloc
    blockchain.create_new_block()
    
    # Afficher la blockchain
    blockchain.display_chain()
    
    # Vérifier les soldes
    print(f"\nSolde Alice: {blockchain.get_balance('Alice')}")
    print(f"Solde Bob: {blockchain.get_balance('Bob')}")
    print(f"Solde Charlie: {blockchain.get_balance('Charlie')}")
    
    # Valider la blockchain
    print(f"\nBlockchain valide: {blockchain.validate_chain()}")

if __name__ == "__main__":
    main()