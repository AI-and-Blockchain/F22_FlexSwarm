# Load necessary libraries
import torch
import numpy as np
import pandas as pd
from tqdm import tqdm
import albumentations as A

from model import get_vit_model
from predict import predict
from dataset import get_loader, get_test_dataset
from utils import seed_everything, label_enc, print_evaluation_metrics, load_data_owner_dataset, get_device

import warnings
warnings.filterwarnings('ignore')


def evaluate(dataset_path, data_owner_id, data_owner_model_name, device):
    """Evaluation data owner's model using train and test datasets

    Args:
        dataset_path (_type_): _description_
        data_owner_id (_type_): _description_
        data_owner_model_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Load image paths
    img_path = dataset_path + '/images'

    # Set a fixed random seed
    seed_everything()

    # Load data owner dataset
    data_owner_dataset = load_data_owner_dataset(dataset_path, data_owner_id)
    num_classes = data_owner_dataset.label_name.nunique()
    images, labels, label2id, id2label = label_enc(data_owner_dataset)

    # Get data owner dataset data loader
    vit_feature_extractor, vit_model = get_vit_model(device)
    eval_transform = A.Compose([A.Resize(224, 224)])
    train_data_loader = get_loader(images, labels, vit_feature_extractor, eval_transform,
                                   pre_trained_model=vit_model, device=device, shuffle=False)

    # Get data owner's model
    model = torch.load(data_owner_model_name)
    predictions = predict(train_data_loader, model, device)
    print_evaluation_metrics(labels, predictions, label2id, 'In sample')

    test_dataset = get_test_dataset(dataset_path)
    other_index = test_dataset.query(
        'label_name not in @label2id.keys()').index
    test_dataset.loc[other_index, 'label_name'] = 'other'

    # Get test dataset images and labels
    images = [f'{img_path}/{image}' for image in test_dataset.image]
    labels = test_dataset.label_name.apply(lambda x: label2id[x]).tolist()

    # Get test dataset data loader
    eval_data_loader = get_loader(images, labels, vit_feature_extractor, eval_transform,
                                  pre_trained_model=vit_model, device=device, shuffle=False)
    predictions = predict(eval_data_loader, model, device)
    evaluation_score = print_evaluation_metrics(
        labels, predictions, label2id, 'Out sample')

    return evaluation_score


if __name__ == '__main__':
    # Load project paths
    dataset_path = './Datasets/CIFAR10'

    # Get applicable training device
    device = get_device()

    # Set data owner id of interest
    data_owner_id = 'A'
    data_owner_model_name = './saved_models/model_A_1.pt'
    evaluation_score = evaluate(
        dataset_path, data_owner_id, data_owner_model_name, device)

    # Print return results
    print(f'{data_owner_id}\'s Evaluation_Score: {evaluation_score}')
