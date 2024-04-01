from web3 import Web3
import requests

''' Function to fetch the status of wallet addresses from networks

Supports passing a pair of addresses in the request parameters

This function sends a request to the blockchain API to retrieve the balance of the wallet addresses
- If the request is successful, the response containing the wallet status data is returned

Parameters:
- addresses (str or list): 
    The address or list of addresses for which the wallet status is to be fetched
- url_api (str):
    The URL of the endpoint in the blockchain
- scan_api_key (srt):
    The API key from scan of the blockchein network for request the API

Returns:
- data (dict): 
    A dictionary containing the wallet status data if the request is successful
'''
def fetch_wallet_status(addresses, url_api, scan_api_key):
    
    # If addresses are a list, we convert a list of addresses as comma-separated
    addresses = ','.join(str(addr) for addr in addresses) if isinstance(addresses, list) else addresses

    params = {
        "module": "account",
        "action": "balancemulti",
        "address": addresses,
        "tag": "latest",
        "apikey": scan_api_key
    }

    headers = {
        "content-type": "application/json",
        "accept": "application/json",
    }

    # Send a POST request to the specified API endpoint with the provided parameters and headers
    response = requests.post(url_api, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # Convert balances from wei to ETH
        for result in data['result']:
            result['balance'] = str(Web3.from_wei(int(result['balance']), 'ether'))
        return data
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
