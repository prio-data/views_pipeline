import subprocess
import time


def main():
    try:
        while True:
            subprocess.run(["python3", "models/blue_sea/main.py"])
            subprocess.run(["python3", "models/yellow_duck/main.py"])
            for _ in range(20):
                print(f'waiting for next run - time remaining: {20 - _} seconds . . . \n', end='', flush=True)
                time.sleep(1)
            print()  # Move to the next line before the next iteration
    except KeyboardInterrupt:
        print("\nInterrupted by user. Stopping...")


if __name__ == "__main__":
    main()
