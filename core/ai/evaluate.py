# Load necessary libraries
import json
import torch
import numpy as np
import pandas as pd
from tqdm import tqdm
import albumentations as A
from argparse import ArgumentParser
from sklearn.metrics import classification_report
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
    images, train_labels, label2id, id2label = label_enc(data_owner_dataset)

    # Get data owner dataset data loader
    vit_feature_extractor, vit_model = get_vit_model(device)
    eval_transform = A.Compose([A.Resize(224, 224)])
    train_data_loader = get_loader(images, train_labels, vit_feature_extractor, eval_transform,
                                   pre_trained_model=vit_model, device=device, shuffle=False)

    # Get data owner's model
    model = torch.load(data_owner_model_name)
    train_predictions = predict(train_data_loader, model, device)
    # print_evaluation_metrics(labels, predictions, label2id, 'In sample')

    # Accuracy of pred_train_label and true_train label
    # diff = numpy.array(train_predictions) == numpy.array(train_labels)
    # acc = diff / diff.shape[0]

    test_dataset = get_test_dataset(dataset_path)
    other_index = test_dataset.query(
        'label_name not in @label2id.keys()').index
    test_dataset.loc[other_index, 'label_name'] = 'other'

    # Get test dataset images and labels
    images = [f'{img_path}/{image}' for image in test_dataset.image]
    test_labels = test_dataset.label_name.apply(lambda x: label2id[x]).tolist()

    # Get test dataset data loader
    eval_data_loader = get_loader(images, test_labels, vit_feature_extractor, eval_transform,
                                  pre_trained_model=vit_model, device=device, shuffle=False)
    eval_predictions = predict(eval_data_loader, model, device)
    evaluation_score = print_evaluation_metrics(test_labels, eval_predictions, label2id, 'Out sample')

    # Accuracy of true_test_label and pred_test_label
    diff = np.array(eval_predictions) == np.array(test_labels)
    acc = np.count_nonzero(diff) / diff.shape[0]

    sample_weight = [5 if label == label2id['other']
                     else 1 for label in test_labels]

    report = classification_report(
        y_true=test_labels, 
        y_pred=eval_predictions, 
        sample_weight=sample_weight,
        output_dict=True
    )

    model_evaluation_json = json.load(open('./modelEvaluation.json', 'r'))
    model_evaluation_json[data_owner_id] = {
        'label': '|'.join([label
                           for label in data_owner_dataset.label_name.unique()
                           if label != 'other']),
        'score': evaluation_score
    }
    json.dump(model_evaluation_json, open(
        './modelEvaluation.json', 'w'), indent=4)

    return evaluation_score


if __name__ == '__main__':

    # Get argument variables
    parser = ArgumentParser()
    parser.add_argument('--id', type=str)
    parser.add_argument('--model', type=str)

    args = parser.parse_args()

    # Load project paths
    dataset_path = './Datasets/CIFAR10'

    # Get applicable training device
    device = get_device()

    # Get data owner id of interest
    data_owner_id = args.id

    # Get data owner's model
    data_owner_model_name = f'./saved_models/{args.model}.pt'

    evaluation_score = evaluate(
        dataset_path, data_owner_id, data_owner_model_name, device)

    # Print return results
    print(f'{data_owner_id}\'s Evaluation_Score: {evaluation_score}')
