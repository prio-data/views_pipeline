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
        # Initialize ensemble-specific directories only if the class is EnsemblePath
        if self.__class__.__name__ == "EnsemblePath":
            self._initialize_ensemble_specific_directories()

    def _initialize_ensemble_specific_directories(self):
        self.reports_figures = self._build_absolute_directory(Path("reports/figures"))
        self.reports_papers = self._build_absolute_directory(Path("reports/papers"))
        self.reports_plots = self._build_absolute_directory(Path("reports/plots"))
        self.reports_slides = self._build_absolute_directory(Path("reports/slides"))
        self.reports_timelapse = self._build_absolute_directory(
            Path("reports/timelapse")
        )

    def _initialize_scripts(self) -> None:
        """
        Initializes the necessary scripts for the ensemble.

        Creates and sets up various scripts required for the ensemble, such as configuration scripts, main script, and other utility scripts.
        """
        super()._initialize_scripts()
        # Initialize ensemble-specific scripts only if the class is EnsemblePath
        if self.__class__.__name__ == "EnsemblePath":
            self._initialize_ensemble_specific_scripts()

    def _initialize_ensemble_specific_scripts(self):
        """
        Initializes the ensemble-specific scripts by appending their absolute paths
        to the `self.scripts` list.

        The paths are built using the `_build_absolute_directory` method.

        Returns:
            None
        """
        self.scripts += [
            self._build_absolute_directory(Path("artifacts/model_metadata_dict.py")),
            self._build_absolute_directory(
                Path("src/offline_evaluation/evaluate_ensemble.py")
            ),
            self._build_absolute_directory(Path("src/training/train_ensemble.py")),
            self._build_absolute_directory(Path("src/utils/utils_check.py")),
            self._build_absolute_directory(Path("src/utils/utils_run.py")),
            self._build_absolute_directory(Path("src/visualization/visual.py")),
        ]


# if __name__ == "__main__":
#     ensemble_path = EnsemblePath("white_mustang", validate=True)
#     print(ensemble_path.get_directories())
#     del ensemble_path
