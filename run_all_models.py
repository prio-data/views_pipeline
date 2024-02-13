
from models.all_zero_baseline_model import main as all_zero_baseline_model
from models.no_change_baseline_model import main as no_change_baseline_model
from models.a_pgm_model import main_training as a_pgm_model


def main():
    all_zero_baseline_model.main()
    no_change_baseline_model.main()
    a_pgm_model.main()


if __name__ == "__main__":
    main()
