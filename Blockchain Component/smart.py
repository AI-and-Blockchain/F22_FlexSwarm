import base64
import json
import random
from algosdk import mnemonic, encoding, account
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.future.transaction import LogicSigTransaction, PaymentTxn, AssetTransferTxn, wait_for_confirmation
from algosdk import constants

def generate_algorand_keypair(user):
    private_key, address = account.generate_account()
    print(user +"'s address: {}".format(address))
    print(user +"'s private key: {}".format(private_key))
    print(user +"'s passphrase: {}".format(mnemonic.from_private_key(private_key)))
    passphrase = mnemonic.from_private_key(private_key)
    return address, private_key, passphrase



def createTxn(algoclient, owner_address, owner_private, client_address, client_private):
    # get a random key from the file
    fi = open("key.txt", "r")
    lik = []
    for i in fi:
        lik.append(i.strip("\n"))
    num = random.randint(0, len(lik))
    key = lik[num]
    # print(key)
    final_message = "Here is your access key: " + key


    # Create the transaction
    params = algoclient.suggested_params()
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE
    amount = 1000000
    c_unsigned_txn = PaymentTxn(client_address, params,  owner_address, amount)
    o_unsigned_txn = PaymentTxn(owner_address, params, client_address, 1, None, final_message)

    gid = transaction.calculate_group_id([o_unsigned_txn, c_unsigned_txn])
    c_unsigned_txn.group = gid
    o_unsigned_txn.group = gid

    stxn1 = c_unsigned_txn.sign(client_private)
    stxn2 = o_unsigned_txn.sign(owner_private)

    signed_group = [stxn2, stxn1]
    print(signed_group)

    tx_id = algoclient.send_transactions(signed_group)
    print("Here is the transaction group id: ",gid)

    wait_for_confirmation(algoclient, tx_id)
    # Print the transaction ID of the first transaction of the group
    print("Send transaction with txID: {}".format(tx_id))



# generate_algorand_keypair("A")
# generate_algorand_keypair("B")

issuers = 'X27FRTBPN2WOC4M3G3Q3TLRYNJTBQO7JALAIVF36XZ646GJD3R3PFUGWDU' # For reward 

owner_address = 'B3HOVTUXTGSPOZXUAMUDUZ3DXJYDIDSIPKQZVPGBPUKV6HMNIUYJ7SDPDQ'
owner_passphrase = 'badge chicken forest decide day misery canvas huge decorate fever food current shy camp black coyote elder another reward soap knee slush property about rug'    


client_address = 'KHCZWNHJE464SNFAS76LZYAXD4ZDIR5M5VB73YWLDQHHMZ3HQPCEAWCZMA'
client_passphrase = 'bar sheriff long setup world vacant ski essence web proof arrow grant parrot grocery visit spawn reward stool correct cake asset clap accuse absent junk'
client_privateKey = mnemonic.to_private_key(client_passphrase)


# Connect to the algod client
purestake_key = 'pHY0FnbMby3VKnaN0RkT03CIsG0vacUp33jPvvOk'
algod_address = 'https://testnet-algorand.api.purestake.io/ps2'
algod_token = "pHY0FnbMby3VKnaN0RkT03CIsG0vacUp33jPvvOk"
headers = {
    'X-Api-key': "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab",
}

algoclient = algod.AlgodClient(algod_token, algod_address, headers)



createTxn(algoclient, owner_address, mnemonic.to_private_key(owner_passphrase), client_address, client_privateKey)

