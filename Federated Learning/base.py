import syft as sy
import numpy as np
import matplotlib.pyplot as plt
import os
import pydicom
import pandas as pd
import time
import torch
from syft.core.adp.entity import Entity

# %%

# %%
def login(email_, password_):
    domain_node = sy.login(email=email_, password=password_, port=8081)
    return domain_node


# %%
def upload(domain_node, keys, data):
    entities = []
    dataset = {}

    for i in range(len(keys)):
        name_ = keys[i]
        new_entity = Entity(name=name_)
        entities.append(new_entity)
        dataset[name_] = sy.Tensor(data[keys[i]]).private(min_val=-10, max_val=10, entities=new_entity)

    domain_node.load_dataset(
        assets=dataset,
        name="11",
        description="22",
        metadata="Any metadata you'd like to include goes here"
    )




