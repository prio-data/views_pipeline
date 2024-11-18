import wandb
import warnings

from views_pipeline.cli.utils import parse_args, validate_arguments
from views_pipeline.logging.utils import setup_logging
from views_pipeline.managers.path_manager import ModelPath
warnings.filterwarnings("ignore")

try:
    model_name = ModelPath.get_model_name_from_path(__file__)
except Exception as e:
    raise RuntimeError(f"An unexpected error occurred: {e}.")
logger = setup_logging(model_name=model_name)

from views_stepshifter.manager.stepshifter_manager import StepshifterManager

if __name__ == "__main__":
    wandb.login()

    args = parse_args()
    validate_arguments(args)

    if args.sweep:
        StepshifterManager(model_path=ModelPath(model_name)).execute_sweep_run(args)
        # execute_sweep_run(args)
    else:
        StepshifterManager(model_path=ModelPath(model_name)).execute_single_run(args)
