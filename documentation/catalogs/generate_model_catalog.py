import os
import logging
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

import sys
from pathlib import Path

PATH = Path(__file__).resolve()
indices = [i for i, x in enumerate(PATH.parts) if x == "views_pipeline"]
PATH_ROOT = Path(*PATH.parts[:indices[-1] + 1])

sys.path.insert(0, str(PATH_ROOT))
sys.path.insert(0, str(PATH_ROOT/"common_utils"))

from model_path import ModelPath

GITHUB_URL = 'https://github.com/prio-data/views_pipeline/blob/main/' 





def extract_models(model_class):
    """
    It creates a dictionary containing all the necessary information about a model by merging the config_meta.py, config_deployement.py and config_hyperparameters.py dictionaries.

    Parameters:
    model_class: ModelPath class object from ModelPath.py

    Returns:
    model_dict: A dictionary containing the following relevant keys:
        -name: model name from config_meta.py
        -algorithm: algorithm from config_meta.py
        -depvar: depvar from config_meta.py
        -queryset: markdown link with marker 'queryset' from config_meta.py pointing to the queryset in common_querysets
        -level: 'priogrid_month' or 'country_month' from queryset
        -creator: creator from config_meta.py
        -deployment_status: deployment_status from config_deployment.py
        -hyperparameters: markdown link with marker 'hyperparameters model_name' config_meta.py pointing to the model specific config_hyperparameters.py
    """
    
    model_dict = {}
    tmp_dict = {}
    config_meta = os.path.join(model_class.configs, 'config_meta.py')
    config_deployment = os.path.join(model_class.configs, 'config_deployment.py')
    config_hyperparameters = os.path.join(model_class.configs, 'config_hyperparameters.py')

    
    if os.path.exists(config_meta):
        logging.info(f"Found meta config: {config_meta}")
        with open(config_meta, 'r') as file:
            code = file.read()
            exec(code, {}, tmp_dict)
        model_dict.update(tmp_dict['get_meta_config']())
        model_dict['queryset'] = create_link(model_dict['queryset'], model_class.queryset_path) if 'queryset' in model_dict else 'None'


    if os.path.exists(config_deployment):
        logging.info(f"Found deployment config: {config_deployment}")
        with open(config_deployment, 'r') as file:
            code = file.read()
            exec(code, {}, tmp_dict) 
        model_dict.update(tmp_dict['get_deployment_config']())

    if os.path.exists(config_hyperparameters):
        logging.info(f"Found hyperparameters config: {config_hyperparameters}") 
        model_dict['hyperparameters'] = create_link(f"hyperparameters {model_class.model_name}", Path(model_class.get_scripts()['config_hyperparameters.py']))
    
    return model_dict



def create_link(marker, filepath: Path):
    """
    Generates a markdown-formatted link to a specific file in the repository's main branch. It creates the link by merging the path of the repository and the relative_path created from filepath.

    Parameters:
    marker: a marker that will be displayed as the clickable text in the markdown link
    filepath: absolute path of the file

    Returns:
    str: A markdown link in the format `- [marker](GITHUB_URL/relative_filepath)`
    """
    relative_path = filepath.relative_to(ModelPath.get_root())
    link_template = '- [{marker}]({url}{file})'
    return link_template.format(marker=marker, url=GITHUB_URL, file=relative_path)



def generate_markdown_table(models_list):
    """
    Function to generate markdown table from the model dictionaries.

    Parameters:
    model_list: list of model dictionaries containing all the necessary information

    Returns:
    markdown_table: a markdown table with links to the querysets and hyperparameters
    """

    headers = ['Model Name', 'Algorithm', 'Target', 'Input Features', 'Non-default Hyperparameters', 'Forecasting Type', 'Implementation Status', 'Implementation Date', 'Author']
    
    markdown_table = '| ' + ' '.join([f"{header} |" for header in headers]) + '\n'
    markdown_table += '| ' + ' '.join(['-' * len(header) + ' |' for header in headers]) + '\n'

    
    for model in models_list:
        

        row = [
            model.get('name', ''),
            str(model.get('algorithm', '')).split('(')[0],
            model.get('depvar', '') if model.get('depvar', '') else ", ".join(model.get('target(S)', '')),
            model.get('queryset', ''),
            model.get('hyperparameters',''),
            'None',#Direct multi-step',
            model.get('deployment_status', ''),
            'NA',
            model.get('creator', '')
        ]
        markdown_table += '| ' + ' | '.join(row) + ' |\n'
        
    return markdown_table




if __name__ == "__main__":
    #import time
    #start_time = time.time()

    models_list_cm = []
    models_list_pgm = []

    for model_name in os.listdir(PATH_ROOT / 'models'):
        model_path = os.path.join(PATH_ROOT / 'models', model_name)
        

        if os.path.isdir(model_path): 
            model_class = ModelPath(model_name, validate=True)
            


            model = extract_models(model_class)
            
            if 'level' in model and model['level'] == 'pgm':
                models_list_pgm.append(model)
            if 'level' in model and model['level'] == 'cm':
                models_list_cm.append(model)

            

            


    markdown_table_pgm = generate_markdown_table(models_list_pgm)
    with open('documentation/catalogs/pgm_model_catalog.md', 'w') as f:
        f.write(markdown_table_pgm)

    markdown_table_cm = generate_markdown_table(models_list_cm)
    with open('documentation/catalogs/cm_model_catalog.md', 'w') as f:
        f.write(markdown_table_cm)

    #print("--- %s seconds ---" % (time.time() - start_time))


