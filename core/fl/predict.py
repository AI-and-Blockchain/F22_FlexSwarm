import torch
from tqdm import tqdm
import albumentations as A

from model import get_vit_model
from dataset import get_loader, get_test_dataset
from utils import seed_everything, label_enc, print_evaluation_metrics, load_data_owner_dataset, get_device

def predict(data_loader, model, device='cpu'):
    '''Get predictions'''
    model.eval()
    predictions = []
    for batch_images, _ in tqdm(data_loader):
        logits = model(batch_images.to(device))
        predictions += logits.argmax(1).cpu().tolist()
    return predictions

def predict_from_dataset(dataset_path, data_owner_id, client_id, model_label, model, device):
    # Load image paths
    img_path = dataset_path + '/images'
    
    # Set a fixed random seed
    seed_everything()
    _,_,label2id_,id2label_=label_enc(load_data_owner_dataset(dataset_path, data_owner_id))
    # Load client dataset
    client_dataset_ = load_data_owner_dataset(dataset_path, client_id)
    num_classes = client_dataset_.label_name.unique()
    predictions_=[]
    for i in num_classes:
        if i in model_label:
            client_dataset = client_dataset_.groupby('label_name').get_group(i)
            images, labels, label2id, id2label = label_enc(client_dataset)
             # Get client dataset data loader
            vit_feature_extractor, vit_model = get_vit_model(device)
            eval_transform = A.Compose([A.Resize(224, 224)])
            train_data_loader = get_loader(images, labels, vit_feature_extractor, eval_transform,
                                           pre_trained_model=vit_model, device=device, shuffle=False)

            # Get data owner's model
            print(train_data_loader,model)
            predictions = predict(train_data_loader, model, device)
            result =  [id2label_[elem] for elem in predictions]
            predictions_+=result
            print(len(predictions_))
    # Save predictions
    return predictions_
