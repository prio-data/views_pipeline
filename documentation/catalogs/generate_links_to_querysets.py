import re
import ast

# Define the path to the model definition file in the cloned viewsforecasting repo
model_def_path = '../viewsforecasting/SystemUpdates/ModelDefinitions.py'

# Define the path to the cm and pgm querysets file in the cloned viewsforecasting repo
cm_querysets_path = '../viewsforecasting/Tools/cm_querysets.py'
pgm_querysets_path = '../viewsforecasting/Tools/pgm_querysets.py'

# The GitHub repo link
GITHUB_URL = 'https://github.com/prio-data/viewsforecasting/blob/github_workflows/'



def convert_to_dict(input_str):
    """
    It converts the string of every model from ModelDefinitions.py to a dict.
    """
    # Adjusted regex pattern to match 'algorithm' value that might contain parentheses or function calls
    input_str = input_str.replace("'", "\"")
    alg_pattern = r'"algorithm":\s*(.*?),\s*(?=\n)'
    
    # Convert 'algorithm' value to string if it isn't already a string
    dict_str = re.sub(
    alg_pattern,
    lambda m: f'"algorithm": \'{m.group(1)}\',' if not m.group(1).startswith('"') and not m.group(1).endswith('"') else f'"algorithm": {m.group(1)},' ,
    input_str
    )
    
    # Evaluate the dictionary string using ast.literal_eval
    try:
        dictionary = ast.literal_eval(dict_str)
    except Exception as e:
        print(f"Error converting string to dict: {e}")
        print(dict_str)
        return None
    
    return dictionary



def extract_models(model_def_path):
    """
    It creates a list of dictionaries containing every model from ModelDefinitions.py.
    """
    with open(model_def_path, 'r') as file:
        content = file.read()

    models_dict = []
    model_dicts_str = re.finditer('model = {', content)
    
    for model_str in model_dicts_str:
        start_index = model_str.end(0) - 1
        end_index = content.find("}", start_index) + 1
        model_dict_str = content[start_index:end_index]
        model_dict = convert_to_dict(model_dict_str)
        models_dict.append(model_dict)
    return models_dict


def find_querysets(queryfilepath, model):
    """
    Parse cm_querysets.py and find the queryset for every model and return a markdown link with the github link pointing to the right line number.
    """
    
    with open(queryfilepath, 'r') as f:
        # Loop through each line in the file
        for i, line in enumerate(f, start=1):
            
            # Search for the pattern in the line
            match = re.search(r'Queryset\("' + re.escape(model['queryset']) , line)
            
            if match:
                #print(f"Match found: {match.group(0)} on line {i}")
                markers = {
                'marker' : match.group(0),
                'line' : i,
                'file' : queryfilepath.split('viewsforecasting/')[1]}
                link_template = '- [{marker}]({url}{file}#L{line})'
                new_links = link_template.format(marker=markers['marker'],
                                      url=GITHUB_URL,
                                      file=markers['file'],
                                      line=markers['line']) 
                break  # Stop after finding the first match
            else:
                new_links = model['queryset']
         
    return new_links







def generate_markdown_table(models):
    """
    Function to generate markdown table from the model dictionaries.
    """
    headers = ['Model Name', 'Algorithm', 'Target', 'Input Features', 'Non-default Hyperparameters', 'Forecasting Type', 'Implementation Status', 'Implementation Date', 'Author']
    
    markdown_table = '| ' + ' '.join([f"{header} |" for header in headers]) + '\n'
    markdown_table += '| ' + ' '.join(['-' * len(header) + ' |' for header in headers]) + '\n'

    
    for model in models:
        if 'pgm' in model.get('queryset', ''):
            querysetname = find_querysets(pgm_querysets_path, model) 
        else:
            querysetname = find_querysets(cm_querysets_path, model) 


        row = [
            model.get('modelname', ''),
            str(model.get('algorithm', '')).split('(')[0],
            model.get('depvar', ''),
            #model.get('data_train', ''),
            querysetname ,   #model.get('queryset', ''),
            #model.get('preprocessing', ''),
            re.search(r'\((.*?)\)', model.get('algorithm','')).group(1) if re.search(r'\((.*?)\)', model.get('algorithm','')) else 'None',
            'Direct multi-step',
            #model.get('level', ''),
            #model.get('description', ''),
            #model.get('long_description', '').replace('\n', ' ')[:100] + '...'
            'no',
            'NA',
            'NA'
        ]
        markdown_table += '| ' + ' | '.join(row) + ' |\n'
        
    return markdown_table

models_dict = extract_models(model_def_path)
markdown_table = generate_markdown_table(models_dict)

with open('documentation/catalogs/cm_model_catalog.md', 'w') as f:
    f.write(markdown_table)








