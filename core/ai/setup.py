# Load necessary libraries
import pandas as pd
from argparse import ArgumentParser

from dataset import load_cifar10

if __name__ == '__main__':

    # Get argument variables
    parser = ArgumentParser()
    parser.add_argument('--download', default=False, action='store_true')
    
    args = parser.parse_args()
    
    
    if args.download:
        print('Start loading all images and labels')
        cache_path ='./Datasets/cache'
        dataset_path = './Datasets/CIFAR10'
        load_cifar10(dataset_path, cache_path)
        data_df = pd.read_csv(f'{dataset_path}/data.csv')
        print(data_df.head())