from flask import Flask, jsonify, request, render_template
import hashlib
import json
import time

# Ensure Flask finds the templates folder
app = Flask(__name__, template_folder="templates")


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_block(proof=1, previous_hash="0")  # Genesis Block

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        return self.get_last_block()['index'] + 1

    def get_last_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        while not self.validate_proof(previous_proof, new_proof):
            new_proof += 1
        return new_proof

    def validate_proof(self, previous_proof, new_proof):
        guess = f'{previous_proof}{new_proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def mine_block(self):
        last_block = self.get_last_block()
        previous_proof = last_block['proof']
        proof = self.proof_of_work(previous_proof)
        previous_hash = self.hash(last_block)
        return self.create_block(proof, previous_hash)

    @staticmethod
    def hash(block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()


# Create blockchain instance
blockchain = Blockchain()


@app.route("/")
def home():
    print("📌 Serving index.html")  # Debugging message
    return render_template("index.html")  # Ensure index.html is in /templates


@app.route("/get_chain", methods=["GET"])
def get_chain():
    print("🔍 Fetching Blockchain Data...")  # Debugging message
    if blockchain.chain:
        return jsonify({"chain": blockchain.chain, "length": len(blockchain.chain)}), 200
    else:
        return jsonify({"error": "❌ Blockchain is empty."}), 500


@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    data = request.get_json()

    if not data or "sender" not in data or "recipient" not in data or "amount" not in data:
        print("🚨 Missing required fields!")  # Debugging
        return jsonify({"error": "❌ Missing required fields"}), 400

    sender = data["sender"].strip()
    recipient = data["recipient"].strip()
    amount = data["amount"]

    if not sender or not recipient or not isinstance(amount, (int, float)) or amount <= 0:
        print("🚨 Invalid transaction data!")  # Debugging
        return jsonify({"error": "❌ Invalid input: Sender, Recipient, and Amount must be valid."}), 400

    index = blockchain.add_transaction(sender, recipient, amount)
    print(f"✅ Transaction added to Block {index}")  # Debugging
    return jsonify({"message": f"✅ Transaction will be added to Block {index}"}), 201


@app.route("/mine", methods=["GET"])
def mine():
    if not blockchain.pending_transactions:
        print("🚨 Mining failed! No transactions available.")  # Debugging log
        return jsonify({"error": "❌ Mining failed! No transactions in the pool."}), 400

    print("⛏️ Mining a new block...")  # Debugging log
    block = blockchain.mine_block()

    if block:
        print(f"✅ Block {block['index']} mined successfully!")  # Debugging log
        return jsonify({"message": "✅ New Block Mined!", "block": block}), 200
    else:
        print("❌ Mining failed!")  # Debugging log
        return jsonify({"error": "❌ Mining failed."}), 500


if __name__ == "__main__":
    print("🚀 Starting Flask Blockchain Server...")
    app.run(debug=True)
