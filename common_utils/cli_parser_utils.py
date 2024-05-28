import sys
import argparse

def parse_args():

    """
    CLI parser for model specific main.py scripts.
    """

    parser = argparse.ArgumentParser(description='Run model pipeline with specified run type.')

    parser.add_argument('-r', '--run_type',
                        choices=['calibration', 'testing', 'forecasting'],
                        type=str,
                        default='calibration',
                        help='Choose the run type for the model: calibration, testing, or forecasting. Default is calibration. '
                             'Note: If --sweep is flagged, --run_type must be calibration.')

    parser.add_argument('-s', '--sweep',
                        action='store_true',
                        help='Set flag to run the model pipeline as part of a sweep. No explicit flag means no sweep.'
                             'Note: If --sweep is flagged, --run_type must be calibration, and both training and evaluation is automatically implied.')
    
    parser.add_argument('-t', '--train',
                        action='store_true',
                        help='Flag to indicate if a new model should be trained. '
                             'Note: If --sweep is flagged, --train will also automatically be flagged.')

    parser.add_argument('-e', '--evaluate',
                        action='store_true',
                        help='Flag to indicate if the model should be evaluated. '
                             'Note: If --sweep is specified, --evaluate will also automatically be flagged. '
                             'Cannot be used with --run_type forecasting.')

    parser.add_argument('-a', '--artifact_name',
                        type=str,
                        help='Specify the name of the model artifact to be used for evaluation. '
                             'The file extension will be added in the main and fit with the specific model algorithm.'
                             'The artifact name should be in the format: <run_type>_model_<timestamp>.pt.'
                             'where <run_type> is calibration, testing, or forecasting, and <timestamp> is in the format %Y%m%d_%H%M%S.'
                             'If not provided, the latest artifact will be used by default.')

    return parser.parse_args()

def validate_arguments(args):
    if args.sweep:
        if args.run_type != 'calibration':
            print("Error: Sweep runs must have --run_type set to 'calibration'. Exiting.")
            print("To fix: Use --run_type calibration when --sweep is flagged.")
            sys.exit(1)

    if args.run_type in ['testing', 'forecasting'] and args.sweep:
        print("Error: Sweep cannot be performed with testing or forecasting run types. Exiting.")
        print("To fix: Remove --sweep flag or set --run_type to 'calibration'.")
        sys.exit(1)

    if args.run_type == 'forecasting' and args.evaluate:
        print("Error: Forecasting runs cannot evaluate. Exiting.")
        print("To fix: Remove --evaluate flag when --run_type is 'forecasting'.")
        sys.exit(1)

    if args.run_type in ['calibration', 'testing'] and not args.train and not args.evaluate:
        print(f"Error: Run type is {args.run_type} but neither --train nor --evaluate flag is set. Nothing to do... Exiting.")
        print("To fix: Add --train and/or --evaluate flag.")
        sys.exit(1)
