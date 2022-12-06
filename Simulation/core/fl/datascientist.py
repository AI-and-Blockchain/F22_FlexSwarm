import syft as sy

import torch
from torch import nn
from syft.core.adp.data_subject import DataSubject
def showdata(domain):
    print(domain.datasets)
def requestdata(domain,index):
    sent = domain.datasets[index]
    asset = sent.assets
    for i in asset:
        result = sent[i['name']]
        result.request(reason='research')
    print("requesting for data wait for confirmation")

def getmodel(domain,index):
    try:
        received_model_structure = domain.datasets[index].description
        received_model = nn.Sequential(
            *[eval('nn.' + layer) for layer in received_model_structure.split('|')]
        )
        sent = domain.datasets[1]
        asset = sent.assets
        for i in asset:
            name = i['name']
            result = sent[name]
            name = f'[{name.split(".")[0]}].{name.split(".")[1]}'
            x = result.get().child.child

            ##add differential privacy


            x = torch.tensor(x).to(dtype=torch.float32)
            exec(f'received_model{name} = nn.Parameter(x)')
    except:
        print("no permission")

    return received_model



