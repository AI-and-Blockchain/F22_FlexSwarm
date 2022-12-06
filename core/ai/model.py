import torch
import torch.nn as nn
from transformers import ViTFeatureExtractor, ViTForImageClassification

from utils import seed_everything


def get_vit_model(device='cpu'):
    # download vision transformer model
    vit_feature_extractor = ViTFeatureExtractor.from_pretrained(
        'google/vit-base-patch16-224-in21k')
    vit_model = ViTForImageClassification.from_pretrained(
        'google/vit-base-patch16-224', output_hidden_states=True).to(device)

    # freeze the pre-trained model
    vit_model.eval()
    for param in vit_model.parameters():
        param.requires_grad = False
    return vit_feature_extractor, vit_model


class CNNClassifier(nn.Module):
    def __init__(self, in_dim, out_dim, dropout=0.1):
        super(CNNClassifier, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 32, (4, 4), stride=2, padding=0),
            nn.ReLU(),
            nn.LazyBatchNorm2d()
        )
        self.conv2 = nn.Sequential(
            nn.LazyConv2d(64, (2, 2), stride=1, padding=0),
            nn.ReLU(),
            nn.LazyBatchNorm2d()
        )

        self.conv3 = nn.Sequential(
            nn.LazyConv2d(64, (1, 1), stride=1),
            nn.ReLU()
        )

        self.fc_out = nn.Sequential(
            nn.Flatten(),
            nn.LazyLinear(256),
            nn.ReLU(),
            nn.LazyLinear(out_dim)
        )

        self.dropout = nn.Dropout(p=dropout)

    def forward(self, x):
        x = self.conv3(self.conv2(self.conv1(x)))
        x = self.dropout(x)
        x = self.fc_out(x)
        return x


def get_model_parameters(model_path):
    """_summary_

    Args:
        model_path (_type_): _description_

    Returns:
        _type_: _description_
    """    
    seed_everything()
    model = torch.load(model_path, map_location='cpu')
    model.eval()
    for param in model.parameters():
        param.requires_grad = False
    print(model)

    # get model structure
    model_structure = '|'.join(
        [layer_str.split('): ')[1] for layer_str in str(model).split('\n')[1:-1]])

    # get model parameters
    with torch.no_grad():
        model_parameters = {name: val.detach().tolist()
                                 for name, val in model.named_parameters()}

    # Since the model uses normalization, we also need to send the mean and variance
    try:
        model_parameters['0.running_mean'] = model[0].running_mean.tolist()
        model_parameters['0.running_var'] = model[0].running_var.tolist()
    except:
        ...

    # print weight name and shape
    model_parameters_names = list(model_parameters.keys())
    model_parameters_vals = list(model_parameters.values())
    model_parameters_names = '|'.join(model_parameters_names)

    return {
        'model_structure': model_structure,
        'model_parameters_names': model_parameters_names,
        'model_parameters_vals': model_parameters_vals
    }
