import sys
import argparse
from pathlib import Path

# Set up the path
PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths
setup_project_paths(PATH)

# Import necessary functions
from utils_dataloaders import get_views_date, df_to_vol, process_partition_data, process_data, parse_args

import sys
import argparse
from pathlib import Path

# Set up the path
PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths
setup_project_paths(PATH)

# Import necessary functions
from config_hyperparameters import get_hp_config
from utils_dataloaders import get_views_date, df_to_vol, process_partition_data

if __name__ == "__main__":
    # Parse CLI arguments
    args = parse_args()

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

    print(f"Partitions to be processed: {', '.join(partitions_to_process)}")

    # Process calibration data if flag is set
    if args.calibration:
        df_cal, vol_cal = process_data('calibration', PATH)
        print(f"Processed calibration data:")
        print(f"DataFrame shape: {df_cal.shape if df_cal is not None else 'None'}")
        print(f"Volume shape: {vol_cal.shape if vol_cal is not None else 'None'}")

    # Process testing data if flag is set
    if args.testing:
        df_test, vol_test = process_data('testing', PATH)
        print(f"Processed testing data:")
        print(f"DataFrame shape: {df_test.shape if df_test is not None else 'None'}")
        print(f"Volume shape: {vol_test.shape if vol_test is not None else 'None'}")

    # Process forecasting data if flag is set
    if args.forecasting:
        df_forecast, vol_forecast = process_data('forecasting', PATH)
        print(f"Processed forecasting data:")
        print(f"DataFrame shape: {df_forecast.shape if df_forecast is not None else 'None'}")
        print(f"Volume shape: {vol_forecast.shape if vol_forecast is not None else 'None'}")
