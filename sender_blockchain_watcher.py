import mysql.connector
from web3 import Web3

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/393d646a0c44480cb66f7efda9fbcab7"))

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

def store_transaction_request(to_address, amount):
    try:

        query = "INSERT INTO blockchain_db.transaction_requests (to_address, amount, status) VALUES (%s, %s, 'pending')"
        values = (to_address, amount)
    
        cursor.execute(query, values)
        db.commit()
        print(f"Stored transaction request: {values}")
    except Exception as e:
        print(f"Error storing transaction request: {e}")


    
def send_pending_transactions():

    try:

        query = "SELECT id, to_address, amount FROM blockchain_db.transaction_requests WHERE status = 'pending'"
        cursor.execute(query)
        pending_transactions = cursor.fetchall()
        print(f"Pending transactions: {pending_transactions}")

        for txn in pending_transactions:
            txn_id, to_address, amount = txn

        # Replace with your from address and private key
            from_address = "0x82ab18C91AFe54Cf385235300B18379E14973459"
            private_key = "bcc887e9b43a7676a851b84b6b5f366109caa8085266b150319d479cb3627e6e"

        # Generate raw transaction
            nonce = web3.eth.get_transaction_count(from_address)
            gas_price = web3.eth.gas_price

            raw_transaction = {
                'nonce': nonce,
                'to': to_address,
                'value': web3.to_wei(amount, 'ether'),
                'gas': 2000000,
                'gasPrice': gas_price
         }
            print(f"Raw transaction: {raw_transaction}")

            signed_tx = web3.eth.account.sign_transaction(raw_transaction, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

            print(f"Transaction sent with hash: {tx_hash.hex()}")

            # Update transaction status
            update_query = "UPDATE blockchain_db.transaction_requests SET status = 'completed' WHERE id = %s"
            cursor.execute(update_query, (txn_id,))

            # Store completed transaction details
            store_query = """INSERT INTO blockchain_db.transactions(from_address, to_address, amount, gas_price, tx_hash, status)
            VALUES (%s, %s, %s, %s, %s, 'completed')"""
            cursor.execute(store_query, (from_address, to_address, amount, str(gas_price), tx_hash.hex()))
            db.commit()
    except Exception as e:
            print(f"Error sending pending transactions: {e}")
    


if __name__ == "__main__":
    store_transaction_request("0x41fdAEcA963f85ccdE141e6242bD721a19A612C2", 0.01)
    # store_request_transaction("0x68d30f47F19c07bCCEf4Ac7FAE2Dc12FCa3e0dC9", 0.02)
    send_pending_transactions()
    db.close()
