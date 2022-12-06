import json
from argparse import ArgumentParser

from model import get_model_parameters
from utils import load_data_owner_dataset

def extract_model(dataset_path, data_owner_id, data_owner_model_path, json_path):
    
    data_owner_dataset = load_data_owner_dataset(dataset_path, data_owner_id)
    
    parameters = get_model_parameters(data_owner_model_path)
    parameters['label'] = data_owner_dataset.label_name.unique().tolist()
    parameters['label'] = '|'.join([label for label in parameters['label'] 
                                    if label != 'other'])
    json.dump(parameters, open(json_path, 'w'), indent=4)
    
    
if __name__ == '__main__':
    
    # Get argument variables
    parser = ArgumentParser()
    parser.add_argument('--id', type=str)
    
    args = parser.parse_args()
   
    # Load project paths
    dataset_path = './Datasets/CIFAR10' 
    
    # Get data owner id of interest
    data_owner_id = args.id
    
    data_owner_model_path = f'./saved_models/model_{data_owner_id}.pt'
    json_path = f'./model_parameters/model_{data_owner_id}.json'
    
    print(f'Extracting data owner {data_owner_id}\'s model to {json_path} ...' )
    extract_model(dataset_path, data_owner_id, data_owner_model_path, json_path)
    