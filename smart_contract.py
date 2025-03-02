import requests

# Flask server URL
BASE_URL = "http://127.0.0.1:5000"

def add_transaction(sender, recipient, amount):
    """Send a transaction request to the Flask server"""
    data = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount
    }
    response = requests.post(f"{BASE_URL}/add_transaction", json=data)
    print(response.json())

def mine_block():
    """Request to mine a new block"""
    response = requests.get(f"{BASE_URL}/mine")
    print(response.json())

def get_chain():
    """Fetch and display the blockchain"""
    response = requests.get(f"{BASE_URL}/get_chain")
    print(response.json())

if __name__ == "__main__":
    print("Adding transaction...")
    add_transaction("Alice", "Bob", 50)

    print("Mining a new block...")
    mine_block()

    print("Fetching the blockchain data...")
    get_chain()
