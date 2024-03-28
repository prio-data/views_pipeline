import sys
from pathlib import Path


PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS
#'/Users/sarakallis/Documents/PRIO Local/views_pipeline/common_utils', '/Users/sarakallis/Documents/PRIO Local/views_pipeline/models/electric_relaxation/src/training'

from set_path import setup_project_paths
setup_project_paths(PATH)

PATH_ARTIFACTS = [i for i in sys.path if "artifacts" in i][0] # this is a list with one element (a str), so I can just index it with 0 

calib_pickle_path = PATH_ARTIFACTS + "/model_calibration_partition.pkl"
print(calib_pickle_path)