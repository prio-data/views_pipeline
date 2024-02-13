import wandb

def wandb_log(project_name,entity_name,entity_to_log,name_of_entity) -> None:
    wandb.init(project=project_name,entity = entity_name)
    wandb.log({f'{name_of_entity}': entity_to_log})
    wandb.finish()