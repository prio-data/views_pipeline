# https://pytorch.org/vision/stable/_modules/torchvision/ops/focal_loss.html

import torch
import torch.nn as nn
import torch.nn.functional as F

class FocalLoss(nn.Module):
    def __init__(self, alpha=0.25, gamma=2.0, reduction='mean'):
        super(FocalLoss, self).__init__()
        self.alpha = alpha  # Focal loss balancing parameter
        self.gamma = gamma  # Focal loss focusing parameter
        self.reduction = reduction  # Loss reduction method

    def forward(self, logits, targets):

        logits, targets = logits.unsqueeze(0), targets.unsqueeze(0)

        # since you are not taking log(p) anywhere, you don't need to clamp it for numerical stability.
        p = torch.sigmoid(logits)

        ce_loss = F.binary_cross_entropy_with_logits(logits, targets, reduction="none")# Calculate the cross-entropy loss. inputs should be Predicted unnormalized logits according to the documentation         
        p_t = p * targets + (1 - p) * (1 - targets) # Calculate the probability of the true class
        loss = ce_loss * ((1 - p_t) ** self.gamma)

        if self.alpha >= 0:
            alpha_t = self.alpha * targets + (1 - self.alpha) * (1 - targets) 
            loss = alpha_t * loss # multiple alpha_t with targets here to balance the loss

        if self.reduction == 'mean':
            return loss.mean()  # Average the loss if reduction is set to 'mean'
        elif self.reduction == 'sum':
            return loss.sum()  # Sum the loss if reduction is set to 'sum'
        else:
            return loss  # Return the focal loss without reduction

