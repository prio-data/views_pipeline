import os
import re
import logging
import pandas as pd
import sys
from pathlib import Path
from tabulate import tabulate

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Path to the root and querysets
PATH = Path(__file__).resolve()
indices = [i for i, x in enumerate(PATH.parts) if x == "views_pipeline"]
PATH_ROOT = Path(*PATH.parts[:indices[-1] + 1])

querysets_path = PATH_ROOT / 'common_querysets'
GITHUB_URL = 'https://github.com/prio-data/views_pipeline/blob/production/' 

def extract_columns_from_querysets(querysets_path):
    """
    Parses each queryset file in the common_querysets folder to extract columns, querysets, and LOA.
    """
    columns_info = []
    
    for file_path in querysets_path.glob("*.py"):
        with open(file_path, 'r') as file:
            content = file.read()
            queryset_name = file_path.stem
            
            # Find all Column definitions
            column_matches = re.findall(r'Column\((.*?)\)', content)
            for match in column_matches:
                column_name = re.search(r'"(.*?)"', match).group(1)
                loa_match = re.search(r'from_loa="(.*?)"', match)
                loa = loa_match.group(1) if loa_match else None
                columns_info.append({
                    'column_name': column_name,
                    'queryset': queryset_name,
                    'loa': loa
                })
    
    # Convert to DataFrame for merging and remove duplicates
    df = pd.DataFrame(columns_info).drop_duplicates()
    
    # Group by column_name and aggregate querysets as a comma-separated string
    df = df.groupby(['column_name', 'loa'], as_index=False).agg({
        'queryset': lambda x: ', '.join(sorted(set(x)))  # Join unique querysets per feature
    })
    
    return df

def generate_markdown_table(columns_info):
    """
    Generates a nicely formatted markdown table for a feature catalog.
    """
    headers = ['Name in viewser', 'Human-readable name', 'Data source (with link)', 
               'Last updated (minutes:hours:day:month:year)', 'Associated querysets/models', 'Notes']

    table_data = []
    for _, row in columns_info.iterrows():
        table_data.append([
            row['column_name'],
            '',  # Placeholder for Human-readable name
            '',  # Placeholder for Data source
            'needs manual update (as of now)',  # Placeholder for Last updated
            row['queryset'],
            '',  #Placeholder for notes
        ])
    
    # Generate markdown with tabulate
    markdown_table = tabulate(table_data, headers=headers, tablefmt="pipe", colalign=("center",))

    return markdown_table

if __name__ == "__main__":
    # Extract feature information from querysets
    columns_info = extract_columns_from_querysets(querysets_path)
    
    # Generate the markdown table for the feature catalog
    feature_catalog = generate_markdown_table(columns_info)
    
    # Save the markdown table
    with open('documentation/catalogs/feature_catalog.md', 'w') as f:
        f.write(feature_catalog)
