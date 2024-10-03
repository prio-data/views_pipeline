import sys
print(sys.path)
from pathlib import Path

# insert common_utils path into sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "common_utils"))
print(sys.path)

# import common_utils module
from set_path import setup_root_paths, setup_model_paths, setup_ensemble_paths