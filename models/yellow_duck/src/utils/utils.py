import wandb

def wandb_log(project_name,entity_name,entity_to_log,name_of_entity) -> None:
    '''
    This function logs the entity to Weights & Biases
    
    Args:
    project_name: The name of the project in Weights & Biases
    entity_name: The name of the entity in Weights & Biases
    entity_to_log: The entity to log
    name_of_entity: The name of the entity to log
    
    Returns:
    None
    '''
    wandb.init(project=project_name,entity = entity_name)
    wandb.log({f'{name_of_entity}': entity_to_log})
    wandb.finish()