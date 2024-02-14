
from models.blue_sea import main as all_zero_baseline_model
from models.yellow_duck import main as no_change_baseline_model
from models.green_oracle import main_training as a_pgm_model
from ensembles.red_panda.src.online_evaluation.evaluate_forecast import ensemble_mean
from ensembles.pink_elephant.src.online_evaluation.evaluate_forecast import ensemble_median

def main():
    all_zero_baseline_model.main()
    no_change_baseline_model.main()
    a_pgm_model.main()
    ensemble_mean()
    ensemble_median()

if __name__ == "__main__":
    main()
