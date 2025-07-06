# main.py - Blockchain avec mining continu et API
import time
import threading
import sys
from blockchain import Blockchain
from transaction import Transaction
from flask import Flask
from api import app
from blockchain_instance import blockchain


def start_api_server():
    """Démarre le serveur API Flask dans un thread séparé"""
    print("Démarrage du serveur API sur http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, threaded=True)

def continuous_mining():
    """Fonction de mining continu pour la blockchain"""
    while True:
        # Vérifier s'il y a des transactions en attente
        if blockchain.pending_transactions:
            print(f"\n[*] Mining en cours avec {len(blockchain.pending_transactions)} transactions...")
            if blockchain.is_last_block_mined():
                new_block = blockchain.create_new_block()
                if new_block:
                    print(f"[+] Nouveau bloc miné! Hash: {new_block.hash[:10]}...")
                    blockchain.display_chain()
                
                # Afficher quelques soldes d'exemple
                if blockchain.blocks and len(blockchain.blocks) > 1:
                    print("\nExemple de soldes:")
                    for address in set([tx.sender for tx in new_block.transactions] + [tx.recipient for tx in new_block.transactions]):
                        if address != "SYSTEM": 
                            print(f"Solde {address}: {blockchain.get_balance(address)}")

def main():
    # Créer un thread pour l'API
    api_thread = threading.Thread(target=start_api_server)
    api_thread.daemon = True
    api_thread.start()
    
    print("Pychain démarré!")
    print("API disponible sur http://localhost:5000")
    
    try:
        # Démarrer le mining continu
        continuous_mining()
    except KeyboardInterrupt:
        print("\n[!] Arrêt de la blockchain")
        sys.exit(0)

if __name__ == "__main__":
    main()