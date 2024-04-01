from dotenv import load_dotenv
from web3 import Web3
import json
import os

from api.fetch_wallet_status import fetch_wallet_status
from api.get_balance import get_balance

load_dotenv()

erc20_abi_path = "../data/erc20_abi.json"
input_data_path = "../data/input_data.json"

with open(input_data_path, 'r') as json_file:
    data = json.load(json_file)

    # Checking for keys in the downloaded data
    if 'wallet_addresses' not in data or 'token_addresses' not in data:
        print("Error: Missing keys in input data.")

    wallet_addresses = data['wallet_addresses']
    token_addresses = data['token_addresses']

""" Save data to a JSON file

Args:
    data (dict): Data to be saved
    file_path (str): Path to the output JSON file
"""
def save_to_json(data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

""" Fetch and save native token balances

Args:
    wallet_addresses (list): List of dictionaries containing:
    - network information
    - wallet addresses
    - url information
"""       
def get_native_token_balance(wallet_addresses):
    balances = {}
    for wallet in wallet_addresses:
        network = wallet["network"]
        address = wallet["address"]
        url = wallet["url_api"]

        # Get balance all addresses
        result = fetch_wallet_status(address, url, os.getenv(f"{network}_API_KEY"))
        # Add all results into dict
        balances[f"{network}"] = result
    
    if balances:
        # Save result into JSON file
        save_to_json(balances, '../data/native_token_balances.json')
        print("Done..[1]")

""" Fetch and save ERC20 token balances

Args:
    token_addresses (list): List of dictionaries containing: 
    - token contract addresses
    - wallet addresses
    - network information
"""
def get_token_balance(token_addresses):
    balances = {}
    for token in token_addresses:
        network = token["network"]
        address_contract = token["address_contract"]
        address_wallet = token["address_wallet"]

        # Get balance for address
        result = get_balance(address_contract, erc20_abi_path, address_wallet, os.getenv(f"{network}_PROVIDER"))
        # Add all results into dict
        balances[f"{network}"] = result
    
    if balances:
        # Save result into JSON file
        save_to_json(balances, '../data/token_balances.json')
        print("Done..[2]")

""" Function for start the script """
def main():
    get_native_token_balance(wallet_addresses)
    get_token_balance(token_addresses)

if __name__ == "__main__":
    main()