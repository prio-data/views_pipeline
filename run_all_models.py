import subprocess
import time


def main():
    try:
        while True:
            subprocess.run(["python3", "models/blue_sea/main.py"])
            subprocess.run(["python3", "models/yellow_duck/main.py"])
            time.sleep(2000)
    except KeyboardInterrupt:
        print("Interrupted by user. Stopping...")


if __name__ == "__main__":
    main()
