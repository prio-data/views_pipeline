import pickle
import os
import logging
import sys
from pathlib import Path
import threading
import atexit
import signal
from views_pipeline.managers.path_manager import ModelPath
PATH = Path(__file__)
if 'views_pipeline' in PATH.parts:
    PATH_ROOT = Path(*PATH.parts[:PATH.parts.index('views_pipeline') + 1])
    sys.path.insert(0, str(PATH_ROOT))
else:
    raise ValueError("The 'views_pipeline' directory was not found in the provided path.")

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class GlobalCacheMeta(type):
    def __getitem__(cls, key):
        instance = cls()
        return instance[key]

    def __setitem__(cls, key, value):
        instance = cls()
        instance[key] = value

    def delete(cls, key):
        instance = cls()
        instance._delete(key)

class GlobalCache(metaclass=GlobalCacheMeta):
    """
    A thread-safe singleton cache class that uses a global cache file to store key-value pairs.

    Attributes:
        _instance (GlobalCache): The singleton instance of the GlobalCache class.
        _lock (threading.Lock): A lock to ensure thread safety.
        filepath (Path): The path to the cache file.
        cache (dict): The in-memory cache dictionary.
        initialized (bool): A flag to check if the instance is initialized.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """
        Ensures that only one instance of the GlobalCache class is created (singleton pattern).

        Uses double-checked locking to minimize the overhead of acquiring the lock.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(GlobalCache, cls).__new__(cls)
        return cls._instance

    def __init__(self, filepath=None):
        """
        Initializes the GlobalCache instance.

        Args:
            filepath (Path, optional): The path to the cache file. Defaults to '.global_cache.pkl' in the project root.
        """
        if not hasattr(self, "initialized"):
            self.local_imports()
            if filepath is None:
                filepath = (
                    ModelPath.find_project_root() / ".global_cache.pkl"
                )
            self.filepath = filepath
            self.cache = {}
            self.ensure_cache_file_exists()
            self.load_cache()
            self.initialized = True

    def __getitem__(self, key):
        """
        Retrieves a value from the cache by key.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            The value associated with the key, or None if the key is not found.
        """
        with self._lock:
            return self.get(key)

    def __setitem__(self, key, value):
        """
        Sets a value in the cache for a given key.

        Args:
            key (str): The key to set the value for.
            value: The value to set.
        """
        with self._lock:
            self.set(key, value)

    def local_imports(self):
        from meta_tools.utils import utils_model_paths  # To avoid circular dependency

        self.utils_model_paths = utils_model_paths

    def ensure_cache_file_exists(self):
        """
        Ensures that the cache file exists. If it does not exist, creates a new cache file.
        """
        if not self.filepath.exists():
            logging.warning(
                f"Cache file: {self.filepath} does not exist. Creating new cache file..."
            )
            with open(self.filepath, "wb") as f:
                pickle.dump({}, f)
            logging.debug(f"Created new cache file: {self.filepath}")

    def set(self, key, value):
        """
        Sets a value in the in-memory cache and saves the cache to the file.

        Args:
            key (str): The key to set the value for.
            value: The value to set.
        """
        self.cache[key] = value
        self.save_cache()
        logging.debug(f"Set key: {key} with value: {value}")

    def get(self, key):
        """
        Retrieves a value from the in-memory cache by key.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            The value associated with the key, or None if the key is not found.
        """
        self.load_cache()
        value = self.cache.get(key, None)
        logging.debug(f"Get key: {key} returned value: {value}")
        return value

    def _delete(self, key):
        """
        Deletes a key-value pair from the in-memory cache and saves the cache to the file.
        
        Args:
            key (str): The key to delete.
        """
        if key in self.cache:
            del self.cache[key]
            self.save_cache()
            logging.debug(f'Deleted key: {key}')
        else:
            logging.warning(f'Key: {key} not found in cache')

    def save_cache(self):
        """
        Saves the in-memory cache to the cache file.
        """
        with open(self.filepath, "wb") as f:
            pickle.dump(self.cache, f)
        logging.debug(f"Cache saved to file: {self.filepath}")

    def load_cache(self):
        """
        Loads the cache from the cache file into the in-memory cache.
        """
        if self.filepath.exists():
            try:
                with open(str(self.filepath), "rb") as f:
                    loaded_cache = pickle.loads(f.read())
                    if isinstance(loaded_cache, dict):
                        self.cache = loaded_cache
                        logging.debug(f"Cache loaded from file: {self.filepath}")
                    else:
                        logging.error(
                            f"Loaded cache is not a dictionary. Initializing empty cache."
                        )
                        self.cache = {}
            except (EOFError, pickle.UnpicklingError) as e:
                logging.error(
                    f"Failed to load cache from file: {self.filepath}. Error: {e}"
                )
                self.cache = {}
        else:
            self.cache = {}
            logging.debug(f"Cache file does not exist. Initialized empty cache.")


def cleanup_cache_file():
    """
    Deletes the global cache file upon program termination.

    This function is registered with the atexit module to ensure that the
    global cache file is deleted when the program exits normally. It acquires
    the lock to ensure thread safety and then checks if the cache file exists.
    If the file exists, it deletes the file and logs the action.
    """
    try:
        # Acquire the lock to ensure thread safety
        with GlobalCache._lock:
            if os.path.exists(GlobalCache().filepath):
                os.remove(GlobalCache().filepath)
                logging.info(f"Cache file: {GlobalCache().filepath} deleted at exit")
    except Exception as e:
        logging.error(f"Error during cleanup: {e}")


def signal_handler(sig, frame):
    """
    Signal handler for SIGINT to delete the cache file upon user interruption.

    Args:
        sig (int): The signal number.
        frame (FrameType): The current stack frame.
    """
    logging.info("SIGINT received. Deleting cache file...")
    cleanup_cache_file()
    os._exit(0)  # Use os._exit to ensure the process exits immediately


# Register the cleanup_cache_file function to be called upon normal program termination
atexit.register(cleanup_cache_file)

# Register the signal handler for SIGINT
signal.signal(signal.SIGINT, signal_handler)


# if __name__ == '__main__':
#     # Example usage of the GlobalCache class
#     print(GlobalCache["test"]) # Returns None

#     GlobalCache["test"] = "Hello, World!"
#     print(GlobalCache["test"])
#     GlobalCache.delete("test")

#     print(GlobalCache["test"]) # Returns None

