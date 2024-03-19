
from models.blue_sea import main as all_zero_baseline_model
from models.yellow_duck import main as no_change_baseline_model


def main():
    all_zero_baseline_model.main()
    no_change_baseline_model.main()


if __name__ == "__main__":
    main()
