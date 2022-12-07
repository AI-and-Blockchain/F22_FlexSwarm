from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from Account import *
from dotenv import load_dotenv
import os
import json


load_dotenv('.env')
bdb_root = 'https://test.ipdb.io'
bdb = BigchainDB(bdb_root)

def loadJson():
    """Load all the data model file from the model_parameters file

    Returns:
        _list_: a completed list of all the file with file size less than 1000K bytes
    """
    entries = os.listdir('../../model_parameters/')
    final_fileList = []
    for i in entries:
        file_size = os.path.getsize('../../model_parameters/' + i)
        # print(i, file_size, "bytes")
        if(file_size <= 10000000):
            final_fileList.append(i)
    return final_fileList

def createAccount():
    '''Create A random blockchain account using bigchandb_driver function

    Returns:
        _CryptoKeypair_: private key and public key 
    '''
    account = generate_keypair()
    return account


# A create operation to create a asset, and send it over to blockchain.
# owner_Address is dictionary with public_key and private_key
# Return the transaction id of the create operation
def createAsset(owner_address, data, metadata=None):
    """create the asset and sent it to blockchain node. If the transaction already exists, it will provided the corresponding transaction id for this assert

    Args:
        owner_address (classs Account): data issuers address and owner private key
        data (dictionary): the data that I want to save into the blockchain
        metadata (dictionary, optional): A small explanation included with this assert. Help to easy find the specific transaction block. Defaults to None.

    Returns:
        string: A specific transaction id for this ttransaction
    """

    model = {
        'data': data
    }


    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=owner_address.public_key,
        asset=model,
        metadata=metadata
    )

    # Fulfilled the transaction
    fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx, private_keys=owner_address.private_key)

    # Send the transaction to connected BigchainDB node.
    try:
        sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)
        print("Transaction sent to blockchain")
    except:
        print("transaction existed in blockchian")

    id = fulfilled_creation_tx['id']

    return id

def saveToBlockchain(issuers):
    """A operation to save all the files data into blockchain; and write the transaction id for each model. 

    Args:
        issuers (class Account): issuers address and issuers private key
    """
    transaction_id = {}
    file1 = open("transactionID.txt", "w")
    AllFile = loadJson()
    for i in AllFile:
        fi = open('../../model_parameters/' + i)
        data = json.load(fi)
        print(i, len(data['model_parameters_vals']))

        for j in range(len(data['model_parameters_vals'])):
            temp = {
                "model_structure": data['model_structure'],
                "model_parameters_name": data['model_parameters_names'],
                "model_parameters_vals": data['model_parameters_vals'][j],
                "label": data['label']
            }
            metadata = {
                'label': data['label'],
                'belongTo': i,
                'section': j,
                'new_update': 'yes',
                'final_update': 'yes'
                
            }
            
            txn_id = createAsset(issuers, temp, metadata)
            if i.rstrip('.json') not in transaction_id:
                transaction_id[i.rstrip('.json')] = []
            else:
                transaction_id[i.rstrip('.json')].append(txn_id)
            if j == 2:
                for k in range(len(data['model_parameters_vals'][2])):
                    tem = {
                        "model_structure": data['model_structure'],
                        "model_parameters_name": data['model_parameters_names'],
                        "model_parameters_vals": data['model_parameters_vals'][2][k],
                        "label": data['label']
                    }
                    metadat = {
                        'label': data['label'],
                        'belongTo': i,
                        'section': '2_' + str(k),
                        'new_update': 'yes',
                        'final_update': 'yes'
                    }
                    txn_id = createAsset(issuers, tem, metadat)
                    if i.rstrip('.json') not in transaction_id:
                        transaction_id[i.rstrip('.json')] = []
                    else:
                        transaction_id[i.rstrip('.json')].append("\t\t" + txn_id)

    for key in transaction_id:
        file1.write(key + ":\n")
        for value in transaction_id[key]:
            file1.write(value + "\n")
        file1.write("\n\n")
    file1.close()


if __name__ == "__main__":

    issuers = os.environ.get("ISSUER_PUBLICKEY")
    issuers_private = os.environ.get("ISSUER_PRIVATEKEY")
    issuers = Account(issuers, issuers_private)
    saveToBlockchain(issuers)