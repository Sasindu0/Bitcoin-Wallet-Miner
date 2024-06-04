import ecdsa
import hashlib
import base58check
import requests
import json
from threading import Thread

def doubleHash(key):
    return hashlib.sha256(hashlib.sha256(key).digest()).digest()

def generatePrivateKey():
    private_key_bytes = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1).to_string()
    private_key_wif = b'\x80' + private_key_bytes + b'\x01'
    private_checksum = doubleHash(private_key_wif)[:4]
    private_key_wif = private_key_wif + private_checksum
    private_key_wif = base58check.b58encode(private_key_wif).decode('ascii')

    return private_key_bytes, private_key_wif

    #Prefix:            Compression:
    #MainNet = x80      True = x01
    #TestNet = xef      False = x00 (no bytes)

    #Generated key should be started with:
    #WIF Uncompressed = 5
    #Compressed = K / L

def generatePublicKey(private_key_bytes):
    signing_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    public_key_bytes = signing_key.get_verifying_key().to_string()

    uncompressedPublicKey = b'\x04' + public_key_bytes

    xPoint = public_key_bytes[0:32]
    yPoint = public_key_bytes[32:]

    if int(yPoint.hex(), 16) % 2 == 0:
       compressedPublicKey = b'\x02' + xPoint
    else:
       compressedPublicKey = b'\x03' + xPoint

    return compressedPublicKey
    
    #x, y coordinates of generator point
    #Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    #Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

    #Public key Prefix:
    #Uncompressed = x04
    #if y is even = x02
    #if y is odd = x03

def generateWalletAddress(public_key_bytes):
    s256 = hashlib.sha256(public_key_bytes).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(s256)

    payload = b'\x00' + ripemd160.digest()
    public_checksum = doubleHash(payload)[:4]
    payload = payload + public_checksum
    wallet_address = base58check.b58encode(payload).decode('ascii')

    return wallet_address

    #Prefix:
    #MainNet = x00
    #TestNet = x6f
    #Generated key should be started with = 1

def checkWalletAddress(bitcoinAddress):

    url = f"https://blockchain.info/balance?active={bitcoinAddress}"
    response = requests.get(url)
    data = json.loads(response.text)

    return data[f'{bitcoinAddress}']['final_balance']

def threadLoop():
    while True:
        try:
            PrivateKeyBytes, PrivateKey = generatePrivateKey()
            PublicKey = generatePublicKey(PrivateKeyBytes)
            WalletAddress = generateWalletAddress(PublicKey)
            BTC = int(checkWalletAddress(WalletAddress)) / 10**8

            print("PKey:",PrivateKey, "| BTCAdd:", WalletAddress, "| BTC:",BTC)
            if BTC > 0:   
                with open("BTC_Data.txt", "a") as file:
                    file.write(f"PKey: {PrivateKey} | PubKey: {PublicKey.hex()} | BTCAdd: {WalletAddress} | BTC: {BTC}\n")

        except Exception as e:
            print(e)


if __name__ == "__main__":

    """ for i in range(2):

        thread = Thread(target=threadLoop, daemon=True)
        thread.start() """


    while True:
        try:
            PrivateKeyBytes, PrivateKey = generatePrivateKey()
            PublicKey = generatePublicKey(PrivateKeyBytes)
            WalletAddress = generateWalletAddress(PublicKey)
            BTC = int(checkWalletAddress(WalletAddress)) / 10**8

            print("PKey:",PrivateKey, "| BTCAdd:", WalletAddress, "| BTC:",BTC)
            if BTC > 0:   
                with open("BTC_Data.txt", "a") as file:
                    file.write(f"PKey: {PrivateKey} | PubKey: {PublicKey.hex()} | BTCAdd: {WalletAddress} | BTC: {BTC}\n")

        except Exception as e:
            print(e)
            
