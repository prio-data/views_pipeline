import pytest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from global_cache import GlobalCache, cleanup_cache_file

@pytest.fixture(scope="function")
def cache_file(tmp_path):
    """
    Fixture to create a temporary cache file for testing.
    """
    cache_file = tmp_path / ".global_cache.pkl"
    yield cache_file
    if cache_file.exists():
        cache_file.unlink()

@pytest.fixture(scope="function")
def global_cache(cache_file):
    """
    Fixture to create a GlobalCache instance with a temporary cache file.
    """
    cache = GlobalCache(filepath=cache_file)
    yield cache
    if cache_file.exists():
        cache_file.unlink()

def test_singleton_pattern(global_cache):
    """
    Test that only one instance of GlobalCache is created (singleton pattern).
    """
    cache1 = global_cache
    cache2 = GlobalCache()
    assert cache1 is cache2, "GlobalCache is not a singleton"

def test_set_and_get(global_cache):
    """
    Test setting and getting values in the cache.
    """
    global_cache["key1"] = "value1"
    assert global_cache["key1"] == "value1", "Failed to get the correct value from the cache"

def test_delete_key(global_cache):
    """
    Test deleting a key from the cache.
    """
    global_cache["key1"] = "value1"
    global_cache.delete("key1")
    assert global_cache["key1"] is None, "Failed to delete the key from the cache"

def test_cleanup_cache_file(global_cache, cache_file):
    """
    Test the cleanup function to ensure the cache file is deleted upon program termination.
    """
    global_cache["key1"] = "value1"
    assert global_cache.filepath.exists() == True
    
    # Call the cleanup function
    cleanup_cache_file()
    assert global_cache.filepath.exists() == False

