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


def queryDataByid(id):
    """Query the entire data asset from the bigchaindb node

    Args:
        id (string): A transaction id 

    Returns:
        Dictionary: A dictionary of the data assert detail. 
    """
    datapoints = bdb.transactions.retrieve(id)['asset']['data']
    datapoints = str(datapoints)  # Convert dictionary to json
    datapoints = eval(datapoints)
    return datapoints


def queryByid(id):
    """Query the blockchain block data by the transaction id and retrieved the data that saved in the node.

    Args:
        id (string): A transaction id for the specific node that saved the data. 

    Returns:
        dictionary: all specific data dictionary that used to reconstruct the data. 
    """
    
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
    """Query the data by searching the metadata in the transaction

    Args:
        input (string): a string that I want to look up in the metadata section

    Returns:
        dictionary: all blocks that may have the word input in their metadata section. 
    """
    return bdb.metadata.get(search=input)


def getTxnID(domain):
    """Order the all the transaction id that belongTo this domain

    Args:
        domain (string): a file type that want to look up, such as model_A.json; want the data parameters from model_A

    Returns:
        dictionary: A dictionary that contain all the ordered transaction id for this domain. [such as transactionId.txt]
    """
    result = (queryMetaData(domain))
    fi = open('../../model_parameters/' + domain)
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
    """Filter the data by label

    Args:
        label (string): a specific label that the client requests on. 
    """
    allFile = loadJson()
    target = []
    for i in allFile:
        fi = open('../../model_parameters/' + i)
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
    """Reconstruct the all the value and save it to the json file for future prediction. 

    Args:
        domain (string): a specific file that want to retrieved the data from
    """
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



def verifyKey(key):
    """A way to verify the client. [client will get the key from smart contract code. ]

    Args:
        key (string): a key

    Returns:
        bool: true or false for the identity. 
    """
    fi = open("key.txt", "r")
    lik =fi.read()
    if key in lik:
        return True
    return False


if __name__ == "__main__":

    # Based on the client label, do the data retrieved from the blockchain 
    label = 'car'
    key = 'mqLfKUHwrmbQLfkFoeBXDwipPNkBKYbJFwXfQNAGWxegTzoEtknFYeqkPlUJtQSwfwIRByzIbcCZSZXveKgqGNHibYveYwYwyzEixYPsL'
    if verifyKey(key):
        filterByLabel(label)
        # print("good")
    else:
        print("incorrect key")
    