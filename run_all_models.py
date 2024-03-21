import subprocess
import time


def main():
    while True:
        subprocess.run(["python3", "models/blue_sea/main.py"])
        subprocess.run(["python3", "models/yellow_duck/main.py"])
        time.sleep(20)  # Pause for 300 seconds (5 minutes)


if __name__ == "__main__":
    main()
