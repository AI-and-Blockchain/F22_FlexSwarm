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
    entries = os.listdir('../model_parameters/')
    final_fileList = []
    for i in entries:
        file_size = os.path.getsize('../model_parameters/' + i)
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

    sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)
    id = fulfilled_creation_tx['id']

    return id



def saveToBlockchain(issuers):
    transaction_id = {}
    file1 = open("transactionID.txt", "w")
    AllFile = loadJson()
    for i in AllFile:
        fi = open('../model_parameters/' + i)
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
    

def queryDataByid(id):
    datapoints = bdb.transactions.retrieve(id)['asset']['data']
    datapoints = str(datapoints)  # Convert dictionary to json
    datapoints = eval(datapoints)
    return datapoints


def queryByid(id):
    
    info = bdb.transactions.get(asset_id=id)
    metadata = info[0]['metadata']
    model_structure = info[0]['asset']['data']['model_structure']
    model_parameters_names = info[0]['asset']['data']['model_parameters_name']
    model_parameters_valus = info[0]['asset']['data']['model_parameters_vals']
    asset = info[0]['asset']['data']
    label = info[0]['asset']['data']['label']
    return metadata, model_structure, model_parameters_names, model_parameters_valus, label



# input is a string
def queryMetaData(input):
    return bdb.metadata.get(search=input)


def getTxnID(domain):
    result = (queryMetaData(domain))
    fi = open('../model_parameters/' + domain)
    data = json.load(fi)
    par_length = len(data['model_parameters_vals'])
    print(par_length)
    A_dic = {2: []}

    for count in range(par_length):

        for i in result:
           
            metalength = len(i['metadata'])
            if(metalength == 5 and i['metadata']['belongTo'] == domain):
               
                if count not in A_dic and count != 2:
                    if (i['metadata']['section'] == count):
                        A_dic[count] = i['id']
                        print(i)

    for k in range(len(data['model_parameters_vals'][2])):
        for i in result:
            metalength = len(i['metadata'])
            if(metalength == 5 and i['metadata']['belongTo'] == domain):
                if (i['metadata']['section'] == '2_' + str(k)):
                    A_dic[2].append(i['id'])
                    print(i)

    return A_dic




def filterByLabel(label):
    allFile = loadJson()
    target = []
    for i in allFile:
        fi = open('../model_parameters/' + i)
        data = json.load(fi)
        detail = data['label'].split("|")
        if label in detail:
            print(i, detail)
            target.append(i)
    print(target)

    # Call the blockchain to get the model parameters.
    for i in target:
        writeToFile(i)




def writeToFile(domain):
    fi = open("Final_" + domain, "w")
    final = {"model_structure": "", "model_parameters_names": "", "model_parameters_vals": [], "label": ""}
    txn_dict = getTxnID(domain)

    for i in sorted(txn_dict.keys()):
        
        if i == 2:
            final["model_parameters_vals"].append([])
            for id in txn_dict[i]:
                meta, structure, name, vals, label = queryByid(id)
                final["model_parameters_vals"][i].append(vals)
        else:
            id = txn_dict[i]
            meta, structure, name, vals, label = queryByid(id)
            final["model_structure"] = structure 
            final["model_parameters_names"] = name
            final["label"] = label
            final["model_parameters_vals"].append(vals)
            print(meta, "\n", name, "\n", vals, "\n", label)
            print()

    # Serializing json
    json_object = json.dumps(final, indent=4)
    fi.write(json_object)
    fi.close()

if __name__ == "__main__":

    issuers = os.environ.get("ISSUER_PUBLICKEY")
    issuers_private = os.environ.get("ISSUER_PRIVATEKEY")
    issuers = Account(issuers, issuers_private)
    
    # Save the model into Blockchain database
    # saveToBlockchain(issuers)


    domain = "model_A.json"
    # writeToFile(domain)
    # print(queryMetaData(domain))

    # Based on the client label, do the data retrieved from the blockchain 
    label = 'car'
    filterByLabel(label)
    