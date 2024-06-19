import requests
import time

node_url = "http://localhost:5000"
peer_urls = []

def add_block(badge_number):
    timestamp = int(time.time() * 1000)  # Get current time in milliseconds
    data = f"Badge Number: {badge_number}, Timestamp: {timestamp}"
    response = requests.post(f"{node_url}/add_block", json={'data': data})
    if response.status_code == 201:
        print("Block added:", response.json())
    else:
        print("Failed to add block:", response.text)

def get_blockchain():
    response = requests.get(f"{node_url}/blockchain")
    if response.status_code == 200:
        blockchain = response.json()
        for block in blockchain:
            print(block)
    else:
        print("Failed to retrieve blockchain:", response.text)

def validate_blockchain():
    response = requests.get(f"{node_url}/validate")
    if response.status_code == 200:
        is_valid = response.json().get('is_valid')
        print("Is blockchain valid?", is_valid)
    else:
        print("Failed to validate blockchain:", response.text)

def register_peers():
    for peer_url in peer_urls:
        response = requests.post(f"{node_url}/register_node", json={'node_url': peer_url})
        if response.status_code == 201:
            print("Registered peer:", peer_url)
        else:
            print("Failed to register peer:", peer_url)

def discover_peers():
    global peer_urls
    for port in range(5000, 5006):
        peer_url = f"http://localhost:{port}"
        try:
            response = requests.get(f"{peer_url}/nodes")
            if response.status_code == 200:
                peer_urls.append(peer_url)
                print(f"Discovered peer: {peer_url}")
        except requests.ConnectionError:
            print(f"Could not connect to {peer_url}")

# Discover and register peers
discover_peers()
register_peers()

# Example usage: interactively add data to the blockchain
while True:
    user_input = input("Enter badge number to store in the blockchain (or 'exit' to finish): ")
    if user_input.lower() == 'exit':
        break
    add_block(user_input)

get_blockchain()
validate_blockchain()
