import json
import random

from datetime import datetime
from hashlib import sha256


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        # Creating the genesis block
        print("Creating genesis block")
        self.chain.append(self.new_block())

    def new_block(self, previous_hash=None):
        block = {
            'index': len(self.chain),
            'timestamp': datetime.utcnow().isoformat(),
            'transactions': self.pending_transactions,
            'previous_hash': self.last_block["hash"] if self.last_block else None,
            'nonce': format(random.getrandbits(64), "x"),
        }

        # Get the hash of this new block, and add it to the block
        block_hash = self.hash(block)
        block["hash"] = block_hash

        # Reset the list of pending transactions
        self.pending_transactions = []

        # Removed ad appending is now after Proof_of_Work completed
        # Add the block to the chain
        # self.chain.append(block)
        # print(f"Created block {block['index']}")

        return block

    @staticmethod
    def hash(block):
        # Ensure the dictionary variable is first sorted, so that there will be no inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        #print(block_string)
        return sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last block in the chain (if there are blocks)
        return self.chain[-1] if self.chain else None

    @staticmethod
    def valid_block(block):
        # Checking if a block's hash starts with 0000
        return block["hash"].startswith("0000")

    def proof_of_work(self):
        while True:
            new_block = self.new_block()
            if self.valid_block(new_block):
                break

        self.chain.append(new_block)
        print("Found a new block: ", new_block)
