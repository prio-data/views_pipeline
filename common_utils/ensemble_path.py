from model_path import ModelPath
import sys
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class EnsemblePath(ModelPath):
    def __init__(self, model_name_or_path, validate=True) -> None:
        self._target = "ensemble"
        super().__init__(model_name_or_path, validate, target="ensemble")
    

if __name__ == "__main__":

    purple_alien = EnsemblePath(model_name_or_path="/Users/dylanpinheiro/Desktop/views_pipeline/ensembles/cruel_summer/configs", validate=True)
    print("\n", purple_alien.get_directories(), "\n")
    print(purple_alien.get_scripts(), "\n")
    print(purple_alien.dataloaders)

    print(sys.path, "\n")
    purple_alien.add_paths_to_sys()
    print(sys.path, "\n")

    # # print(sys.path, "\n")
    # purple_alien.add_paths_to_sys()
    # print(sys.path, "\n")

    # orange_pasta = ModelPath(model_name_or_path="/Users/dylanpinheiro/Desktop/views_pipeline/models/orange_pasta/reports/papers", validate=True)
    # orange_pasta.add_paths_to_sys()

    # purple_alien.remove_paths_from_sys()
    # print(sys.path, "\n")

    # orange_pasta.add_paths_to_sys()
    # print(sys.path, "\n")

    # print(purple_alien.view_directories(), "\n")
    # print(purple_alien.view_scripts(), "\n")
