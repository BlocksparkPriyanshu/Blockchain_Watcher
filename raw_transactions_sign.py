import csv
from web3 import Web3

web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/393d646a0c44480cb66f7efda9fbcab7"))

# Step 1: Read private keys and from addresses from ethereum_address.csv
private_keys = {}
with open('ethereum_address.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        from_address = row['Address']
        private_key = row['Private_key']
        private_keys[from_address] = private_key

# Step 2: Read raw transactions from raw_transactions.csv
raw_transactions = []
with open('raw_transactions.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        raw_tx = {
            'from_address': row['from_address'],
            'nonce': int(row['nonce']),
            'to': row['to'],
            'value': int(row['value']),
            'gas': int(row['gas']),
            'gasPrice': int(row['gasPrice'])
        }
        raw_transactions.append(raw_tx)

# Step 3: Sign each raw transaction using the corresponding private key
signed_transactions = []
for tx in raw_transactions:
    from_address = tx['from_address']
    key = private_keys[from_address]
    
    # Prepare the transaction dictionary for signing
    tx_to_sign = {
        'nonce': tx['nonce'],
        'to': tx['to'],
        'value': tx['value'],
        'gas': tx['gas'],
        'gasPrice': tx['gasPrice']
    }
    
    # Sign the transaction
    signed_tx = web3.eth.account.sign_transaction(tx_to_sign, private_key=key)
    tx['signed_tx'] = signed_tx.rawTransaction.hex()
    signed_transactions.append(tx)


print("from_address, nonce, to_address, value, gas, gasPrice, signed_tx")
for tx in signed_transactions:
    print(f"{tx['from_address']}, {tx['nonce']}, {tx['to']}, {tx['value']}, {tx['gas']}, {tx['gasPrice']}, {tx['signed_tx']}")

# Step 4: Save signed transactions to a new CSV file
csv_file = 'signed_transactions.csv'
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['from_address', 'nonce', 'to', 'value', 'gas', 'gasPrice', 'signed_tx'])
    writer.writeheader()
    writer.writerows(signed_transactions)

print(f"Successfully Signed transactions saved to '{csv_file}'.")
