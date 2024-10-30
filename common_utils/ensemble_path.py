from model_path import ModelPath
import logging
from pathlib import Path
from typing import Union
import sys
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class EnsemblePath(ModelPath):
    """
    A class to manage ensemble paths and directories within the ViEWS Pipeline.
    Inherits from ModelPath and sets the target to 'ensemble'.
    """

    _target = "ensemble"

    @classmethod
    def _initialize_class_paths(cls):
        """Initialize class-level paths for ensemble."""
        super()._initialize_class_paths()
        cls._models = cls._root / Path(cls._target + "s")
        # Additional ensemble-specific initialization...

    def __init__(
        self, ensemble_name_or_path: Union[str, Path], validate: bool = True
    ) -> None:
        """
        Initializes an EnsemblePath instance.

        Args:c
            ensemble_name_or_path (str or Path): The ensemble name or path.
            validate (bool, optional): Whether to validate paths and names. Defaults to True.
        """
        super().__init__(ensemble_name_or_path, validate)
        # Additional ensemble-specific initialization...
        print(self._validate)

    def _initialize_directories(self) -> None:
        """
        Initializes the necessary directories for the ensemble.

        Creates and sets up various directories required for the ensemble, such as architectures, artifacts, configs, data, etc.
        """
        # Call the parent class's _initialize_directories method
        super()._initialize_directories()

        # List of directories to keep
        keep_dirs = {
            "artifacts",
            "configs",
            "data",
            "data/generated",
            "data/processed",
            "notebooks",
            "reports",
            "reports/figures",
            "reports/papers",
            "reports/plots",
            "reports/slides",
            "reports/timelapse",
            "src",
            "src/dataloaders",
            "src/forecasting",
            "src/management",
            "src/offline_evaluation",
            "src/training",
            "src/utils",
            "src/visualization",
        }

        # Remove directories that are not in the keep_dirs list
        for attr, value in list(self.__dict__.items()):
            if Path(value).relative_to(self.model_dir) not in keep_dirs:
                delattr(self, attr)

        # Initialize directories as per the new structure
        self.model_dir = self._get_model_dir()
        self.artifacts = self._build_absolute_directory(Path("artifacts"))
        self.configs = self._build_absolute_directory(Path("configs"))
        self.data = self._build_absolute_directory(Path("data"))
        self.data_generated = self._build_absolute_directory(Path("data/generated"))
        self.data_processed = self._build_absolute_directory(Path("data/processed"))
        self.notebooks = self._build_absolute_directory(Path("notebooks"))
        self.reports = self._build_absolute_directory(Path("reports"))
        self.reports_figures = self._build_absolute_directory(Path("reports/figures"))
        self.reports_papers = self._build_absolute_directory(Path("reports/papers"))
        self.reports_plots = self._build_absolute_directory(Path("reports/plots"))
        self.reports_slides = self._build_absolute_directory(Path("reports/slides"))
        self.reports_timelapse = self._build_absolute_directory(
            Path("reports/timelapse")
        )
        self.src = self._build_absolute_directory(Path("src"))
        self.dataloaders = self._build_absolute_directory(Path("src/dataloaders"))
        self.forecasting = self._build_absolute_directory(Path("src/forecasting"))
        self.management = self._build_absolute_directory(Path("src/management"))
        self.offline_evaluation = self._build_absolute_directory(
            Path("src/offline_evaluation")
        )
        self.training = self._build_absolute_directory(Path("src/training"))
        self.utils = self._build_absolute_directory(Path("src/utils"))
        self.visualization = self._build_absolute_directory(Path("src/visualization"))
        self._templates = self.meta_tools / "templates"
        self._sys_paths = None
        # if self.common_querysets not in sys.path:
        #     sys.path.insert(0, str(self.common_querysets))
        # self.queryset_path = self.common_querysets / f"queryset_{self.model_name}.py"
        # self._queryset = None

    def _initialize_scripts(self) -> None:
        """
        Initializes the necessary scripts for the ensemble.

        Creates and sets up various scripts required for the ensemble, such as configuration scripts, main script, and other utility scripts.
        """
        self.scripts = [
            self._build_absolute_directory(Path("configs/config_deployment.py")),
            self._build_absolute_directory(Path("configs/config_hyperparameters.py")),
            self._build_absolute_directory(Path("configs/config_meta.py")),
            self._build_absolute_directory(Path("main.py")),
            self._build_absolute_directory(Path("README.md")),
            self._build_absolute_directory(Path("requirements.txt")),
            self._build_absolute_directory(Path("artifacts/model_metadata_dict.py")),
            self._build_absolute_directory(
                Path("src/forecasting/generate_forecast.py")
            ),
            self._build_absolute_directory(
                Path("src/management/execute_model_runs.py")
            ),
            self._build_absolute_directory(
                Path("src/management/execute_model_tasks.py")
            ),
            self._build_absolute_directory(
                Path("src/offline_evaluation/evaluate_ensemble.py")
            ),
            self._build_absolute_directory(Path("src/training/train_ensemble.py")),
            self._build_absolute_directory(Path("src/utils/utils_check.py")),
            self._build_absolute_directory(Path("src/utils/utils_run.py")),
            self._build_absolute_directory(Path("src/visualization/visual.py")),
            # self.common_querysets / f"queryset_{self.model_name}.py",
        ]


# if __name__ == "__main__":
#     ensemble_path = EnsemblePath("white_mustang", validate=True)
#     print(ensemble_path.get_directories())
#     del ensemble_path
