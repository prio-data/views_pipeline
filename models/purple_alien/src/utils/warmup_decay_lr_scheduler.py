import torch
from torch.optim.lr_scheduler import _LRScheduler

class WarmupDecayLearningRateScheduler(_LRScheduler):
    def __init__(self, optimizer, d, warmup_steps, last_epoch=-1):
        self.d = d
        self.warmup_steps = warmup_steps
        super().__init__(optimizer, last_epoch)

    def get_lr(self):
        step_num = self.last_epoch + 1
        scale = self.d**(-0.5)
        lr = scale * min(step_num**(-0.5), step_num * self.warmup_steps**(-1.5))
        return [lr] * len(self.base_lrs)
