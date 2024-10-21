import threading
import logging
import functools

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class GlobalCache:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(GlobalCache, cls).__new__(cls)
                    cls._instance._cache = functools.lru_cache(maxsize=1000)(dict)()
        return cls._instance

    def get(self, key):
        with self._lock:
            try:
                value = self._cache[key]
                logging.info(f"Retrieved value for key {key} from cache.")
                return value
            except KeyError:
                logging.error(f"Key {key} not found in cache.")
                return None
    
    def set(self, key, value):
        with self._lock:
            self._cache[key] = value
            logging.info(f"Set value {value} for key {key} in cache.")
            return True

    def clear(self):
        with self._lock:
            self._cache.clear()
            logging.info("Cleared cache.")
            return True