import os
import torch
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Image loading and processing
from PIL import Image
import albumentations as A
import torchvision
import torchvision.transforms as transforms

# Progress bar
from tqdm.autonotebook import tqdm

from utils import get_random_hundreds


def load_cifar10(dataset_path='../Datasets/CIFAR10', cache_path='../cache'):
    """_summary_

    Args:
        dataset_path (str, optional): _description_. Defaults to '../Datasets/CIFAR10'.
        cache_path (str, optional): _description_. Defaults to '../cache'.
    """
    img_path = f'{dataset_path}/images'

    # Make directories if they don't exist
    os.makedirs(dataset_path, exist_ok=True)
    os.makedirs(img_path, exist_ok=True)

    # Load images and normalize
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize(224),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    batch_size = 32
    train_set = torchvision.datasets.CIFAR10(
        root=cache_path, train=True, download=True, transform=transform)
    test_set = torchvision.datasets.CIFAR10(
        root=cache_path, train=False, download=True, transform=transform)
    train_loader = torch.utils.data.DataLoader(
        train_set, batch_size=batch_size, shuffle=True)

    # Set CIFAR-10 class labels
    classes = ('plane', 'car', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck')
    label_map = {k: v for k, v in enumerate(classes)}

    # Get all images that have been downloaded
    images = os.listdir(img_path)
    images_ids = [int(i.split('.')[0]) for i in images]

    # Save the image arrays to images (.png)
    labels = []

    for i, (image, label) in tqdm(enumerate(train_set), total=len(train_set)):
        labels.append(label)
        if i+1 in images_ids:
            continue
        image = image / 2 + 0.5
        image = image.numpy().transpose(1, 2, 0)
        plt.imsave(f'{img_path}/{i+1:05d}.png', image)

    # Repeat the process for the test set
    for i, (image, label) in tqdm(enumerate(test_set), total=len(test_set)):
        labels.append(label)
        if i+1+len(train_set) in images_ids:
            continue
        image = image / 2 + 0.5
        image = image.numpy().transpose(1, 2, 0)
        plt.imsave(f'{img_path}/{i+len(train_set)+1:05d}.png', image)

    # create and save the data file with image filenames and the labels
    data_df = pd.DataFrame(dict(
        image=[f'{i+1:05d}.png' for i in range(len(train_set)+len(test_set))],
        label=labels,
        label_name=[label_map[label] for label in labels]
    ))
    data_df.to_csv(f'{dataset_path}/data.csv', index=False)
    


def get_dataset(data_df: pd.DataFrame, seed=20, **kwargs):
    """Get a custom dataset by defining label and the associated count value or fraction

    Args:
        data_df (pd.DataFrame): _description_
        kwargs: label'

    Returns:
        _type_: _description_
    """
    np.random.seed(seed)

    data_df = data_df.reset_index(drop=True)

    label_count_df = pd.DataFrame({
        'label': list(kwargs.keys()),
        'count': list(kwargs.values())
    })

    label_count_dict = dict(
        zip(label_count_df['label'], label_count_df['count']))

    labels = list(label_count_dict.keys())
    # print(labels)
    # print([len(data_df.query(f'label_name == "{label}"')) for label in labels ])
    return_data_idx = [i for label in labels
                       for i in data_df.query(f'label_name == "{label}"')
                       .sample(label_count_dict[label]).index
                       ]

    return data_df.iloc[return_data_idx].reset_index(drop=True)


def get_test_dataset(dataset_path, SEED=20):
    """Get test dataset from a random seed

    Args:
        dataset_path (_type_): _description_
        SEED (int, optional): _description_. Defaults to 20.

    Returns:
        _type_: _description_
    """
    np.random.seed(SEED)
    data_df = pd.read_csv(dataset_path + '/data.csv')
    test_dataset = data_df.groupby('label') .sample(frac=.2) \
        .query('image != "51101.png"')  # 51101.png has a loading problem
    return test_dataset


def generate_data_owner_datasets(labels):
    """Generate data owner datasets by labels

    Args:
        labels (_type_): _description_

    Returns:
        _type_: _description_
    """    
    label_count_info = {label:get_random_hundreds() for label in labels}
    return label_count_info


class Dataset(torch.utils.data.Dataset):
    """_summary_"""

    def __init__(self, images, labels, feature_extractor, transform,
                 pre_trained_model=None, device='cpu'):
        """_summary_

        Args:
            images (_type_): _description_
            labels (_type_): _description_
            feature_extractor (_type_): _description_
            pre_trained_model (_type_): _description_
            transform (_type_): _description_
            device (_type_): _description_
        """
        self.images = images
        self.labels = labels
        self.transform = transform
        self.feature_extractor = feature_extractor
        self.pre_trained_model = pre_trained_model
        self.device = device

    def __len__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return len(self.images)

    def __getitem__(self, index):
        """_summary_

        Args:
            index (_type_): _description_

        Returns:
            _type_: _description_
        """
        image = Image.open(self.images[index])
        image = np.array(image.convert('RGB'))

        if self.transform is not None:
            image = self.transform(image=image)['image']

        if self.feature_extractor is not None:
            image = Image.fromarray(image, 'RGB')
            image = self.feature_extractor(image, return_tensors='pt')[
                'pixel_values'][0]
        else:
            image = torch.tensor(image)

        if self.pre_trained_model is not None:
            logits = self.pre_trained_model(image.unsqueeze(0).to(self.device)) \
                .hidden_states[-1][:, -1, :].cpu().squeeze().detach()
        else:
            logits = image
        return logits, self.labels[index]


def get_loader(images, labels, feature_extractor, transform,
               pre_trained_model=None, device='cpu', batch_size=32, shuffle=True):
    """_summary_

    Args:
        images (_type_): _description_
        labels (_type_): _description_
        feature_extractor (_type_): _description_
        transform (_type_): _description_
        pre_trained_model (_type_, optional): _description_. Defaults to None.
        batch_size (int, optional): _description_. Defaults to 32.
        shuffle (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """
    return torch.utils.data.DataLoader(
        Dataset(images, labels, feature_extractor, transform,
                pre_trained_model=pre_trained_model, device=device),
        batch_size=batch_size,
        shuffle=shuffle
    )
