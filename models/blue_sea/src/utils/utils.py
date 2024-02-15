import wandb


def wandb_log(project_name, entity_name, entity_to_log, name_of_entity):
    wandb.init(project=project_name, entity=entity_name)
    wandb.log({f'{name_of_entity}': entity_to_log})
    wandb.finish()


def wandb_init(project_name, entity_name):
    wandb.init(project=project_name, entity=entity_name)


def wandb_finish():
    wandb.finish()

