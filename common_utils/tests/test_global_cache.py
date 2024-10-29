import pytest
from pathlib import Path
import sys
import os
import signal
from unittest.mock import patch

PATH = Path(__file__)
if 'views_pipeline' in PATH.parts:
    PATH_ROOT = Path(*PATH.parts[:PATH.parts.index('views_pipeline') + 1])
    PATH_COMMON_UTILS = PATH_ROOT / 'common_utils'
    if not PATH_COMMON_UTILS.exists():
        raise ValueError("The 'common_utils' directory was not found in the provided path.")
    sys.path.insert(0, str(PATH_COMMON_UTILS))
else:
    raise ValueError("The 'views_pipeline' directory was not found in the provided path.")
 
from global_cache import GlobalCache, cleanup_cache_file, signal_handler

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
    global_cache._delete("key1")
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

@patch("os._exit")
def test_signal_handler(mock_exit, global_cache, cache_file):
    """
    Test the signal handler to ensure the cache file is deleted upon user interruption.
    """
    global_cache["key1"] = "value1"
    assert global_cache.filepath.exists() == True
    
    # Send a SIGINT signal to the current process
    os.kill(os.getpid(), signal.SIGINT)
    
    # Verify that the cache file is deleted
    assert not global_cache.filepath.exists(), "Cache file was not deleted by the signal handler"
    mock_exit.assert_called_once_with(0)