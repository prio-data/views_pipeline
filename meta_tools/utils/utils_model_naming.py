import re
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
import sys
# sys.path.append(str(Path(__file__).parent))

def validate_model_name(name: str) -> bool:
    """
    Validates the model name to ensure it follows the lowercase "adjective_noun" format.

    Parameters:
        name (str): The model name to validate.

    Returns:
        bool: True if the name is valid, False otherwise.
    """
    # Define a basic regex pattern for a noun_adjective format
    pattern = r"^[a-z]+_[a-z]+$"
    # Check if the name matches the pattern
    if re.match(pattern, name):
        # You might want to add further checks for actual noun and adjective validation
        # For now, this regex checks for two words separated by an underscore
        return True
    return False