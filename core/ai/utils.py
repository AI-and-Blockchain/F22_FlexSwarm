import os
import torch
import random
import numpy as np
import pandas as pd


def seed_everything(seed=20):
    """set seed for all"""
    os.environ['PYTHONHASHSEED'] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True


def get_device(cpu=False):
    """Get applicable training device

    Args:
        cpu (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    if cpu:
        return 'cpu'
    if hasattr(torch.backends, 'mps'):
        if torch.backends.mps.is_built():
            return 'mps'
    return 'cuda:0' if torch.cuda.is_available() else 'cpu'


def label_enc(data_owner_dataset):
    """Label encoding and get images and labels as lists

    Args:
        data_owner_dataset (_type_): _description_

    Returns:
        _type_: _description_
    """
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder().fit(data_owner_dataset.label_name)
    label2id = {k: v for k, v in zip(le.classes_, le.transform(le.classes_))}
    id2label = {v: k for k, v in label2id.items()}
    labels = le.transform(data_owner_dataset.label_name)
    images = data_owner_dataset.image.tolist()
    return images, labels, label2id, id2label


def get_metrics(labels, predictions, label2id):
    """Get evaluation metrics (accuracy, f1 score, and the weighted ones)


    Args:
        labels (_type_): _description_
        predictions (_type_): _description_
        label2id (_type_): _description_

    Returns:
        _type_: _description_
    """
    from sklearn import metrics
    # Get accuracy
    accuracy_score = metrics.accuracy_score(labels, predictions)

    # Get f1 score
    f1_score = metrics.f1_score(labels, predictions, average='micro')

    # Get weighted accuracy
    sample_weight = [5 if label == label2id['other']
                     else 1 for label in labels]
    weighted_accuracy_score = metrics.accuracy_score(
        labels, predictions, sample_weight=sample_weight)

    # Get weighted f1 score
    weighted_f1_score = metrics.f1_score(
        labels, predictions, average='micro', sample_weight=sample_weight)

    return accuracy_score, f1_score, weighted_accuracy_score, weighted_f1_score


def print_evaluation_metrics(labels, predictions, label2id, title):
    """Get and print evaluation metrics

    Args:
        labels (_type_): _description_
        predictions (_type_): _description_
        label2id (_type_): _description_
        title (_type_): _description_
    """
    accuracy_score, f1_score, weighted_accuracy_score, weighted_f1_score = get_metrics(
        labels, predictions, label2id)

    print(f'{title} accuracy score: {accuracy_score:.4f}')
    print(f'{title} f1 score: {f1_score:.4f}')
    print(f'{title} weighted accuracy score: {weighted_accuracy_score:.4f}')
    print(f'{title} weighted f1 score: {weighted_f1_score:.4f}')
    return weighted_f1_score


def load_data_owner_dataset(dataset_path, data_owner_id):
    """Load data owner dataset

    Args:
        dataset_path (_type_): _description_
        data_owner_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Load image paths
    img_path = dataset_path + '/images'

    data_owner_dataset = pd.read_excel(
        dataset_path + '/CIFAR10dataOwnerInfo.xlsx', sheet_name=data_owner_id)
    data_owner_dataset.image = [
        f'{img_path}/{image}' for image in data_owner_dataset.image]
    return data_owner_dataset


def get_random_hundreds(low=500, high=3000):
    """Generate a random hundreds, default: between 500 ~ 3000

    Args:
        low (int, optional): _description_. Defaults to 500.
        high (int, optional): _description_. Defaults to 3000.

    Returns:
        _type_: _description_
    """
    return round(random.randint(low//100, high//100)) * 100

def generate_list_by_sum(m, n):
    arr = [0] * m
    for i in range(n):
        arr[random.randint(0, m-1)] += 1
    return arr
