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
