# Bitcoin-Wallet-Miner
Bitcoin-Wallet-Miner can check all available bitcoin wallets and generate necessary keys to access it.

## Disclaimer: 
This code is provided for educational purposes only. Distributing or using this code for malicious purposes is strictly prohibited. The developer assumes no responsibility for any misuse of this code.

By using this code, you acknowledge and agree to the following:
* You are responsible for understanding the potential impact of this code.
* You will use this code in a legal and ethical manner.

## How to work a Wallet Miner?
1. Wallet Miner randomly generates a private_key using "ecdsa" library.
2. Convert private_key to Wallet Import Format(WIF) using generated private_key.
3. Encode the private_key_wif using "base58check" library.
4. Generate public_key using generated private_key.
5. Get compressed_public_key using generated public_key.
6. Check wallet data using compressed_public_key and "blockchain" API.

## Drawbacks!
1. There is a daily request limitation in blockchain API.
2. Wallet-Miner needs to check all generated public keys through internet. therefore it takes considerable time to check per key.

## Requirements
1. Install following libraries
    * Python 3.10.4
    * requests
    * ecdsa
    * base58check
    * json
    * hashlib
