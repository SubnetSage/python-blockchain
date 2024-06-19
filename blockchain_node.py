from flask import Flask, request, jsonify
import hashlib
import time
import requests
import json
import os
from datetime import datetime
import argparse
import logging

app = Flask(__name__)

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def __repr__(self):
        return f"Block(index={self.index}, previous_hash='{self.previous_hash}', timestamp={self.timestamp}, data='{self.data}', hash='{self.hash}')"

def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + previous_hash + str(timestamp) + data
    return hashlib.sha256(value.encode()).hexdigest()

def create_genesis_block():
    timestamp = int(time.time() * 1000)
    return Block(0, "0", timestamp, "Genesis Block", calculate_hash(0, "0", timestamp, "Genesis Block"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time() * 1000)
    previous_hash = previous_block.hash
    hash = calculate_hash(index, previous_hash, timestamp, data)
    return Block(index, previous_hash, timestamp, data, hash)

def is_chain_valid(chain):
    for i in range(1, len(chain)):
        current_block = chain[i]
        previous_block = chain[i - 1]

        # Check if the hash of the current block is correct
        if current_block.hash != calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data):
            logging.error(f"Invalid hash at block {current_block.index}")
            return False

        # Check if the previous hash matches
        if current_block.previous_hash != previous_block.hash:
            logging.error(f"Invalid previous hash at block {current_block.index}")
            return False

    return True

def save_blockchain(chain, filename):
    with open(filename, 'w') as f:
        json.dump([block.__dict__ for block in chain], f)

def load_blockchain(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            return [Block(**block) for block in data]
    else:
        return [create_genesis_block()]

@app.route('/add_block', methods=['POST'])
def add_block():
    data = request.json.get('data')
    if data is None:
        logging.error("Invalid data received for new block")
        return "Invalid data", 400

    # Load the current blockchain
    blockchain = load_blockchain(filename)

    previous_block = blockchain[-1]
    new_block = create_new_block(previous_block, data)
    blockchain.append(new_block)

    # Save the updated blockchain to the file
    save_blockchain(blockchain, filename)
    logging.info(f"New block added: {new_block}")

    # Notify peers about the new block
    for peer in peers:
        try:
            requests.post(f"{peer}/new_block", json=new_block.__dict__)
            logging.info(f"Notified peer {peer} about new block")
        except Exception as e:
            logging.error(f"Could not notify peer {peer}: {e}")

    return jsonify(new_block.__dict__), 201

@app.route('/new_block', methods=['POST'])
def new_block():
    block_data = request.json
    blockchain = load_blockchain(filename)
    
    # Check if the block is already in the blockchain to avoid duplication
    if any(b.index == block_data['index'] and b.hash == block_data['hash'] for b in blockchain):
        logging.info(f"Block {block_data['index']} already exists")
        return "Block already exists", 200

    block = Block(block_data['index'], block_data['previous_hash'], block_data['timestamp'], block_data['data'], block_data['hash'])
    blockchain.append(block)

    # Save the updated blockchain to the file
    save_blockchain(blockchain, filename)
    logging.info(f"New block received and added: {block}")

    return "Block added", 201

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    blockchain = load_blockchain(filename)
    return jsonify([block.__dict__ for block in blockchain]), 200

@app.route('/validate', methods=['GET'])
def validate_blockchain():
    blockchain = load_blockchain(filename)
    is_valid = is_chain_valid(blockchain)
    logging.info(f"Blockchain validation result: {is_valid}")
    return jsonify({'is_valid': is_valid}), 200

@app.route('/register_node', methods=['POST'])
def register_node():
    node_url = request.json.get('node_url')
    if node_url is None:
        logging.error("Invalid node URL received for registration")
        return "Invalid node URL", 400

    peers.add(node_url)
    logging.info(f"Node registered: {node_url}")
    return jsonify(list(peers)), 201

@app.route('/nodes', methods=['GET'])
def get_nodes():
    return jsonify(list(peers)), 200

@app.route('/sync', methods=['GET'])
def sync():
    blockchain = load_blockchain(filename)
    for peer in peers:
        try:
            response = requests.get(f"{peer}/blockchain")
            peer_chain = response.json()
            new_blocks = get_blockchain_difference(blockchain, peer_chain)
            for block in new_blocks:
                blockchain.append(Block(**block))
            save_blockchain(blockchain, filename)
            logging.info(f"Synchronized with peer {peer}")
        except Exception as e:
            logging.error(f"Could not sync with peer {peer}: {e}")

    return jsonify([block.__dict__ for block in blockchain]), 200

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Blockchain Node')
    parser.add_argument('--port', type=int, default=5000, help='port to run the server on')
    args = parser.parse_args()
    
    # Set the filename for the blockchain JSON file
    filename = "blockchain.json"
    
    # Load the blockchain from the file or create a new one if it doesn't exist
    blockchain = load_blockchain(filename)
    peers = set()

    # Configure logging
    log_filename = f"blockchain_node_{args.port}.log"
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        handlers=[logging.FileHandler(log_filename), logging.StreamHandler()])

    logging.info("Starting blockchain node")
    app.run(host='0.0.0.0', port=args.port)
