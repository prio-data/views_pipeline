from model_path import ModelPath
import logging
from pathlib import Path
from typing import Union

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


# if __name__ == "__main__":
#     ensemble_path = EnsemblePath("white_mustang", validate=True)
#     ensemble_path.view_directories()
#     ensemble_path.view_scripts()
#     print(ensemble_path.get_queryset())
#     del ensemble_path
