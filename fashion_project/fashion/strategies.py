import torch
import numpy as np
from typing import List

from .utils import fix_random_seed
from sklearn.cluster import KMeans

def random_sampling(pred_probs: torch.Tensor, budget : int = 1000) -> List[int]:
  '''Randomly pick examples.
  :param pred_probs: list of predicted probabilities for the production set in order.
  :param budget: the number of examples you are allowed to pick for labeling.
  :return indices: A list of indices (into the `pred_probs`) for examples to label.
  '''
  fix_random_seed(42)
  
  indices = []
  # ================================
  # FILL ME OUT
  # Randomly pick a 1000 examples to label. This serves as a baseline.
  # Note that we fixed the random seed above. Please do not edit.
  # HINT: when you randomly sample, do not choose duplicates.
  # HINT: please ensure indices is a list of integers
  indices = np.arange(len(pred_probs))
  indices = np.sort(np.random.choice(indices, size=budget, replace=False))
  indices = indices.tolist()
  # ================================
  return indices

def uncertainty_sampling(pred_probs: torch.Tensor, budget : int = 1000) -> List[int]:
  '''Pick examples where the model is the least confident in its predictions.
  :param pred_probs: list of predicted probabilities for the production set in order.
  :param budget: the number of examples you are allowed to pick for labeling.
  :return indices: A list of indices (into the `pred_probs`) for examples to label.
  '''
  indices = []
  chance_prob = 1 / 10.  # may be useful
  # ================================
  # FILL ME OUT
  # Sort indices by the predicted probabilities and choose the 1000 examples with 
  # the least confident predictions. Think carefully about what "least confident" means 
  # for a N-way classification problem.
  # Take the first 1000.
  # HINT: please ensure indices is a list of integers
  scores = []
  for i in range(len(pred_probs)):
    pred_probs_i = pred_probs[i].numpy().tolist()
    scores.append(abs(max(pred_probs_i) - chance_prob))
  indices = np.argsort(scores)[:budget]
  indices = indices.tolist()
  # ================================
  return indices

def margin_sampling(pred_probs: torch.Tensor, budget : int = 1000) -> List[int]:
  '''Pick examples where the difference between the top two predicted probabilities is the smallest.
  :param pred_probs: list of predicted probabilities for the production set in order.
  :param budget: the number of examples you are allowed to pick for labeling.
  :return indices: A list of indices (into the `pred_probs`) for examples to label.
  '''
  indices = []
  # ================================
  # FILL ME OUT
  # Sort indices by the different in predicted probabilities in the top two classes per example.
  # Take the first 1000.
  scores = []
  for i in range(len(pred_probs)):
    pred_probs_i = pred_probs[i].numpy().tolist()
    pred_probs_i = sorted(pred_probs_i)[::-1]
    scores.append(pred_probs_i[0] - pred_probs_i[1])
  indices = np.argsort(scores)[:budget]
  indices = indices.tolist()
  # ================================
  return indices

def entropy_sampling(pred_probs: torch.Tensor, budget : int = 1000) -> List[int]:
  '''Pick examples with the highest entropy in the predicted probabilities.
  :param pred_probs: list of predicted probabilities for the production set in order.
  :param budget: the number of examples you are allowed to pick for labeling.
  :return indices: A list of indices (into the `pred_probs`) for examples to label.
  '''
  indices = []
  epsilon = 1e-6
  # ================================
  # FILL ME OUT
  # Entropy is defined as -E_classes[log p(class | input)] aja the expected log probability
  # over all K classes. See https://en.wikipedia.org/wiki/Entropy_(information_theory).
  # Sort the indices by the entropy of the predicted probabilities from high to low.
  # Take the first 1000.
  # HINT: Add epsilon when taking a log for entropy computation
  def calculate_entropy(probs):
    return -np.sum(probs * np.log(probs + epsilon))
  
  scores = []
  for i in range(len(pred_probs)):
    pred_probs_i = pred_probs[i].numpy()
    entropy = calculate_entropy(pred_probs_i)
    scores.append(entropy)
  indices = np.argsort(scores)[::-1][:budget]
  indices = indices.tolist()
  # ================================
  return indices
