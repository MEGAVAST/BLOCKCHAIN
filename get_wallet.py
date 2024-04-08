#!/usr/bin/env python3
import cgi
import json

### run on https://bcnt.io/cgi-bin/CRYPTO/get_wallet.py ?wallet=0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270&token=xxxxxxx&block=POLYGON

# Get the parameters from the URL
form = cgi.FieldStorage()
wallet = form.getvalue('wallet')
block = form.getvalue('block')
token = form.getvalue('token')

# Default wallet address
default_wallet = "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"
default_token = "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"
default_block = "ETHEREUM"

# Use default address if wallet is not provided or empty
if not wallet:
    wallet = default_wallet

# Prepare JSON data with the provided wallet ID or default address
json_data = {
    "ETHEREUM": {
        "status": "1",
        "message": "OK",
        "result": [
            {
                "account": f"{wallet}",
                "balance": "1.691919857047735649"
            },
            {
                "account": f"{wallet}",
                "balance": "0.4540882879396993"
            }
        ]
    },
    "POLYGON": {
        "status": "1",
        "message": "OK",
        "result": [
            {
                "account": f"{wallet}",
                "balance": "167747064.781939283045063165"
            },
            {
                "account": f"{wallet}",
                "balance": "29470694.606007361604604922"
            }
        ]
    }
}

# Print the JSON data
print("Content-Type: application/json\n")  # Required header for Apache to understand this is JSON content
print(json.dumps(json_data))
