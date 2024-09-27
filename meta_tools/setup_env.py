import subprocess
import yaml
import logging
import argparse
from datetime import datetime
from utils.utils_model_paths import find_project_root

# Configure logging to display information level messages
logging.basicConfig(
    level=logging.INFO,
)

# Define the path to the environment.yml file
environment_yml_path = find_project_root() / "environment.yml"


def get_mamba_packages():
    """
    Retrieves the list of installed packages using mamba.

    Returns:
        str: A string containing the list of installed packages.
        None: If an error occurs during the subprocess call.
    """
    try:
        result = subprocess.run(
            ["mamba", "list", "--export"], capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while getting mamba packages: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def get_pip_packages():
    """
    Retrieves the list of installed packages using pip.

    Returns:
        list: A list of strings, each representing a package and its version.
        None: If an error occurs during the subprocess call.
    """
    try:
        result = subprocess.run(
            ["pip", "freeze"], capture_output=True, text=True, check=True
        )
        packages = result.stdout.splitlines()
        # Filter out packages installed from local files
        filtered_packages = [pkg for pkg in packages if "@ file:///" not in pkg]
        return filtered_packages
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while getting pip packages: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def write_requirements_files():
    """
    Writes the current mamba and pip packages to the environment.yml file.
    """
    try:
        mamba_packages = get_mamba_packages()
        pip_packages = get_pip_packages()

        # Process mamba packages to include version information and sources
        mamba_packages_list = [
            line
            for line in mamba_packages.splitlines()
            if line and not line.startswith("#")
        ]

        # Write mamba packages and pip packages to environment.yml
        with open(environment_yml_path, "w") as env_file:
            env = {
                "name": "views_pipeline_env",
                "channels": ["defaults", "conda-forge"],
                "dependencies": mamba_packages_list + [{"pip": pip_packages}],
            }
            yaml.dump(env, env_file, default_flow_style=False)

        logging.info("`environment.yml` file has been written.")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except PermissionError as e:
        logging.error(f"Permission error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


def check_environment():
    """
    Checks the current environment against the saved environment.yml file for discrepancies.

    Returns:
        list: A list of discrepancies found between the current and saved environments.
    """
    try:
        with open(environment_yml_path, "r") as env_file:
            saved_env = yaml.safe_load(env_file)
            saved_mamba_packages = saved_env["dependencies"]
    except FileNotFoundError:
        logging.error(
            "`environment.yml` file not found. Run with --write flag to create them."
        )
        return
    except yaml.YAMLError as e:
        logging.error(f"Error parsing `environment.yml`: {e}")
        return
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return

    try:
        current_pip_packages = get_pip_packages()
        current_mamba_packages = get_mamba_packages().splitlines()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error retrieving current packages: {e}")
        return
    except Exception as e:
        logging.error(
            f"An unexpected error occurred while retrieving current packages: {e}"
        )
        return

    discrepancies = []

    try:
        # Create sets of package names for intersection
        saved_pip_set = {
            pkg.split("==")[0]
            for pkg in saved_mamba_packages
            if isinstance(pkg, dict) and "pip" in pkg
            for pkg in pkg["pip"]
        }
        current_pip_set = {pkg.split("==")[0] for pkg in current_pip_packages}
        saved_mamba_set = {
            pkg.split("=")[0]
            for pkg in saved_mamba_packages
            if not isinstance(pkg, dict)
        }
        current_mamba_set = {pkg.split("=")[0] for pkg in current_mamba_packages}

        # Find intersections
        pip_intersection = saved_pip_set & current_pip_set
        mamba_intersection = saved_mamba_set & current_mamba_set

        # Check for pip package discrepancies
        for pip_package in pip_intersection:
            saved_version = next(
                pkg.split("==")[1]
                for pkg in saved_mamba_packages
                if isinstance(pkg, dict) and "pip" in pkg
                for pkg in pkg["pip"]
                if pkg.startswith(pip_package)
            )
            current_version = next(
                pkg.split("==")[1]
                for pkg in current_pip_packages
                if pkg.startswith(pip_package)
            )
            if saved_version != current_version:
                discrepancies.append(
                    f"Version mismatch for pip package: {pip_package} (saved: {saved_version}, current: {current_version})"
                )

        # Check for mamba package discrepancies
        for mamba_package in mamba_intersection:
            saved_version = next(
                pkg.split("=")[1]
                for pkg in saved_mamba_packages
                if pkg.startswith(mamba_package)
            )
            current_version = next(
                pkg.split("=")[1]
                for pkg in current_mamba_packages
                if pkg.startswith(mamba_package)
            )
            if saved_version != current_version:
                discrepancies.append(
                    f"Version mismatch for mamba package: {mamba_package} (saved: {saved_version}, current: {current_version})"
                )

        # Check for missing packages
        missing_pip_packages = saved_pip_set - current_pip_set
        missing_mamba_packages = saved_mamba_set - current_mamba_set

        for pip_package in missing_pip_packages:
            saved_version = next(
                pkg.split("==")[1]
                for pkg in saved_mamba_packages
                if isinstance(pkg, dict) and "pip" in pkg
                for pkg in pkg["pip"]
                if pkg.startswith(pip_package)
            )
            discrepancies.append(f"Missing pip package: {pip_package}=={saved_version}")

        for mamba_package in missing_mamba_packages:
            saved_version = next(
                pkg.split("=")[1]
                for pkg in saved_mamba_packages
                if pkg.startswith(mamba_package)
            )
            discrepancies.append(
                f"Missing mamba package: {mamba_package}={saved_version}"
            )

        if discrepancies:
            logging.warning("Discrepancies found:")
            for discrepancy in discrepancies:
                logging.warning(discrepancy)
        else:
            logging.info("The current environment matches the saved requirements.")

    except Exception as e:
        logging.error(f"An unexpected error occurred during the environment check: {e}")

    return discrepancies


def install_package(package, manager):
    """
    Installs a package using the specified package manager.

    Args:
        package (str): The name of the package to install.
        manager (str): The package manager to use ('pip' or 'mamba').
    """
    try:
        if manager == "pip":
            subprocess.run(["pip", "install", package], check=True)
        elif manager == "mamba":
            subprocess.run(["mamba", "install", package, "-y"], check=True)
        logging.info(f"Successfully installed {package} using {manager}.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install {package} using {manager}. Error: {e}")


def uninstall_package(package, manager):
    """
    Uninstalls a package using the specified package manager.

    Args:
        package (str): The name of the package to uninstall.
        manager (str): The package manager to use ('pip' or 'mamba').
    """
    try:
        if manager == "pip":
            subprocess.run(["pip", "uninstall", "-y", package], check=True)
        elif manager == "mamba":
            subprocess.run(["mamba", "remove", package, "-y"], check=True)
        logging.info(f"Successfully uninstalled {package} using {manager}.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to uninstall {package} using {manager}. Error: {e}")


# DOES NOT WORK. BUILDING A NEW ENVIRONMENT FROM SCRATCH IS THE BEST OPTION.
# Suggestions: Write a shell script to create a new environment from scratch and account for os and architecture.
def fix_environment(prune=False):
    """
    Fixes the current environment to match the `environment.yml` file.

    This function compares the current pip and mamba packages with those specified
    in the `environment.yml` file. It installs missing packages, updates mismatched
    versions, and optionally prunes unnecessary packages.

    Args:
        prune (bool): If True, removes packages not specified in the `environment.yml` file.

    Raises:
        FileNotFoundError: If the `environment.yml` file is not found.
    """
    logging.warning(
        "Very experimental. Fixing the environment may cause issues. Proceed with caution. See 'https://github.com/prio-data/ViEWS_organization/blob/main/The%20Views%20Environment/Setting%20up.MD'"
    )
    discrepancies = check_environment()
    if not discrepancies:
        logging.info("No discrepancies found. Environment is already up to date.")
        return

    for discrepancy in discrepancies:
        if "Version mismatch for pip package" in discrepancy:
            package = discrepancy.split(": ")[1].split(" ")[0]
            saved_version = discrepancy.split("(saved: ")[1].split(",")[0]
            install_package(f"{package}=={saved_version}", "pip")
        elif "Version mismatch for mamba package" in discrepancy:
            package = discrepancy.split(": ")[1].split(" ")[0]
            saved_version = discrepancy.split("(saved: ")[1].split(",")[0]
            install_package(f"{package}={saved_version}", "mamba")
        elif "Missing pip package" in discrepancy:
            package = discrepancy.split(": ")[1]
            install_package(package, "pip")
        elif "Missing mamba package" in discrepancy:
            package = discrepancy.split(": ")[1]
            install_package(package, "mamba")

    if prune:
        saved_env = yaml.safe_load(open(environment_yml_path, "r"))
        saved_pip_set = {
            pkg.split("==")[0]
            for pkg in saved_env["dependencies"]
            if isinstance(pkg, dict) and "pip" in pkg
            for pkg in pkg["pip"]
        }
        current_pip_set = {pkg.split("==")[0] for pkg in get_pip_packages()}
        saved_mamba_set = {
            pkg.split("=")[0]
            for pkg in saved_env["dependencies"]
            if not isinstance(pkg, dict)
        }
        current_mamba_set = {
            pkg.split("=")[0] for pkg in get_mamba_packages().splitlines()
        }

        for package in current_pip_set - saved_pip_set:
            uninstall_package(package, "pip")

        for package in current_mamba_set - saved_mamba_set:
            uninstall_package(package, "mamba")

    discrepancies = check_environment()
    if not discrepancies:
        logging.info("Environment has been fixed.")
    else:
        logging.error("Errors occurred while fixing the environment:")
        for discrepancy in discrepancies:
            logging.error(discrepancy)


def main():
    """
    Main function to parse command-line arguments and execute the appropriate actions.

    This function supports checking the environment, fixing the environment, pruning
    unnecessary packages, and writing the current environment to `environment.yml`.
    """
    parser = argparse.ArgumentParser(
        description="Check and fix Mamba/Conda environment."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if the environment matches the `environment.yml` file.",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Fix the environment to match the `environment.yml` file.",
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Remove packages not specified in the `environment.yml` file.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the current environment to `environment.yml`.",
    )
    args = parser.parse_args()

    # Ensure that at least one action is specified
    if not (args.check or args.fix or args.write):
        parser.error("Invalid input, add --check, --fix, or --write.")

    if args.check:
        check_environment()

    if args.fix:
        fix_environment(prune=args.prune)

    if args.write:
        write_requirements_files()


if __name__ == "__main__":
    main()
