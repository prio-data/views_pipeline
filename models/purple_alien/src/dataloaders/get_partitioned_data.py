import sys
import argparse
from pathlib import Path

# Set up the path
PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)

# Import necessary functions
from utils_dataloaders import process_partition_data, parse_args

if __name__ == "__main__":
    # Parse CLI arguments
    args = parse_args()

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

    print(f"Partitions to be fetched from viewser: {', '.join(partitions_to_process)}")

    # Process calibration data if flag is set
    if args.calibration:
        df_cal, vol_cal = process_partition_data('calibration', PATH_RAW, PATH_PROCESSED)
        print(f"Fetch calibration data from viewser:")
        print(f"DataFrame shape: {df_cal.shape if df_cal is not None else 'None'}")
        print(f"Volume shape: {vol_cal.shape if vol_cal is not None else 'None'}")

    # Process testing data if flag is set
    if args.testing:
        df_test, vol_test = process_partition_data('testing', PATH_RAW, PATH_PROCESSED)
        print(f"Fetch testing data from viewser:")
        print(f"DataFrame shape: {df_test.shape if df_test is not None else 'None'}")
        print(f"Volume shape: {vol_test.shape if vol_test is not None else 'None'}")

    # Process forecasting data if flag is set
    if args.forecasting:
        df_forecast, vol_forecast = process_partition_data('forecasting', PATH_RAW, PATH_PROCESSED)
        print(f"Fetch forecasting data from viewser:")
        print(f"DataFrame shape: {df_forecast.shape if df_forecast is not None else 'None'}")
        print(f"Volume shape: {vol_forecast.shape if vol_forecast is not None else 'None'}")
