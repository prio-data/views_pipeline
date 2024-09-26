from pathlib import Path
import py_compile
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def save_script(output_file: Path, code: str) -> bool:
    """
    Compiles a Python script to a specified file and saves it.

    Parameters:
    output_file : Path
        The path to the file where the Python script will be saved. This should
        be a `Path` object pointing to the desired file location, including
        the filename and extension (e.g., 'script.py').

    code : str
        The Python code to be written to the file. This should be a string containing
        valid Python code that will be saved and compiled.

    Returns:
    bool:
        Returns `True` if the script was successfully written and compiled.
        Returns `False` if an error occurred during the file writing or compilation or if file already exists.

    Raises:
    IOError: If there is an error writing the code to the file (e.g., permission denied, invalid path).

    py_compile.PyCompileError: If there is an error compiling the Python script (e.g., syntax error in the code).
    """
    if output_file.exists():
        # while True:
        #     overwrite = (
        #         input(
        #             f"The file {output_file} already exists. Do you want to overwrite it? (y/n): "
        #         )
        #         .strip()
        #         .lower()
        #     )
        #     if overwrite in {"y", "n"}:
        #         break  # Exit the loop if the input is valid
        #     logger.info("Invalid input. Please enter 'y' for yes or 'n' for no.")

        # if overwrite == "n":
        #     logger.info("Script not saved.")
        #     return False
        logger.info(f"Script {output_file} already exists. Skipping.")
        return False

    try:
        # Write the sample code to the Python file
        with open(output_file, "w") as file:
            file.write(code)

        # Compile the newly created Python script
        py_compile.compile(output_file)  # cfile=output_file.with_suffix('.pyc')
        logger.info(f"Script saved and compiled successfully: {output_file}")
        return True
    except (IOError, py_compile.PyCompileError) as e:
        logger.exception(
            f"Failed to write or compile the deployment configuration script: {e}"
        )
        logger.exception(f"Script file: {output_file}")
        return False
