import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Run model pipeline with specified run type.')

    parser.add_argument('-r', '--run_type',
                        choices=['calibration', 'testing', 'forecasting'],
                        type=str,
                        default='calibration',
                        help='Choose the run type for the model: calibration, testing, or forecasting. Default is calibration. '
                             'Note: If --sweep is True, --run_type must be calibration.')

    parser.add_argument('-s', '--sweep',
                        choices=[True, False],
                        type=bool,
                        default=False,
                        help='Choose whether to run the model pipeline as part of a sweep. Default is False. '
                             'Note: If --sweep is True, --run_type must be calibration, and both --train and --evaluate will be set to True automatically.')

    parser.add_argument('-t', '--train',
                        choices=[True, False],
                        type=bool,
                        default=False,
                        help='Flag to indicate if a new model should be trained - if not, a model will be loaded from an artifact. '
                             'Note: If --sweep is True, --train will be set to True automatically.')

    parser.add_argument('-e', '--evaluate',
                        choices=[True, False],
                        type=bool,
                        default=False,
                        help='Flag to indicate if the model should be evaluated. '
                             'Note: If --sweep is True, --evaluate will be set to True automatically.'
                             'Cannot be used with --run_type forecasting.')

    return parser.parse_args()


def validate_arguments(args):
    if args.sweep:
        if args.run_type != 'calibration':
            print("Sweep runs must have run_type set to 'calibration'. Exiting.")
            print("To fix: Use --run_type calibration when --sweep True.")

            sys.exit(1)
        args.train = True
        args.evaluate = True

    if args.run_type in ['testing', 'forecasting'] and args.sweep:
        print("Sweep cannot be performed with testing or forecasting run types. Exiting.")
        print("To fix: Use --sweep False or set --run_type to 'calibration'.")
        sys.exit(1)

    if args.run_type == 'forecasting' and args.evaluate:
        print("Forecasting runs cannot evaluate. Exiting.")
        print("To fix: Use --evaluate False when --run_type is 'forecasting'.")
        sys.exit(1)

    if args.run_type in ['calibration', 'testing'] and not args.train and not args.evaluate:
        print(f"Run type is {args.run_type} but neither --train nor --evaluate flag is set. Exiting.")
        print("To fix: Use --train True and/or --evaluate True.")
        sys.exit(1)

