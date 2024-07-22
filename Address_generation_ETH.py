import csv
from web3 import Web3
from mnemonic import Mnemonic
from hdwallet import HDWallet
from hdwallet.symbols import ETH
from eth_account import Account

# Number of addresses to generate
num_addresses = 5

csv_file = 'ethereum_address.csv'

web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/393d646a0c44480cb66f7efda9fbcab7"))

# Function to generate and store Ethereum addresses
def generate_and_store_addresses(num_addresses, csv_file):
    mnemo = Mnemonic("english")
    mnemonic = mnemo.generate(strength=128)
    print(f"Mnemonic: {mnemonic}")

    hdwallet = HDWallet(symbol=ETH)
    hdwallet.from_mnemonic(mnemonic=mnemonic)

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Derivation Path','Public_key', 'Private_key', 'Address'])
        if file.tell() == 0:
            writer.writeheader()
        
        for i in range(num_addresses):
            derivation_path = f"m/44'/60'/0'/0/{i+1}"
            hdwallet.from_path(derivation_path)
            
            private_key = hdwallet.private_key()
            account = Account.from_key(private_key)
            public_key = account._key_obj.public_key.to_hex()
            address = account.address

            
            # Write data to CSV file
            writer.writerow({
                'Derivation Path': derivation_path,
                'Public_key': public_key,
                'Private_key': private_key,
                'Address': address   
            })

            # Print the generated Ethereum account details (optional)
            print(f"Derivation Path: {derivation_path}")
            print(f"Public Key: {public_key}")
            print(f"Private Key: {private_key}")
            print(f"Address: {address}")
            print("---")



# Call the function to generate and store addresses
generate_and_store_addresses(num_addresses,csv_file)
def read_csv_file(csv_file):
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            print(row)

print(f"{num_addresses} Ethereum addresses generated and stored in {csv_file}.")
