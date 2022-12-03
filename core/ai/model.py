import torch.nn as nn
from transformers import ViTFeatureExtractor, ViTForImageClassification


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
