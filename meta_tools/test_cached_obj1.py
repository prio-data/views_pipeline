# test_script1.py
import logging
from model_path_manager import ModelPathManager

logging.basicConfig(level=logging.INFO)

def main():
    model_name = "purple_alien"
    path_manager = ModelPathManager(model_name=model_name)
    print(f"[Script 1] Model directory: {path_manager.model_dir}")

if __name__ == "__main__":
    main()
