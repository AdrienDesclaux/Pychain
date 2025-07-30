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
        if blockchain.is_last_block_mined() and len(blockchain.pending_transactions) > 50:
            new_block = blockchain.create_new_block()
            if new_block:
                print(f"[+] Nouveau bloc miné! Hash: {new_block.hash[:10]}...")
                blockchain.display_chain()

def main():
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