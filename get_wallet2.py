#!/usr/bin/env python3
import os
import cgi
import json
import requests

from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Function to fetch wallet status from the Ethereum/Polygon API
def fetch_wallet_status(wallet_address, api_url, api_key):
    params = {
        "module": "account",
        "action": "balance",
        "address": wallet_address,
        "tag": "latest",
        "apikey": api_key
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return "active" if data.get("status") == "1" else "inactive"
    else:
        return None

# Function to get balance using the Ethereum/Polygon API
def get_balance(token_address, wallet_address, api_url, api_key):
    params = {
        "module": "account",
        "action": "tokenbalance",
        "contractaddress": token_address,
        "address": wallet_address,
        "tag": "latest",
        "apikey": api_key
    }
    response = requests.get(api_url, params=params)
    return response.json()["result"] if response.ok else "Error"

# Set API URLs
api_urls = {
    "ethereum_url": "https://api.etherscan.io/api",
    "polygon_url": "https://api.polygonscan.com/api"
}

# Read input from CGI form
form = cgi.FieldStorage()
wallet = form.getvalue('wallet') or "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"
block = form.getvalue('block') or "ETHEREUM"
token = form.getvalue('token') or "0xB8c77482e45F1F44dE1745F52C74426C631bDD52"

# Determine the appropriate API URL
api_url = api_urls.get(f"{block.lower()}_url")
if not api_url:
    print("Content-Type: application/json\n")
    print(json.dumps({"error": "Invalid block specified"}))
    exit()

# Get API key from environment
api_key = os.getenv(f"{block}_API_KEY")
if not api_key:
    print("Content-Type: application/json\n")
    print(json.dumps({"error": f"No API key provided for {block}"}))
    exit()

# Fetch wallet status and balance data
status_data = fetch_wallet_status(wallet, api_url, api_key)
balance_data = get_balance(token, wallet, api_url, api_key)

# Prepare and print JSON response
json_data = {f"{block}": {"status": status_data, "balance": balance_data}}
print("Content-Type: application/json\n")
print(json.dumps(json_data))
