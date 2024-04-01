# Code Documentation
### Activating and Deactivating the Virtual Environment
##### For Console:
- _Hint: main project directory_

__Activate the Virtual Environment:__
`source venv/bin/activate`
__Deactivate the Virtual Environment:__
`deactivate`

##### For Git Bash:
- _Hint: main project directory_

__Activate the Virtual Environment:__
`source venv/Scripts/activate`
__Deactivate the Virtual Environment:__
`deactivate`

### Requirements
- _Hint: main project directory_

##### For install all dependencies:
```
pip install -r requirements.txt
```
The team will install all the necessary __dependencies__ to run the __project__

### Project structure
```
PyScriptRequests/
│
├── data/
│   └── (JSON files: ABI, input data, output data)
│
├── src/
│   ├── api/
│   │   ├── fetch_wallet_status.py
│   │   └── get_balance.py
│   └── main.py
│
├── venv/
│   └── (virtual environment files)
│
├── .env
├── .Scriptsactivate
├── README.md
└── requirements.txt
```
`data/:` Folder containing JSON files, such as ABI, input data, and output data.
`src/:` Main source code directory.
`src/api/:` Folder containing modules for making API requests.
`src/api/fetch_wallet_status.py:` Module for fetching wallet status from networks.
`src/api/get_balance.py:` Module for retrieving token balances.
`src/main.py:` Main program file.
`venv/:` Folder containing Python virtual environment files.
`.env:` Environment variable file.
`.Scriptsactivate:` Activation script for virtual environment.
`README.md:` Markdown file containing project documentation.
`requirements.txt:` File containing a list of all project dependencies.

### Description of the input_data.json File
The `input_data.json` file contains information about __wallet addresses__ and __token contracts__ for __various__ blockchain __networks__. It is used to pass data to the script for fetching __balances__.

#### Sample content of input_data.json:

```JSON
{
    "wallet_addresses": [
    {   
        "network": "ETHEREUM",
        "address": ["0x0d...1270", "0x4c...9FF4"],
        "url_api": "https://api.etherscan.io/api"
    },
    {
        "network": "POLYGON",
        "address": ["0x0d...1270", "0x4c...9FF4"],
        "url_api": "https://api.polygonscan.com/api"
    }
],
    "token_addresses": [
        {
            "network": "ETHEREUM",
            "address_contract": "0xB8...DD52",
            "address_wallet": "0x48...7e5F"
        },
        {   
            "network": "POLYGON",
            "address_contract": "0x3B...42c3",
            "address_wallet": "0xf7...d7fC"
        }
]
}
```
### Adding New Networks to wallet_addresses
To add a __new network__ to `wallet_addresses`, add a new item to the `wallet_addresses` array with information about the __network__, __wallet addresses__, and __API URL__ of that network.

#### Adding New Networks and Contracts to token_addresses
Similarly, to add a __new network__ and/or __contract__ to `token_addresses`, add a new item to the `token_addresses` array with information about the __network__, __contract address__, and __wallet address__.

#### Function Descriptions
`save_to_json(data, file_path)`
Saves _data_ in JSON format to the specified _file_.

`get_native_token_balance(wallet_addresses)`
Fetches balances of __native__ tokens for the specified wallet __addresses__ on various blockchain __networks__.

`get_token_balance(token_addresses)`
Fetches balances of __ERC20__ tokens for the specified wallet __addresses__ and contracts on various blockchain __networks__.
# BLOCKCHAIN
# BLOCKCHAIN
