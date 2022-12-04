import os
import torch
import random
import numpy as np


def seed_everything(seed=20):
    """set seed for all"""
    os.environ['PYTHONHASHSEED'] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    
# Label encoding and get images and labels as lists
def label_enc(data_owner_dataset):
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder().fit(data_owner_dataset.label_name)
    label2id = {k:v for k, v in zip(le.classes_, le.transform(le.classes_))}
    id2label = {v:k for k, v in label2id.items()}
    labels = le.transform(data_owner_dataset.label_name)
    images = data_owner_dataset.image.tolist()
    return images, labels, label2id, id2label

# Get evaluation metrics (accuracy, f1 score, and the weighted ones)
def get_metrics(labels, predictions, label2id):
    from sklearn import metrics
    # Get accuracy
    accuracy_score = metrics.accuracy_score(labels, predictions)

    # Get f1 score
    f1_score = metrics.f1_score(labels, predictions, average='micro')

    # Get weighted accuracy
    sample_weight = [5 if label==label2id['other'] else 1 for label in labels]
    weighted_accuracy_score = metrics.accuracy_score(labels, predictions, sample_weight=sample_weight)

    # Get weighted f1 score
    weighted_f1_score = metrics.f1_score(labels, predictions, average='micro', sample_weight=sample_weight)
    
    return accuracy_score, f1_score, weighted_accuracy_score, weighted_f1_score

