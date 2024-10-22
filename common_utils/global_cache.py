import pickle
import os
import logging
import sys
from pathlib import Path
import threading
import atexit
sys.path.append(str(Path(__file__).parent.parent))
from meta_tools.utils import utils_model_paths

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class GlobalCache:
    """
    A thread-safe singleton cache class that uses a global cache file to store key-value pairs.
    
    Attributes:
        _instance (GlobalCache): The singleton instance of the GlobalCache class.
        _lock (threading.Lock): A lock to ensure thread safety.
        filename (Path): The path to the cache file.
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
                if cls._instance is None:  # Double-checked locking.
                    # Reasoning: Ensure that only one thread can create the instance in multithreaded environments to prevent race conditions.
                    cls._instance = super(GlobalCache, cls).__new__(cls)
        return cls._instance

    def __init__(self, filename=utils_model_paths.find_project_root() / '.global_cache.pkl'):
        """
        Initializes the GlobalCache instance.
        
        Args:
            filename (Path, optional): The path to the cache file. Defaults to '.global_cache.pkl' in the project root.
        """
        if not hasattr(self, 'initialized'):
            self.filename = filename
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

    def ensure_cache_file_exists(self):
        """
        Ensures that the cache file exists. If it does not exist, creates a new cache file.
        """
        if not os.path.exists(self.filename):
            logging.info(f'Cache file: {self.filename} does not exist. Creating new cache file...')
            with open(self.filename, 'wb') as f:
                pickle.dump({}, f)
            logging.info(f'Created new cache file: {self.filename}')

    def set(self, key, value):
        """
        Sets a value in the in-memory cache and saves the cache to the file.
        
        Args:
            key (str): The key to set the value for.
            value: The value to set.
        """
        self.cache[key] = value
        self.save_cache()
        logging.debug(f'Set key: {key} with value: {value}')

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
        logging.debug(f'Get key: {key} returned value: {value}')
        return value

    def delete(self, key):
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
        with open(self.filename, 'wb') as f:
            pickle.dump(self.cache, f)
        logging.info(f'Cache saved to file: {self.filename}')

    def load_cache(self):
        """
        Loads the cache from the cache file into the in-memory cache.
        """
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                self.cache = pickle.load(f)
            logging.info(f'Cache loaded from file: {self.filename}')
        else:
            logging.warning(f'Cache file: {self.filename} does not exist')

    def delete_cache_file(self):
        """
        Deletes the cache file from the filesystem.
        """
        if os.path.exists(self.filename):
            os.remove(self.filename)
            logging.info(f'Cache file: {self.filename} deleted')
        else:
            logging.warning(f'Cache file: {self.filename} does not exist')

def cleanup_cache_file():
    """
    Deletes the global cache file upon program termination.

    This function is registered with the atexit module to ensure that the
    global cache file is deleted when the program exits normally. It acquires
    the lock to ensure thread safety and then checks if the cache file exists.
    If the file exists, it deletes the file and logs the action.
    """
    # Acquire the lock to ensure thread safety
    with GlobalCache._lock:
        # Check if the cache file exists
        if os.path.exists(GlobalCache().filename):
            # Delete the cache file
            os.remove(GlobalCache().filename)
            # Log the deletion of the cache file
            logging.info(f'Cache file: {GlobalCache().filename} deleted at exit')

# Register the cleanup_cache_file function to be called upon normal program termination
atexit.register(cleanup_cache_file)