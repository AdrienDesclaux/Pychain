"""
Module fournissant une instance unique de la blockchain
Ce module agit comme un singleton pour partager la même instance de blockchain
entre différents composants de l'application (API, mining, etc.)
"""
from blockchain import Blockchain

# Instance unique de blockchain partagée entre tous les modules
blockchain = Blockchain()
