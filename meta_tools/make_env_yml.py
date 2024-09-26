import argparse
import yaml
import subprocess


def get_installed_packages(env_name=None):
    if env_name is None:
        env_name = get_current_env()
    command = f"conda list -n {env_name} --explicit"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if error:
        print(f"Error: {error.decode('utf-8')}")
        return None
    else:
        output = output.decode("utf-8")
        packages = []
        for line in output.split("\n"):
            if line.startswith("#"):
                continue
            if line.strip():
                package = line.split("::")[1].split("-")[0]
                version = line.split("::")[1].split("-")[1]
                channel = line.split("::")[0]
                packages.append((package, version, channel))
        return packages


def write_requirements_txt(packages):
    with open("requirements.txt", "w") as f:
        for package, version, channel in packages:
            if channel == "pypi":
                f.write(f"{package}=={version}\n")


def get_current_env():
    command = "conda info --envs"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if error:
        print(f"Error: {error.decode('utf-8')}")
        return None
    else:
        output = output.decode("utf-8")
        for line in output.split("\n"):
            if "*" in line:
                return line.split()[0]


def write_environment_yml(packages):
    data = {"name": get_current_env(), "dependencies": []}
    for package, version, channel in packages:
        if channel == "conda-forge":
            data["dependencies"].append(f"-c conda-forge {package}={version}")
        else:
            data["dependencies"].append(f"{package}=={version}")
    with open("environment.yml", "w") as f:
        yaml.dump(data, f)


def fix_environment():
    """
    Install the missing packages in the current conda environment to match the saved requirements.
    """
    # Get the list of packages in the current conda environment
    result = subprocess.run(
        ["conda", "list", "--export"], capture_output=True, text=True
    )
    current_packages = set(result.stdout.strip().split("\n"))

    # Read the packages from the requirements.txt file
    with open("requirements.txt", "r") as f:
        required_packages = set(f.read().strip().split("\n"))

    # Check if the current packages match the required packages
    if current_packages == required_packages:
        print("The current environment matches the saved requirements.")
    else:
        print("The current environment does not match the saved requirements.")
        print("Mismatched packages:")
        for package in required_packages - current_packages:
            print(package)
        print("Installing missing packages to match the saved requirements...")
        # Install the missing packages in the current conda environment
        missing_packages = required_packages - current_packages
        subprocess.run(
            ["conda", "install", "--yes"] + list(missing_packages), check=True
        )
        print("Environment fixed successfully.")


def check_environment_match():
    """
    Check if the list of packages in the current conda environment matches the saved requirements.
    If the environments do not match, print the list of mismatched packages.
    """
    # Get the list of packages in the current conda environment
    result = subprocess.run(
        ["conda", "list", "--export"], capture_output=True, text=True
    )
    current_packages = set(result.stdout.strip().split("\n"))

    # Read the packages from the requirements.txt file
    with open("requirements.txt", "r") as f:
        required_packages = set(f.read().strip().split("\n"))

    # Check if the current packages match the required packages
    if current_packages == required_packages:
        print("The current environment matches the saved requirements.")
        return True
    else:
        print("The current environment does not match the saved requirements.")
        print("Mismatched packages:")
        for package in required_packages - current_packages:
            print(package)
        return False


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Save and check the conda environment."
    )
    parser.add_argument("-f", "--fix", action="store_true", help="fix the environment")
    args = parser.parse_args()

    # Save the environment files
    packages = get_installed_packages()
    write_environment_yml(packages)

    # Check if the environment matches the saved requirements
    # if not check_environment_match():
    #     # If the environment does not match and the --fix flag is provided, fix the environment
    #     if args.fix:
    #         fix_environment()
