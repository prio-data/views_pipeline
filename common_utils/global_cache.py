import pickle
import os
import logging
import sys
from pathlib import Path
import threading
sys.path.append(str(Path(__file__).parent.parent))
from meta_tools.utils import utils_model_paths

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GlobalCache:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking.
                    # Reasoning: Ensure that only one thread can create the instance in multithreaded environments to prevent race conditions.
                    cls._instance = super(GlobalCache, cls).__new__(cls)
        return cls._instance

    def __init__(self, filename=utils_model_paths.find_project_root() / '.global_cache.pkl'):
        if not hasattr(self, 'initialized'):
            self.filename = filename
            self.cache = {}
            self.ensure_cache_file_exists()
            self.load_cache()
            self.initialized = True

    def __getitem__(self, key):
        with self._lock:
            return self.get(key)

    def __setitem__(self, key, value):
        with self._lock:
            self.set(key, value)

    # DO NOT USE THREAD LOCKS IN THESE METHODS. WILL CAUSE DEADLOCKS!
    def ensure_cache_file_exists(self):
        if not os.path.exists(self.filename):
            logging.info(f'Cache file: {self.filename} does not exist. Creating new cache file...')
            with open(self.filename, 'wb') as f:
                pickle.dump({}, f)
                f.close()
                logging.info(f'Created new cache file: {self.filename}')

    def set(self, key, value):
        self.cache[key] = value
        self.save_cache()
        logging.info(f'Set key: {key} with value: {value}')

    def get(self, key):
        self.load_cache()
        value = self.cache.get(key, None)
        logging.info(f'Get key: {key} returned value: {value}')
        return value

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]
            self.save_cache()
            logging.info(f'Deleted key: {key}')
        else:
            logging.info(f'Key: {key} not found in cache')

    def save_cache(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.cache, f)
            f.close()
        logging.info(f'Cache saved to file: {self.filename}')

    def load_cache(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                self.cache = pickle.load(f)
                f.close()
            logging.info(f'Cache loaded from file: {self.filename}')
        else:
            logging.info(f'Cache file: {self.filename} does not exist')

    def delete_cache_file(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
            logging.info(f'Cache file: {self.filename} deleted')
        else:
            logging.info(f'Cache file: {self.filename} does not exist')

# Example usage
# if __name__ == "__main__":
#     cache = GlobalCache()
#     cache.set('key1', 'value1')
#     print(cache.get('key1'))  # Output: value1
#     cache.delete('key1')
#     print(cache.get('key1'))  # Output: None
#     cache.delete_cache_file()

#     # New usage example
#     try:
#         model_name = 'example_model'
#         if not GlobalCache()[model_name]:
#             GlobalCache()[model_name] = 'model_instance'
#             logging.info(f"Model {model_name} added to cache.")
#     except Exception as e:
#         logging.error(f"Error adding model {model_name} to cache: {e}")