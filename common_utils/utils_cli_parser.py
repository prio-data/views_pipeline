import sys
import argparse


def parse_args():
    """
    CLI parser for model specific main.py scripts.
    """

    parser = argparse.ArgumentParser(
        description="Run model pipeline with specified run type."
    )

    parser.add_argument(
        "-r",
        "--run_type",
        choices=["calibration", "testing", "forecasting"],
        type=str,
        default="calibration",
        help="Choose the run type for the model: calibration, testing, or forecasting. Default is calibration. "
        "Note: If --sweep is flagged, --run_type must be calibration.",
    )

    parser.add_argument(
        "-s",
        "--sweep",
        action="store_true",
        help="Set flag to run the model pipeline as part of a sweep. No explicit flag means no sweep."
        "Note: If --sweep is flagged, --run_type must be calibration, and both training and evaluation is automatically implied.",
    )

    parser.add_argument(
        "-t",
        "--train",
        action="store_true",
        help="Flag to indicate if a new model should be trained. "
        "Note: If --sweep is flagged, --train will also automatically be flagged.",
    )

    parser.add_argument(
        "-e",
        "--evaluate",
        action="store_true",
        help="Flag to indicate if the model should be evaluated. "
        "Note: If --sweep is specified, --evaluate will also automatically be flagged. "
        "Cannot be used with --run_type forecasting.",
    )

    parser.add_argument(
        "-f",
        "--forecast",
        action="store_true",
        help="Flag to indicate if the model should produce predictions. "
        "Note: If --sweep is specified, --forecast will also automatically be flagged. "
        "Can only be used with --run_type forecasting.",
    )

    parser.add_argument(
        "-a",
        "--artifact_name",
        type=str,
        help="Specify the name of the model artifact to be used for evaluation. "
        "The file extension will be added in the main and fit with the specific model algorithm."
        "The artifact name should be in the format: <run_type>_model_<timestamp>.pt."
        "where <run_type> is calibration, testing, or forecasting, and <timestamp> is in the format YMD_HMS."
        "If not provided, the latest artifact will be used by default.",
    )

    parser.add_argument(
        "-en",
        "--ensemble",
        action="store_true",
        help="Flag to indicate if the model is an ensemble.",
    )

    parser.add_argument(
        "-sa", "--saved", action="store_true", help="Used locally stored data"
    )

    parser.add_argument(
        "-o", "--override_month", help="Over-ride use of current month", type=int
    )

    parser.add_argument(
        "-dd", "--drift_self_test", action="store_true", default=False,
        help="Enable drift-detection self_test at data-fetch"
    )

    return parser.parse_args()


def validate_arguments(args):
    if args.sweep and args.run_type != "calibration":
        print("Error: Sweep runs must have --run_type set to 'calibration'. Exiting.")
        print("To fix: Use --run_type calibration when --sweep is flagged.")
        sys.exit(1)

    if args.evaluate and args.run_type == "forecasting":
        print("Error: Forecasting runs cannot evaluate. Exiting.")
        print("To fix: Remove --evaluate flag when --run_type is 'forecasting'.")
        sys.exit(1)

    if (
        args.run_type in ["calibration", "testing", "forecasting"]
        and not args.train
        and not args.evaluate
        and not args.forecast
        and not args.sweep
    ):
        print(
            f"Error: Run type is {args.run_type} but neither --train, --evaluate, nor --sweep flag is set. Nothing to do... Exiting."
        )
        print(
            "To fix: Add --train and/or --evaluate flag. Or use --sweep to run both training and evaluation in a WadnB sweep loop."
        )
        sys.exit(1)

    if args.train and args.artifact_name:
        print("Error: Both --train and --artifact_name flags are set. Exiting.")
        print("To fix: Remove --artifact_name if --train is set, or vice versa.")
        sys.exit(1)

    if args.forecast and args.run_type != "forecasting":
        print(
            "Error: --forecast flag can only be used with --run_type forecasting. Exiting."
        )
        print("To fix: Set --run_type to forecasting if --forecast is flagged.")
        sys.exit(1)

    if args.ensemble and args.sweep:
        # This is a temporary solution. In the future we might need to train and sweep the ensemble models.
        print(
            "Error: --aggregation flag cannot be used with --sweep. Exiting."
        )
        sys.exit(1)

    if not args.train and not args.saved:
        # if not training, then we need to use saved data
        print(
            "Error: if --train is not set, you should only use --saved flag. Exiting."
        )
        print("To fix: Add --train or --saved flag.")
        sys.exit(1)
