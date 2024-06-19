## README: Blockchain Application

### Overview

This blockchain application allows for a decentralized ledger where blocks of data can be added and validated across multiple nodes. It is built using Python and Flask, providing a simple yet functional implementation of a blockchain network.

### Components

1. **`blockchain_node.py`**: This file contains the server-side logic for the blockchain node. Each node can add blocks, validate the blockchain, and sync with peers.
2. **`blockchain_client.py`**: This file contains the client-side logic to interact with the blockchain nodes. It allows adding blocks, retrieving the blockchain, validating the blockchain, and discovering/registering peer nodes.
3. **`deploy-nodes.py`**: This script launches multiple instances of the blockchain nodes to simulate a network of nodes.

### How the Blockchain Works

1. **Block Structure**: Each block contains an index, previous hash, timestamp, data, and hash. The hash is calculated based on the block's contents to ensure integrity.
2. **Genesis Block**: The first block in the blockchain is the genesis block, created with predefined values.
3. **Adding Blocks**: Blocks are added to the blockchain by creating a new block with a reference to the previous block's hash, ensuring the chain's integrity.
4. **Validation**: The blockchain can be validated by checking the hashes and previous hashes of each block.
5. **Peers and Synchronization**: Nodes can register peers and synchronize their blockchains to maintain consistency across the network.

### How to Use

#### Setting Up the Environment

1. **Install Dependencies**:
   - Ensure you have Python installed.
   - Install necessary packages using pip:
     ```sh
     pip install Flask requests
     ```

2. **Launch Blockchain Nodes**:
   - Run the `deploy-nodes.py` script to start multiple instances of the blockchain node:
     ```sh
     python deploy-nodes.py
     ```
   - Enter the number of nodes you want to launch (e.g., 3). This will start nodes on ports 5000, 5001, 5002, etc.

#### Interacting with the Blockchain

1. **Add Blocks**:
   - Run the `blockchain_client.py` script to interact with the blockchain:
     ```sh
     python blockchain_client.py
     ```
   - Follow the interactive prompt to add badge numbers to the blockchain. Enter 'exit' to stop.

2. **Retrieve Blockchain**:
   - The client script will automatically retrieve and display the current blockchain.

3. **Validate Blockchain**:
   - The client script will automatically validate the blockchain.

4. **Discover and Register Peers**:
   - The client script will discover and register peer nodes automatically.

#### API Endpoints (Node)

- **Add Block**: `POST /add_block`
  - Request Body: `{"data": "Block data"}`
  - Response: Details of the added block.

- **Retrieve Blockchain**: `GET /blockchain`
  - Response: JSON representation of the blockchain.

- **Validate Blockchain**: `GET /validate`
  - Response: JSON indicating whether the blockchain is valid.

- **Register Node**: `POST /register_node`
  - Request Body: `{"node_url": "http://localhost:5001"}`
  - Response: List of registered peers.

- **Retrieve Nodes**: `GET /nodes`
  - Response: List of peer nodes.

- **Sync Blockchain**: `GET /sync`
  - Response: JSON representation of the synchronized blockchain.

### Code Structure and Details

#### `blockchain_node.py`

- **Block Class**: Defines the structure of a block.
- **create_genesis_block**: Creates the initial block.
- **create_new_block**: Adds a new block to the blockchain.
- **is_chain_valid**: Validates the blockchain.
- **Flask Routes**: Defines various endpoints for adding blocks, retrieving the blockchain, validating it, and managing peers.

#### `blockchain_client.py`

- **add_block**: Sends a request to add a block.
- **get_blockchain**: Retrieves the blockchain.
- **validate_blockchain**: Validates the blockchain.
- **register_peers**: Registers peer nodes.
- **discover_peers**: Discovers peer nodes.
- **Interactive Prompt**: Allows the user to add data to the blockchain.

#### `deploy-nodes.py`

- **launch_flask_servers**: Launches multiple Flask servers on different ports.

### Conclusion

This blockchain application demonstrates a basic implementation of a blockchain network with nodes that can add, validate, and sync blocks. By running the provided scripts, you can simulate a decentralized network and interact with the blockchain through a simple client interface.
