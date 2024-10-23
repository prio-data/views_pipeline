from model_path import ModelPath
import sys
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class EnsemblePath(ModelPath):
    def __init__(self, model_name_or_path, validate=True, force_cache_overwrite=False) -> None:
        self._target = "ensemble"
        super().__init__(model_name_or_path, validate, target="ensemble", force_cache_overwrite=force_cache_overwrite)

# if __name__ == "__main__":
#     model = EnsemblePath("white_mustang", validate=True)
#     print(model.model_dir)
#     del model