# Meta Tools

This folder contains several scripts for creating and assessing new model folders with proper structure.

## Building a new model

1. Run `python meta_tools/model_scaffold_builder.py` and follow the instructions. Ensure the model name is in the format `adjective_noun` (e.g., `happy_kitten`).
2. **Directory and Script Creation**: The script will create the necessary directories and files, including `README.md` and `requirements.txt`.
3. **Assessment**: The script will assess the created directories and scripts, logging any missing components.

To test the scripts in meta_tools, run `pytest -v meta_tools`