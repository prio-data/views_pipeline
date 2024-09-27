import subprocess
import yaml
import logging
import argparse
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_mamba_packages():
    result = subprocess.run(
        ["mamba", "list", "--export"], capture_output=True, text=True
    )
    return result.stdout


def get_pip_packages():
    result = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
    packages = result.stdout.splitlines()
    filtered_packages = [pkg for pkg in packages if "@ file:///" not in pkg]
    return filtered_packages


def write_requirements_files():
    mamba_packages = get_mamba_packages()
    pip_packages = get_pip_packages()

    # Write pip packages to requirements.txt
    with open("requirements.txt", "w") as req_file:
        req_file.write("\n".join(pip_packages))

    # Process mamba packages to include version information and sources
    mamba_packages_list = [
        line
        for line in mamba_packages.splitlines()
        if line and not line.startswith("#")
    ]

    # Write mamba packages and pip packages to environment.yml
    with open("environment.yml", "w") as env_file:
        env = {
            "name": "current_env",
            "channels": ["defaults", "conda-forge"],
            "dependencies": mamba_packages_list + [{"pip": pip_packages}],
        }
        yaml.dump(env, env_file, default_flow_style=False)

    logging.info("requirements.txt and environment.yml files have been written.")


def check_environment():
    try:
        with open("requirements.txt", "r") as req_file:
            saved_pip_packages = req_file.read().splitlines()

        with open("environment.yml", "r") as env_file:
            saved_env = yaml.safe_load(env_file)
            saved_mamba_packages = saved_env["dependencies"]
    except FileNotFoundError:
        logging.error(
            "requirements.txt and/or environment.yml files not found. Run with --write flag to create them."
        )
        return

    current_pip_packages = get_pip_packages()
    current_mamba_packages = get_mamba_packages().splitlines()

    discrepancies = []

    for package in saved_pip_packages:
        if package not in current_pip_packages:
            discrepancies.append(f"Missing pip package: {package}")
        else:
            saved_version = package.split("==")[1]
            current_version = next(
                (
                    pkg.split("==")[1]
                    for pkg in current_pip_packages
                    if pkg.startswith(package.split("==")[0])
                ),
                None,
            )
            if saved_version != current_version:
                discrepancies.append(
                    f"Version mismatch for pip package: {package.split('==')[0]} (saved: {saved_version}, current: {current_version})"
                )

    for package in saved_mamba_packages:
        if isinstance(package, dict) and "pip" in package:
            for pip_package in package["pip"]:
                if pip_package not in current_pip_packages:
                    discrepancies.append(f"Missing pip package: {pip_package}")
                else:
                    saved_version = pip_package.split("==")[1]
                    current_version = next(
                        (
                            pkg.split("==")[1]
                            for pkg in current_pip_packages
                            if pkg.startswith(pip_package.split("==")[0])
                        ),
                        None,
                    )
                    if saved_version != current_version:
                        discrepancies.append(
                            f"Version mismatch for pip package: {pip_package.split('==')[0]} (saved: {saved_version}, current: {current_version})"
                        )
        elif package not in current_mamba_packages:
            discrepancies.append(f"Missing mamba package: {package}")
        else:
            saved_version = package.split("=")[1]
            current_version = next(
                (
                    pkg.split("=")[1]
                    for pkg in current_mamba_packages
                    if pkg.startswith(package.split("=")[0])
                ),
                None,
            )
            if saved_version != current_version:
                discrepancies.append(
                    f"Version mismatch for mamba package: {package.split('=')[0]} (saved: {saved_version}, current: {current_version})"
                )

    if discrepancies:
        logging.warning("Discrepancies found:")
        for discrepancy in discrepancies:
            logging.warning(discrepancy)
    else:
        logging.info("The current environment matches the saved requirements.")

    return discrepancies


def fix_environment(discrepancies):
    for discrepancy in discrepancies:
        if "pip package" in discrepancy:
            package = discrepancy.split(": ")[1]
            subprocess.run(["pip", "install", package])
        elif "mamba package" in discrepancy:
            package = discrepancy.split(": ")[1]
            subprocess.run(["mamba", "install", package, "-y"])

    logging.info("Environment has been fixed.")


def main():
    parser = argparse.ArgumentParser(description="Check and fix Mamba environment.")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Fix the environment if discrepancies are found.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the current environment to requirements.txt and environment.yml.",
    )
    args = parser.parse_args()

    check_environment()

    if args.fix:
        discrepancies = check_environment()
        if discrepancies:
            fix_environment(discrepancies)

    if args.write:
        write_requirements_files()
        check_environment()


if __name__ == "__main__":
    main()
