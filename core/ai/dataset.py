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
    data_df = pd.read_csv(f'{dataset_path}/data.csv')


def get_dataset(data_df: pd.DataFrame, label2id, drop=True, **kwargs):
    """Get a custom dataset by defining label and the associated count value or fraction

    Args:
        data_df (pd.DataFrame): _description_
        drop (bool, optional): whether the data selected will be removed from data_df. Defaults to True.
        kwargs: label'

    Returns:
        _type_: _description_
    """

    label_count_df = pd.DataFrame({
        'label': list(kwargs.keys()),
        'count': list(kwargs.values())
    })

    # Sanity check
    for label in label_count_df.label:
        if label == 'other':
            continue
        # Assert the label exists
        assert np.logical_or(
            label in data_df.label.astype('str').unique().tolist(),
            label in data_df.label_name.unique().tolist()
        )
        # Assert no two labels are the same
        # TODO

    # Change the fraction of data to number if the count is a fraction
    for i, (label, count) in label_count_df.iterrows():
        if label == 'other':
            continue
        if count <= 1:
            if isinstance(label, str):
                label = label2id[label]
            label_count_total = len(data_df.query(f'label == {label}'))
            label_count_df.iloc[i, 1] = round(count * label_count_total)

    label_count_df['count'] = label_count_df['count'].astype('int32')
    label_count_df['label'] = label_count_df['label'].apply(
        lambda x: label2id[x])
    # Convert a data frame to dictionary
    label_count_dict = dict(
        zip(label_count_df['label'], label_count_df['count']))

    labels = [label for label in label_count_dict if label != -1]

    return_data_idx = [i for label in labels
                       for i in data_df.query(f'label == {label}')
                       .sample(label_count_dict[label]).index
                       ]
    # Add indices for other labels
    return_data_idx += [] if -1 not in label_count_dict else \
        data_df.query(f'label not in {labels}') \
        .sample(label_count_dict[-1]).index.tolist()

    images = data_df.image[return_data_idx]
    labels = [int(l)
              for label, count in zip(label_count_df['label'], label_count_df['count'])
              for l in np.ones(count) * label]

    return (
        data_df.iloc[[i for i in data_df.index if i not in return_data_idx]],
        pd.DataFrame({
            'image': images,
            'label': labels
        }).reset_index(drop=True)
    )


class Dataset(torch.utils.data.Dataset):
    """_summary_"""

    def __init__(self, data, img_path, feature_extractor, vit_model, transform, device):
        """_summary_

        Args:
            data (_type_): _description_
            img_path (_type_): _description_
            feature_extractor (_type_): _description_
            vit_model (_type_): _description_
            transform (_type_): _description_
            device (_type_): _description_
        """
        self.images = [f'{img_path}/{i}' for i in data.image]
        self.labels = data.label.tolist()
        self.transform = transform
        self.feature_extractor = feature_extractor
        self.vit_model = vit_model
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
        if self.transform is not None:
            image = np.array(image)
            image = Image.fromarray(
                self.transform(image=image)['image'], 'RGB')
        image = self.feature_extractor(image, return_tensors='pt')[
            'pixel_values'][0]
        logits = self.vit_model(image.unsqueeze(0).to(self.device)) \
            .hidden_states[-1][:, -1, :].cpu().squeeze().detach()
        return logits, self.labels[index]


def get_loader(data, feature_extractor, vit_model, transform, batch_size=32, shuffle=True):
    """_summary_

    Args:
        data (_type_): _description_
        feature_extractor (_type_): _description_
        vit_model (_type_): _description_
        transform (_type_): _description_
        batch_size (int, optional): _description_. Defaults to 32.
        shuffle (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """
    return torch.utils.data.DataLoader(
        Dataset(data, feature_extractor, vit_model, transform),
        batch_size=batch_size,
        shuffle=shuffle
    )
