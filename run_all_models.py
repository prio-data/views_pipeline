# from models.blue_sea import main as zero_baseline_model
# from models.yellow_duck import main as no_change_baseline_model

# def main():
#     zero_baseline_model.main()
#     no_change_baseline_model.main()


# if __name__ == "__main__":
#     main()

import subprocess


def main():
    subprocess.run(["python3", "models/blue_sea/main.py"])
    subprocess.run(["python3", "models/yellow_duck/main.py"])


if __name__ == "__main__":
    main()
