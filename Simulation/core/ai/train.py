# Load necessary libraries
import numpy as np
import pandas as pd
from tqdm import tqdm
import albumentations as A
from argparse import ArgumentParser

import torch
import torch.nn as nn

from dataset import get_loader
from model import get_vit_model
from utils import seed_everything, label_enc, load_data_owner_dataset, get_device

import warnings
warnings.filterwarnings('ignore')



def train(dataset_path, data_owner_id, modules, save_model_path, num_epochs, learning_rate, device):
    """Train a data owner's model

    Args:
        dataset_path (_type_): _description_
        data_owner_id (_type_): _description_
        modules (_type_): _description_
        save_model_path (_type_): _description_
        num_epochs (_type_): _description_
        learning_rate (_type_): _description_
        device (_type_): _description_
    """
    # Load image paths
    img_path = dataset_path + '/images'
    
    # Set a fixed random seed
    seed_everything()

    # Load data owner dataset
    data_owner_dataset = load_data_owner_dataset(dataset_path, data_owner_id)
    num_classes = data_owner_dataset.label_name.nunique()
    images, labels, label2id, id2label = label_enc(data_owner_dataset)

    # Create data owner's model
    modules += [nn.LazyLinear(num_classes)]
    model = nn.Sequential(*modules)
    model.to(device)

    # Initialize loss function (criterion) and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Get data owner dataset data loader
    vit_feature_extractor, vit_model = get_vit_model(device)
    train_transform = A.Compose([
        A.Resize(256, 256),
        A.RandomCrop(224, 224),
        A.Flip(p=0.5),
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5)
    ])
    train_data_loader = get_loader(images, labels, vit_feature_extractor, train_transform,
                            pre_trained_model=vit_model, device=device)

    # Test sample input for the model, also for model warm up
    sample_batch = next(iter(train_data_loader))
    sample_images, sample_labels = sample_batch
    logits = model(sample_images.to(device))
    print(model)
    print('Batch image shape:', list(sample_images.shape))
    print('Batch label shape:', list(sample_labels.shape))
    print('Model output shape:', list(logits.shape))


    model.train()
    for epoch in range(num_epochs):
        epoch_loss_list = []
        epoch_acc_sum = [0, 0]
        for batch_images, batch_labels in tqdm(train_data_loader):
            logits = model(batch_images.to(device))
            batch_labels = batch_labels.long().to(device)
            optimizer.zero_grad()
            loss = criterion(logits, batch_labels)
            loss.backward()
            optimizer.step()

            epoch_loss_list.append(loss.item())
            epoch_acc_sum[0] += (logits.argmax(1) == batch_labels).sum().item()
            epoch_acc_sum[1] += len(batch_labels)

        print(f'[ {epoch+1:2d}:{num_epochs} ]\tloss={np.mean(epoch_loss_list):.3f}, \
            acc={epoch_acc_sum[0]}/{epoch_acc_sum[1]}={epoch_acc_sum[0]/epoch_acc_sum[1]:.3f}')

    # Save models
    torch.save(model, save_model_path)

if __name__ == '__main__':
    
    # Get argument variables
    parser = ArgumentParser()
    parser.add_argument('--id', type=str)
    parser.add_argument('--modules', type=str) # Example: LazyBatchNorm1d() | LazyLinear(128) | GELU()
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--lr', type=float, default=0.001)
    parser.add_argument('--cpu', default=False, action='store_true')
    
    args = parser.parse_args()
    
    # Get data owner id of interest
    data_owner_id = args.id
    
    # Get model structure layer lists
    modules = args.modules.replace(' ', '').split('|')
    
    # Get training epochs
    num_epochs = args.epochs

    # Get training hyperparameters -- learning rate
    learning_rate = args.lr
    
    # Load project paths
    dataset_path = './Datasets/CIFAR10'
    
    # Get applicable training device
    device = get_device(cpu=args.cpu)

    # Set the path to save the model
    save_model_path = f'./saved_models/model_{data_owner_id}.pt'

    # Set the model without the output layer
    modules = [eval(f'nn.{layer}') for layer in modules]
    
    print(f'Training data owner {data_owner_id}\'s dataset on {device} ...')    
    train(dataset_path, data_owner_id, modules, save_model_path, num_epochs, learning_rate, device)
    
    print('\n\n\n')
    
    