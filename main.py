import mysql.connector
import time
from web3 import Web3

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/393d646a0c44480cb66f7efda9fbcab7"))

# Check connection to Ganache
if not web3.is_connected():
    print("Failed to connect to Ganache")
    exit()
else:
    print("Connected to Ganache")

# Connect to MySQL database
def connect_to_db():
    try:
        db = mysql.connector.connect(
            host="192.168.0.106",
            user="root",
            passwd="admin",
            database="blockchain_db"
        )
        print("Connected to MySQL database")
        return db
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        exit()

db = connect_to_db()
cursor = db.cursor()

def monitor_blocks():
    new_block_filter = web3.eth.filter('latest')
    print("Monitoring new blocks...")
    try:
        while True:
            print("Checking for new blocks...")
            # Fetch new entries from the filter
            new_entries = new_block_filter.get_new_entries()
            print(f"New entries: {new_entries}")

            for block_hash in new_entries:
                try:
                    # Fetch the block with full transactions
                    block = web3.eth.get_block(block_hash, full_transactions=True)
                    print(f"Block fetched: {block_hash.hex()}")
                    if block and 'transactions' in block:
                        for tx in block['transactions']:
                            print(f"Processing transaction {tx['hash'].hex()}")
                            store_transaction(tx)
                except Exception as e:
                    print(f"Error fetching block {block_hash.hex()}: {e}")

            # Sleep for a bit before polling for new blocks again
            time.sleep(10)
    
    except Exception as e:
        print(f"Error while monitoring blocks: {e}")

# Function to store transaction in the database
def store_transaction(tx):
    global cursor, db
    try:
        if not db.is_connected():
            db = connect_to_db()
            cursor = db.cursor()

        from_address = tx['from']
        to_address = tx['to']
        transaction_hash = tx['hash'].hex()
        block_number = tx['blockNumber']
        value = Web3.from_wei(tx['value'], 'ether')
        gas_price = Web3.from_wei(tx['gasPrice'], 'gwei')

        sql = "INSERT INTO blockchain_db.receive_blockchain_watcher (from_address, to_address, transaction_hash, block_number, value, gas_price) VALUES (%s, %s, %s, %s, %s,%s)"
        cursor.execute(sql, (from_address, to_address, transaction_hash, block_number, value, gas_price))
        db.commit()
        print(f"Stored transaction {transaction_hash}")
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        if err.errno == 2055:  # Cursor not connected
            db = connect_to_db()
            cursor = db.cursor()
    except Exception as e:
        print(f"Error storing transaction: {e}")

# Monitor new blocks and store transaction details
if __name__ == "__main__":
    monitor_blocks()
    db.close()
