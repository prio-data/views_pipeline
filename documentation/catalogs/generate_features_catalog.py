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

def get_path_common_querysets():
    """
    Retrieves the path to the 'common_querysets' directory within the 'views_pipeline' directory.

    This function identifies the 'views_pipeline' directory within the path of the current file,
    constructs a new path up to and including this directory, and then appends the relative path
    to the 'common_querysets' directory. If the 'views_pipeline' directory or the 'common_querysets'
    directory is not found, it raises a ValueError.

    Returns:
        Path: The path to the 'common_querysets' directory.

    Raises:
        ValueError: If the 'views_pipeline' directory or the 'common_querysets' directory is not found in the provided path.
    """

    PATH = Path(__file__)

    # Locate 'views_pipeline' in the current file's path parts
    if 'views_pipeline' in PATH.parts:
        PATH_ROOT = Path(*PATH.parts[:PATH.parts.index('views_pipeline') + 1])
        PATH_COMMON_QUERYSETS = PATH_ROOT / 'common_querysets'

        # Check if 'common_querysets' directory exists
        if not PATH_COMMON_QUERYSETS.exists():
            raise ValueError("The 'common_querysets' directory was not found in the provided path.")
        
    else:
        raise ValueError("The 'views_pipeline' directory was not found in the provided path.")

    return PATH_COMMON_QUERYSETS


def extract_columns_from_querysets(PATH_COMMON_QUERYSETS):
    """
    Parses each queryset file in the common_querysets folder to extract columns, querysets, and LOA.
    """
    columns_info = []
    
    for file_path in PATH_COMMON_QUERYSETS.glob("*.py"):
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
            'needs manual update',  # Placeholder for Human-readable name
            'needs manual update',  # Placeholder for Data source
            'needs manual update (as of now)',  # Placeholder for Last updated
            row['queryset'],
            '',  #Placeholder for notes
        ])
    
    # Generate markdown with tabulate
    markdown_table = tabulate(table_data, headers=headers, tablefmt="pipe", colalign=("center",))

    return markdown_table

if __name__ == "__main__":

    GITHUB_URL = 'https://github.com/prio-data/views_pipeline/blob/production/' 

    PATH_COMMON_QUERYSETS = get_path_common_querysets()

    # Extract feature information from querysets
    columns_info = extract_columns_from_querysets(PATH_COMMON_QUERYSETS)
    
    # Generate the markdown table for the feature catalog
    feature_catalog = generate_markdown_table(columns_info)
    
    # Save the markdown table
    with open('feature_catalog.md', 'w') as f: # saved locally right next to this script
        f.write(feature_catalog)
