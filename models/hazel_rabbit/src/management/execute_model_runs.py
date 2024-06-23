import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_artifacts_paths
setup_project_paths(PATH)

#from config_sweep import get_swep_config
from config_hyperparameters import get_hp_config
#from model_run_manager import model_run_manager
from execute_model_tasks import execute_model_tasks


def execute_sweep_run(args):
    print('Running sweep...')

    project = f"hazel_rabbit_sweep" # check naming convention
    
    print('Sweep run is not implemented. Exiting...')


def execute_single_run(args):
    
    # get config
    config = get_hp_config()
    config['run_type'] = args.run_type
    

    # get run type and denoting project name - check convention!
    project = f"hazel_rabbit_{args.run_type}"

    if args.run_type == 'calibration' or args.run_type == 'testing':
      
        execute_model_tasks(config = config, project = project, train = args.train, eval = args.evaluate, forecast = False)

    elif args.run_type == 'forecasting':
     
        execute_model_tasks(config = config, project = project, train = False, eval = False, forecast=True)

    else:
        raise ValueError(f"Invalid run type: {args.run_type}")


