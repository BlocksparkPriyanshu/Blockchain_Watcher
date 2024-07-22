import csv
from web3 import Web3

web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/393d646a0c44480cb66f7efda9fbcab7"))

address=[]
with open('ethereum_address.csv','r') as file:
    reader = csv.DictReader(file)
    for row in reader :
        address.append({'from': row['Address']})

to_address = input("Enter the recipient address (to): ")

transactions =[]

for address in address:
    from_address = address['from']

    tx = {
        'from_address': from_address,
        'nonce': web3.eth.get_transaction_count(from_address),
        'to': to_address,
        'value': web3.to_wei(0.1, 'ether'),
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei')
    }
    transactions.append(tx)
    print(transactions)

raw_transactions=[]

for tx in transactions:
    raw_tx = {
        'from_address':  tx['from_address'],
        'nonce': tx['nonce'],
        'to' : tx['to'],
        'value': tx['value'],
        'gas' : tx['gas'],
        'gasPrice' : tx['gasPrice']
    }
    raw_transactions.append(raw_tx)

print("from_address : nonce, to_address, value, gas, gasPrice")
for tx in raw_transactions:
     print(f"{tx['from_address']} : {tx['nonce']}, {tx['to']}, {tx['value']}, {tx['gas']}, {tx['gasPrice']}")

csv_file = 'raw_transactions.csv'

with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['from_address','nonce','to', 'value', 'gas', 'gasPrice'])
    writer.writeheader()
    writer.writerows(raw_transactions)

print(f"Successfully Raw transactions saved to '{csv_file}'.")