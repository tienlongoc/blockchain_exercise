import hashlib

class Block:
    def __init__(self, message, prev_block_hash=0):
        self.message = message
        self.hash = hashlib.sha256(f"{message}{prev_block_hash}".encode("utf-8")).hexdigest()
    
    def __repr__(self):
        return f"{self.message},{self.hash}"


class Blockchain:
    def __init__(self, load_ledger_path=""):
        self.chain = []
        if load_ledger_path:
            self.read_ledger(load_ledger_path)

    def __repr__(self):
       return "\n".join(str(block) for block in self.chain)

    def insert_new_block(self, message):
        if self.chain:
            last_block_hash = self.chain[-1].hash
        else:
            last_block_hash = 0
        self.chain.append(Block(message, last_block_hash))

    def read_ledger(self, ledger_file_path):
        ledger_info = open(ledger_file_path).read().splitlines()
        for line in ledger_info:
            message, hash = line.split(",")
            self.insert_new_block(message)
            if str(self.chain[-1].hash) != str(hash):
                raise ValueError(f"Incorrect hash in ledger input -- item {len(self.chain)} has recorded hash {hash} whilst the calculated hash is {self.chain[-1].hash}")

    def print_ledger(self, ledger_file_path):
        with open(ledger_file_path, "w") as f:
            f.write(str(self))



# Sample usage
print("Instantiate a new empty blockchain")
my_blockchain = Blockchain()
print("")

print("Inserting a new block with message 'Test message 1'")
my_blockchain.insert_new_block("Test message 1")
print("")

print("Inserting a new block with message 'Test message 2'")
my_blockchain.insert_new_block("Test message 2")
print("")

print("Inserting a new block with message 'Test message 3'")
my_blockchain.insert_new_block("Test message 3")
print("")

print("My blockchain now looks like this:")
print(my_blockchain)
print("")

print("Now dump the record into a ledger path")
my_blockchain.print_ledger("ledger")
print("")


print("Retrieving the record back from the ledger path")
read_my_blockchain = Blockchain("ledger")
print("")

print("The retrieved record:")
print(read_my_blockchain)
print("")

print("Try to read a corrupted ledger record:")
bad_blockchain = Blockchain("bad_ledger")
