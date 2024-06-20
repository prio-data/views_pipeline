import sys
import argparse
from pathlib import Path
import wandb

# Set up the path
PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)

# Import necessary functions
from utils_dataloaders import fetch_or_load_views_df, create_or_load_views_vol, parse_args, get_alert_help_string
from common_configs import config_drift_detection

if __name__ == "__main__":
    # Parse CLI arguments
    args = parse_args()

    # wandb login to log output from drift-detection machinery
    wandb.login()

    project = f"purple_alien_data" # project name should go in the config

    PATH_RAW, PATH_PROCESSED, _ = setup_data_paths(PATH)

    # Immediate feedback on partitions to be processed
    partitions_to_process = []
    if args.calibration:
        partitions_to_process.append('calibration')
    if args.testing:
        partitions_to_process.append('testing')
    if args.forecasting:
        partitions_to_process.append('forecasting')

    if not partitions_to_process:
        print("Error: No partition flag provided. Use -c, -t, and/or -f.")
        sys.exit(1)

    print(f"Partitions to be fetched: {', '.join(partitions_to_process)}")

    config = config_drift_detection.drift_detection_partition_dict

    with wandb.init(project=project, entity="views_pipeline", config=config, notes=get_alert_help_string()):

#        wandb.log({f"_Input drift detection": get_alert_help_string()})

#        print(get_alert_help_string())

        # Process calibration data if flag is set
        if args.calibration:

            df_cal, alerts_cal = fetch_or_load_views_df('calibration', PATH_RAW, args.saved)
            for ialert, alert in enumerate(str(alerts_cal).strip('[').strip(']').split('Input')):
                if 'offender' in alert:
                    wandb.log({f"calibration data alert {ialert}": str(alert)})

            vol_cal = create_or_load_views_vol('calibration', PATH_PROCESSED, PATH_RAW)
#            print(f"Fetch calibration data from viewser:")
            print(f"DataFrame shape: {df_cal.shape if df_cal is not None else 'None'}")
            print(f"Volume shape: {vol_cal.shape if vol_cal is not None else 'None'}")

        # Process testing data if flag is set
        if args.testing:

            df_test, alerts_test = fetch_or_load_views_df('testing', PATH_RAW, args.saved)
            for ialert, alert in enumerate(str(alerts_test).strip('[').strip(']').split('Input')):
                if 'offender' in alert:
                    wandb.log({f"test data alert {ialert}": str(alert)})

            vol_test = create_or_load_views_vol('testing', PATH_PROCESSED, PATH_RAW)
#            print(f"Fetch testing data from viewser:")
            print(f"DataFrame shape: {df_test.shape if df_test is not None else 'None'}")
            print(f"Volume shape: {vol_test.shape if vol_test is not None else 'None'}")

        # Process forecasting data if flag is set
        if args.forecasting:
            df_forecast, alerts_forecast = fetch_or_load_views_df('forecasting', PATH_RAW, args.saved, args.override_month)
            for ialert, alert in enumerate(str(alerts_forecast).strip('[').strip(']').split('Input')):
                if 'offender' in alert:
                    wandb.log({f"forecasting data alert {ialert}": str(alert)})

            vol_forecast = create_or_load_views_vol('forecasting', PATH_PROCESSED, PATH_RAW)
#            print(f"Fetch forecasting data from viewser:")
            print(f"DataFrame shape: {df_forecast.shape if df_forecast is not None else 'None'}")
            print(f"Volume shape: {vol_forecast.shape if vol_forecast is not None else 'None'}")


# The only HydraNet specific thing here is really the volume creation. Everything else is generic to the data loading process.