import pandas as pd
import numpy as np


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


def get_dataset_old(data_df: pd.DataFrame, label2id, drop=True, **kwargs):
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

    # sanity check
    for label in label_count_df.label:
        if label == 'other':
            continue
        # assert the label exists
        assert np.logical_or(
            label in data_df.label.astype('str').unique().tolist(),
            label in data_df.label_name.unique().tolist()
        )
        # assert no two labels are the same
        # TODO

    # change the fraction of data to number if the count is a fraction
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
    # convert a data frame to dictionary
    label_count_dict = dict(
        zip(label_count_df['label'], label_count_df['count']))

    labels = [label for label in label_count_dict if label != -1]

    return_data_idx = [i for label in labels
                       for i in data_df.query(f'label == {label}')
                       .sample(label_count_dict[label]).index
                       ]
    # add indices for other labels
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
