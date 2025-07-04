from flask import Flask, jsonify, request
from flask_cors import CORS
from blockchain import Blockchain
from transaction import Transaction

app = Flask(__name__)
CORS(app)

blockchain = Blockchain()

def serialize_transaction(tx):
    return {
        'sender': tx.sender,
        'recipient': tx.recipient,
        'amount': tx.amount
    }

def serialize_block(block):
    return {
        'hash': block.hash,
        'previous_hash': block.previous_hash,
        'timestamp': block.timestamp,
        'nonce': block.nonce,
        'transactions': [serialize_transaction(tx) for tx in block.transactions]
    }

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify([serialize_block(block) for block in blockchain.blocks])

@app.route('/mine', methods=['POST'])
def mine_block():
    block = blockchain.create_new_block()
    if block:
        return jsonify(serialize_block(block))
    else:
        return jsonify({'message': 'Aucune transaction à miner'}), 400

@app.route('/transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    try:
        tx = Transaction(
            sender=data['sender'],
            recipient=data['recipient'],
            amount=data['amount']
        )
        blockchain.add_transaction(tx)
        return jsonify({'message': 'Transaction ajoutée'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/validate', methods=['GET'])
def validate_chain():
    valid = blockchain.validate_chain()
    return jsonify({'valid': valid})

@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    balance = blockchain.get_balance(address)
    return jsonify({'address': address, 'balance': balance})

if __name__ == '__main__':
    app.run(port=5000)
