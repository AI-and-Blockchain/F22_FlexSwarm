import os
import torch
import random
import numpy as np
import json
import torch.nn as nn
from predict import predict_from_dataset
from utils import seed_everything, label_enc, print_evaluation_metrics, load_data_owner_dataset, get_device
import pandas as pd
from collections import Counter

def loadmodel(name):
    x = open('model_parameters/'+ name+'.json')
    data = json.load(x)
    model_structure = data['model_structure']
    model_parameters_names = data['model_parameters_names']
    model_parameters_vals_= data['model_parameters_vals']
    model_parameters_vals =[]
    for i in model_parameters_vals_:
        tmp=torch.tensor(i)
        tmp2=torch.rand(tmp.shape)*0.0000001
        tmp3=torch.add(tmp,tmp2)
        model_parameters_vals.append(tmp3.tolist())
    model_parameters_names = [f'[{name.split(".")[0]}].{name.split(".")[1]}'
                                   for name in model_parameters_names.split('|')]
    received_model = nn.Sequential(
    *[eval('nn.' + layer) for layer in model_structure.split('|')]
    )
    for parameters_name, parameters_val in zip(model_parameters_names, model_parameters_vals):
        exec(f'received_model{parameters_name} = nn.Parameter(torch.tensor(parameters_val))')
    for param in received_model.parameters():
        param.requires_grad = False
    return received_model.to('cuda')


def ensemble_model(client):
    dataset_path = '../../Datasets/CIFAR10'
    #corresponding labels for each model
    x = open('../../dataOwnerLabelInfo.json')
    data= json.load(x)
    model_names=[]
    model_labels=[]
    for i in data:
        if(data[i][0]=='trainer'):
            model_names.append(('model_'+i))
            model_labels.append(data[i][1].split(', '))
    all_models=[]
    for i in model_names:
        all_models.append(loadmodel(i))
    df = pd.DataFrame()
    for i in range(len(all_models)):
        name= model_names[i].split('_')[1]
        tmp=pd.Series(predict_from_dataset(dataset_path,name,client,model_labels[i],all_models[i],'cuda'))
        df[model_names[i]]=tmp
    tmp = df.T
    result=[]
    for x in tmp.columns:
        result.append(tmp[x].value_counts().idxmax())
    client_dataset = load_data_owner_dataset(dataset_path, client)
    client_dataset['prediction'] = result
    client_dataset.to_csv(f'Client_{client}.csv')