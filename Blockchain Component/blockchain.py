from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from Account import *

bdb_root = 'https://test.ipdb.io'
bdb = BigchainDB(bdb_root)


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
    '''
    '''

    if len(data) == 0:
        print("invalid length of data asset")
        return False
    # The pass in data need to be json format
        #   data = {
        #     'label_1':{
        #       'plane':[123,156,123,145]
        #     }
        #   }
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

    return id, owner_address.public_key


def queryDataByid(id):
    datapoints = bdb.transactions.retrieve(id)['asset']['data']
    datapoints = str(datapoints)  # Convert dictionary to json
    datapoints = eval(datapoints)
    return datapoints


def queryByid(id):
    return bdb.transactions.get(asset_id=id)


# input is a string
def queryMetaData(input):
    return bdb.metadata.get(search=input)


# recipients must be a list
# price must be an integer
def divisibleAsset(owner_address, recipients, create_id, retail, price):

    data = queryDataByid(create_id)
    time_sharing_token = {
        'data': {
            'token_for': data,
            'description': 'Limit time access data points for model'
        }
    }

    prepared_token_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=owner_address.public_key,
        recipients=[([recipients.public_key], retail)],
        asset=time_sharing_token
    )

    fulfilled_token_tx = bdb.transactions.fulfill(
        prepared_token_tx, private_keys=owner_address.private_key)

    try:
        sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)
        print("Transaction sent to blockchain")
    except:
        print("create transaction existed in blockchian")

    id = fulfilled_token_tx['id']
    issuer = fulfilled_token_tx['inputs'][0]['owners_before'][0]

    output = fulfilled_token_tx['outputs'][0]
    transfer_input = {
        'fulfillment': output['condition']['details'],
        'fulfills': {
            'output_index': 0,
            'transaction_id': id,
        },
        'owners_before': output['public_keys'],
    }

    transfer_asset = {
        'id': create_id
    }

    prepared_transfer_tx = bdb.transactions.prepare(
        operation='TRANSFER',
        asset=transfer_asset,
        inputs=transfer_input,
        recipients=[([owner_address.public_key], price),
                    ([recipients.public_key], 1)]
    )

    fulfilled_transfer_tx = bdb.transactions.fulfill(
        prepared_transfer_tx, private_keys=recipients.private_key)

    try:
        sent_creation_tx = bdb.transactions.send_commit(fulfilled_transfer_tx)
        print("Transaction sent to blockchain")
    except:
        print("transfer transaction existed in blockchian")

    # return id, issuer
    owner = owner_address.public_key
    buyer = recipients.public_key
    asset_id = fulfilled_transfer_tx['asset']['id']
    return owner, buyer, asset_id


if __name__ == "__main__":
    datapoint = {
        'label_1': {
            'plane': [123, 156, 123, 145, 'testing', 'ok']
        }
    }

    account1 = createAccount()
    account2 = createAccount()
    sam = Account(account1)
    alice = Account(account2)

    create_id, issuer = createAsset(sam, datapoint)

    queryDataByid(create_id)
    print(create_id)

    owner, buyer, asset_id = divisibleAsset(sam, alice, create_id, 200, 10)
    print(owner, buyer, asset_id)
