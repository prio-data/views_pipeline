import subprocess
import logging
import argparse
import yaml
from utils.utils_model_paths import find_project_root

# Configure logging to display information level messages
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define the path to the environment.yml file
environment_yml_path = find_project_root() / "environment.yml"


def get_mamba_packages():
    try:
        result = subprocess.run(
            ["mamba", "list", "--export"], capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while getting mamba packages: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None


def get_pip_packages():
    try:
        result = subprocess.run(
            ["pip", "freeze"], capture_output=True, text=True, check=True
        )
        packages = result.stdout.splitlines()
        filtered_packages = [pkg for pkg in packages if "@" not in pkg and "==" in pkg]
        return filtered_packages
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while getting pip packages: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None


def write_requirements_files():
    try:
        mamba_packages = get_mamba_packages()
        pip_packages = get_pip_packages()

        mamba_packages_list = [
            line for line in mamba_packages.splitlines() if line and not line.startswith("#")
        ]

        with open(environment_yml_path, "w") as env_file:
            env_file.write("name: myenv\n")
            env_file.write("dependencies:\n")
            for pkg in mamba_packages_list:
                env_file.write(f"  - {pkg}\n")
            env_file.write("  - pip:\n")
            for pkg in pip_packages:
                env_file.write(f"    - {pkg}\n")

        logging.info("`environment.yml` file has been written.")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except PermissionError as e:
        logging.error(f"Permission error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


def check_environment():
    try:
        with open(environment_yml_path, "r") as env_file:
            saved_env = yaml.safe_load(env_file)
            saved_mamba_packages = [
                pkg for pkg in saved_env["dependencies"] if not isinstance(pkg, dict)
            ]
            saved_pip_packages = [
                pkg for pkg in saved_env["dependencies"] if isinstance(pkg, dict) and "pip" in pkg
            ][0]["pip"]
    except FileNotFoundError:
        logging.error("`environment.yml` file not found. Run with --write flag to create it.")
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
        logging.error(f"An unexpected error occurred while retrieving current packages: {e}")
        return

    discrepancies = []

    saved_pip_set = {pkg.split("==")[0] for pkg in saved_pip_packages}
    current_pip_set = {pkg.split("==")[0] for pkg in current_pip_packages}
    saved_mamba_set = {pkg.split("=")[0] for pkg in saved_mamba_packages}
    current_mamba_set = {pkg.split("=")[0] for pkg in current_mamba_packages}

    pip_intersection = saved_pip_set & current_pip_set
    mamba_intersection = saved_mamba_set & current_mamba_set

    for pip_package in pip_intersection:
        saved_version = next(
            (pkg.split("==")[1] for pkg in saved_pip_packages if pkg.startswith(pip_package) and "==" in pkg),
            None
        )
        current_version = next(
            (pkg.split("==")[1] for pkg in current_pip_packages if pkg.startswith(pip_package) and "==" in pkg),
            None
        )
        if saved_version is None or current_version is None:
            logging.error(f"Error parsing version for pip package: {pip_package}")
            continue
        if saved_version != current_version:
            discrepancies.append(
                f"Version mismatch for pip package: {pip_package} (saved: {saved_version}, current: {current_version})"
            )

    for mamba_package in mamba_intersection:
        saved_version = next(
            (pkg.split("=")[1] for pkg in saved_mamba_packages if pkg.startswith(mamba_package) and "=" in pkg),
            None
        )
        current_version = next(
            (pkg.split("=")[1] for pkg in current_mamba_packages if pkg.startswith(mamba_package) and "=" in pkg),
            None
        )
        if saved_version is None or current_version is None:
            logging.error(f"Error parsing version for mamba package: {mamba_package}")
            continue
        if saved_version != current_version:
            discrepancies.append(
                f"Version mismatch for mamba package: {mamba_package} (saved: {saved_version}, current: {current_version})"
            )

    missing_pip_packages = saved_pip_set - current_pip_set
    missing_mamba_packages = saved_mamba_set - current_mamba_set

    for pip_package in missing_pip_packages:
        saved_version = next(
            (pkg.split("==")[1] for pkg in saved_pip_packages if pkg.startswith(pip_package) and "==" in pkg),
            None
        )
        if saved_version is None:
            logging.error(f"Error parsing version for missing pip package: {pip_package}")
            continue
        discrepancies.append(f"Missing pip package: {pip_package}=={saved_version}")

    for mamba_package in missing_mamba_packages:
        saved_version = next(
            (pkg.split("=")[1] for pkg in saved_mamba_packages if pkg.startswith(mamba_package) and "=" in pkg),
            None
        )
        if saved_version is None:
            logging.error(f"Error parsing version for missing mamba package: {mamba_package}")
            continue
        discrepancies.append(f"Missing mamba package: {mamba_package}={saved_version}")

    if discrepancies:
        logging.info("Discrepancies found:")
        for discrepancy in discrepancies:
            logging.info(discrepancy)
    else:
        logging.info("No discrepancies found. Environment is up to date.")

    return discrepancies


def install_package(package, manager):
    try:
        if manager == "pip":
            subprocess.run(["pip", "install", package], check=True)
        elif manager == "mamba":
            subprocess.run(["mamba", "install", "-y", package], check=True)
        logging.info(f"Successfully installed {package} using {manager}.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install {package} using {manager}. Error: {e}")


def uninstall_package(package, manager):
    try:
        if manager == "pip":
            subprocess.run(["pip", "uninstall", "-y", package], check=True)
        elif manager == "mamba":
            subprocess.run(["mamba", "remove", "-y", package], check=True)
        logging.info(f"Successfully uninstalled {package} using {manager}.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to uninstall {package} using {manager}. Error: {e}")


def fix_environment(prune=False):
    logging.warning(
        "Very experimental. Fixing the environment may cause issues. Proceed with caution."
    )
    response = input("Are you sure you want to proceed? (y/n): ")
    if response.lower() != "y":
        logging.info("Exiting without making changes.")
        return

    discrepancies = check_environment()
    if not discrepancies:
        logging.info("No discrepancies found. Environment is already up to date.")
        return

    for discrepancy in discrepancies:
        if "Version mismatch for pip package" in discrepancy:
            package = discrepancy.split(":")[1].split("(")[0].strip()
            install_package(package, "pip")
        elif "Version mismatch for mamba package" in discrepancy:
            package = discrepancy.split(":")[1].split("(")[0].strip()
            install_package(package, "mamba")
        elif "Missing pip package" in discrepancy:
            package = discrepancy.split(":")[1].strip()
            install_package(package, "pip")
        elif "Missing mamba package" in discrepancy:
            package = discrepancy.split(":")[1].strip()
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
        logging.info("Environment fixed successfully.")
    else:
        logging.error("Failed to fix some discrepancies.")


def main():
    parser = argparse.ArgumentParser(
        description="Check if current Mamba/Conda environment matches the project's environment.yml."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if the environment matches the `environment.yml` file.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the current environment to `environment.yml`.",
    )
    args = parser.parse_args()

    if not (args.check or args.write):
        parser.error("No action requested, add --check or --write")

    if args.check:
        check_environment()

    if args.write:
        write_requirements_files()


if __name__ == "__main__":
    main()