from tqdm import tqdm

def predict(data_loader, model, device='cpu'):
    '''Get predictions'''
    model.eval()
    predictions = []
    for batch_images, _ in tqdm(data_loader):
        logits = model(batch_images.to(device))
        predictions += logits.argmax(1).cpu().tolist()
    return predictions