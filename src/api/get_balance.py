from web3 import Web3
import json

"""
This function loads the ABI data from a JSON file specified by the file_path parameter

Parameters:
- file_path (str): The path to the JSON file containing ABI data

Returns:
- dict: The ABI data loaded from the file as a dictionary
"""
def load_abi_from_file(file_path):
    try:
        with open(file_path, "r") as abi_file:
            abi_data = json.load(abi_file)
            return abi_data
    except FileNotFoundError:
        print("ABI file not found.")
        return None

"""
This function retrieves the balance of a wallet address for a specific token contract

Parameters:
- address_contract (str):
    The address of the token contract
- erc20_abi_path (str):
    The path to the JSON file containing the ABI data of the ERC20 token contract
- address_wallet (str):
    The wallet address for which the balance is to be retrieved
- provider_key (str):
    The provider key for connecting to the blockchain network

Returns:
- dict: A dictionary containing the wallet address, token symbol, and balance

"""
def get_balance(address_contract, erc20_abi_path, address_wallet, provider_key):
    # Connect  to the provider
    w3 = Web3(Web3.HTTPProvider(provider_key))
    # Get ABI of the ERC20
    token_abi = load_abi_from_file(erc20_abi_path)

    # Create an instance of the contract using the contract address and ABI
    contract = w3.eth.contract(address=address_contract, abi=token_abi)
    # Get the balance of the user
    balance_wei = contract.functions.balanceOf(address_wallet).call()
    # Get symbol of the token
    symbol = contract.functions.symbol().call()

    # Convert balance from Wei to Ether
    balance = str(w3.from_wei(balance_wei, 'ether'))

    return {
        "address": address_wallet,
        "symbol": symbol,
        "balance": balance
    }
