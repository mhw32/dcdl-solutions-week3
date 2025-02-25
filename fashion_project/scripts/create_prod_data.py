# Do not edit this file
import torch
from os.path import join
from tqdm import tqdm
from torchvision import datasets, transforms
from fashion.paths import DATA_DIR

def main():
  '''Create a production dataset by augmenting the test set of FashionMNIST.
  '''
  perturbations = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(degrees=60),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.2),
    transforms.ToTensor(),
  ])
  test_dataset = datasets.FashionMNIST(
    DATA_DIR,
    download = True,
    train = False,
    transform = perturbations,
  )
  images = []
  labels = []
  for image, label in tqdm(test_dataset):
    images.append(image)
    labels.append(label)

  images = torch.stack(images)
  labels = torch.Tensor(labels)
  
  torch.save({'images': images, 'labels': labels}, join(DATA_DIR, 'production/dataset.pt'))

if __name__ == "__main__":
  main()