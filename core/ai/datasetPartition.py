# Set up
import json
import random
import numpy as np
import pandas as pd

from dataset import get_dataset
from argparse import ArgumentParser

from utils import get_random_hundreds, generate_list_by_sum
from dataset import generate_data_owner_datasets
# # Generate a random hundreds, default: between 500 ~ 3000


# def get_random_hundreds(low=500, high=3000):
#     return round(random.randint(low//100, high//100)) * 100

# # Generate data owner datasets by labels


# def generate_data_owner_datasets(labels):
#     label_count_info = {label: get_random_hundreds() for label in labels}
#     return label_count_info

# # Generate a list with the given length


# def generate_list_by_sum(m, n):
#     arr = [0] * m
#     for i in range(n):
#         arr[random.randint(0, m-1)] += 1
#     return arr


def partition(dataset_path, data_owner_label_info, result_filename):
    SEED = 20
    random.seed(SEED)
    np.random.seed(SEED)

    # Load all image paths
    data_df = pd.read_csv(dataset_path + '/data.csv')

    # Split test dataset and private (data owner) dataset
    test_dataset = data_df.groupby('label').sample(frac=.2)
    private_dataset = data_df.iloc[[
        i for i in data_df.index if i not in test_dataset.index]]

    # get label map
    id2label = data_df[['label', 'label_name']].drop_duplicates().sort_values(
        'label').set_index('label').to_dict()['label_name']
    label2id = {v: k for k, v in id2label.items()}

    data_owner_label_info = {k: (v[0], v[1].split(', '))
                             for k, v in data_owner_label_info.items()}
    data_owner_label_count_info = {k: {label: get_random_hundreds(
    ) for label in v[1]} for k, v in data_owner_label_info.items()}
    all_labels = set()
    for k, v in data_owner_label_count_info.items():
        all_labels.update(list(v.keys()))
        print(k, '\t', '\t'.join([f'{i[0]}({i[1]})' for i in v.items()]))

    all_labels.remove('other')

    # update the count for other labels
    data_owner_label_count_full_info = {}
    for k, v in data_owner_label_count_info.items():
        other_labels = all_labels.difference(set(v.keys()))
        data_owner_label_count_full_info[k] = v
        if 'other' in v:
            total_other_labels = v['other']
            del data_owner_label_count_full_info[k]['other']
            for label, count in zip(other_labels, generate_list_by_sum(len(other_labels), total_other_labels)):
                data_owner_label_count_full_info[k][label] = f'{count}*'

        # Set count of extra labels to 0
        extra_labels = all_labels.difference(
            set(data_owner_label_count_full_info[k].keys()))
        for label in extra_labels:
            data_owner_label_count_full_info[k][label] = ''
        for label in v.keys():
            data_owner_label_count_full_info[k][label] = f'{data_owner_label_count_full_info[k][label]}'

    # Convert the count information to pandas data frame
    data_owner_info_df = pd.DataFrame(data_owner_label_count_full_info).T
    data_owner_info_df

    # Get data owner dataset
    data_owner_dict = {}
    for data_owner_id in data_owner_info_df.index:
        data_owner_info = data_owner_info_df.T[data_owner_id].to_dict()
        data_owner_labels = [
            k for k, v in data_owner_info.items() if v.isnumeric()]
        data_owner_dataset = get_dataset(
            private_dataset,
            **{k: int(v.replace('*', '')) if len(v) > 0 else 0
               for k, v in data_owner_info.items()})

        other_idx = data_owner_dataset.query(
            'label_name not in @data_owner_labels').index
        data_owner_dataset.loc[other_idx, 'label'] = -1
        data_owner_dataset.loc[other_idx, 'label_name'] = 'other'
        data_owner_dict[data_owner_id] = data_owner_dataset

        # Sanity check
        # Check all labels are selected as expected
        all_labels = data_owner_dict[data_owner_id].label_name.unique()
        true_labels = data_owner_label_info[data_owner_id][1]
        assert not len(set(all_labels).difference(true_labels))

    # Save data owner datasets as excel
    with pd.ExcelWriter(f'{dataset_path}/{result_filename}') as writer:
        for data_owner_id in data_owner_dict:
            data_owner_dict[data_owner_id].to_excel(
                writer, data_owner_id, index=False)


if __name__ == '__main__':

    # Get argument variables
    parser = ArgumentParser()
    parser.add_argument('--config', type=str)
    parser.add_argument('--result_fn', type=str)
    args = parser.parse_args()

    # Load project paths
    dataset_path = './Datasets/CIFAR10'

    # Get data owner label information
    data_owner_label_info = json.load(open(args.config, 'r'))

    result_filename = args.result_fn
    partition(dataset_path, data_owner_label_info, result_filename)
