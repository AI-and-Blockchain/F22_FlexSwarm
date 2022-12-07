import base64
import json
from algosdk import mnemonic, encoding, account
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.future.transaction import LogicSigTransaction, PaymentTxn, AssetTransferTxn, wait_for_confirmation

def generate_algorand_keypair(user):
    private_key, address = account.generate_account()
    print(user +"'s address: {}".format(address))
    print(user +"'s private key: {}".format(private_key))
    print(user +"'s passphrase: {}".format(mnemonic.from_private_key(private_key)))
    passphrase = mnemonic.from_private_key(private_key)
    return address, private_key, passphrase

def checkBalance(algoclient, address):
    account_info = algoclient.account_info(address)
    return account_info.get('amount')

# generate_algorand_keypair("A")
# generate_algorand_keypair("B")
issuers = 'X27FRTBPN2WOC4M3G3Q3TLRYNJTBQO7JALAIVF36XZ646GJD3R3PFUGWDU'
A_address = 'B3HOVTUXTGSPOZXUAMUDUZ3DXJYDIDSIPKQZVPGBPUKV6HMNIUYJ7SDPDQ'
A_passphrase = 'badge chicken forest decide day misery canvas huge decorate fever food current shy camp black coyote elder another reward soap knee slush property about rug'    
B_address = 'KHCZWNHJE464SNFAS76LZYAXD4ZDIR5M5VB73YWLDQHHMZ3HQPCEAWCZMA'
B_passphrase = 'bar sheriff long setup world vacant ski essence web proof arrow grant parrot grocery visit spawn reward stool correct cake asset clap accuse absent junk'



# Connect to the algod client
purestake_key = 'pHY0FnbMby3VKnaN0RkT03CIsG0vacUp33jPvvOk'
algod_address = 'https://testnet-algorand.api.purestake.io/ps2'
algod_token = "pHY0FnbMby3VKnaN0RkT03CIsG0vacUp33jPvvOk"
headers = {
    'X-Api-key': "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab",
}

algoclient = algod.AlgodClient(algod_token, algod_address, headers)
price = checkBalance(algoclient, issuers)
print(price)
