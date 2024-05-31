import wandb

# there are things in other utils that should be here...

def add_wandb_monthly_metrics():
        
    # Define "new" monthly metrics for WandB logging
    wandb.define_metric("monthly/out_sample_month")
    wandb.define_metric("monthly/*", step_metric="monthly/out_sample_month")