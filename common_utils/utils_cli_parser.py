import sys
import argparse

import argparse
import sys

def parse_args():
    """
    Parses command-line arguments for the model pipeline.

    This function sets up and parses command-line arguments used to configure 
    the model pipeline. It provides options for specifying the type of run 
    (e.g., calibration, testing, forecasting), whether to include a sweep, 
    training, evaluation, or forecasting, and to specify the model artifact name.

    Arguments:
        -r, --run_type: Specifies the type of run. Options are 'calibration', 
                        'testing', or 'forecasting'. Default is 'calibration'.
                        This refers to wich partition of the data to used.
                        Note: If --sweep is flagged, --run_type must be 'calibration'.

        -s, --sweep:     Flag to run the model pipeline as part of a sweep. If 
                        flagged, both training and evaluation are implied. 
                        Note: --run_type must be 'calibration' if --sweep is used.

        -t, --train:     Flag to indicate if a new model should be trained. 
                        If --sweep is flagged, --train is automatically set.
                        If --sweep is not flagged, --train will also produce
                        a model artifact that can be used for evaluation/forecasting.

        -e, --evaluate:  Flag to indicate if the model should be evaluated. 
                        Cannot be used with --run_type 'forecasting'. 
                        If --sweep is specified, --evaluate is automatically set.
                        If --sweep is not specified, --evaluate will evaluate the latest model artifact.
                        Unless --artifact_name is specified, in which case that artifact will be evaluated.

        -f, --forecast:  Flag to indicate if the model should generate true forecasts.
                        Relevant for forecasting runs, where predictions are made 
                        for future time steps without holdout data evaluation.
                        Will use the latest model artifact by default, unless --artifact_name is specified.

        -a, --artifact_name: Specifies the name of the model artifact for evaluation.
                            The artifact name should follow the format: 
                            <run_type>_model_<timestamp>.pt. If not provided, the latest 
                            artifact is used by default.
    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments.
    """
    
    parser = argparse.ArgumentParser(description='Run model pipeline with specified run type (data partition).')

    parser.add_argument('-r', '--run_type',
                        choices=['calibration', 'testing', 'forecasting'],
                        type=str,
                        default='calibration',
                        help='Choose the run type for the model: calibration, testing, or forecasting. Default is calibration. '
                             'Note: If --sweep is flagged, --run_type must be calibration.')

    parser.add_argument('-s', '--sweep',
                        action='store_true',
                        help='Set flag to run the model pipeline as part of a sweep. No explicit flag means no sweep. '
                             'Note: If --sweep is flagged, --run_type must be calibration, and both training and evaluation are automatically implied.')

    parser.add_argument('-t', '--train',
                        action='store_true',
                        help='Flag to indicate if a new model should be trained. '
                             'Note: If --sweep is flagged, --train will also automatically be flagged.')

    parser.add_argument('-e', '--evaluate',
                        action='store_true',
                        help='Flag to indicate if the model should be evaluated. '
                             'Note: If --sweep is specified, --evaluate will also automatically be flagged. '
                             'Cannot be used with --run_type forecasting.')

    parser.add_argument('-f', '--forecast',
                        action='store_true',
                        help='Flag to indicate if the model should be used for true forecasting. '
                             'Note: The purpose of this flag is to indicate that the model should generate true forecasts, i.e., predictions for future time steps. '
                             'This can in principle be used with any run type, but it is most relevant for forecasting runs. It is basically an evaluation run, but with no holdout data to evaluate on.')

    parser.add_argument('-a', '--artifact_name',
                        type=str,
                        help='Specify the name of the model artifact to be used for evaluation. '
                             'The file extension will be added in the main and fit with the specific model algorithm. '
                             'The artifact name should be in the format: <run_type>_model_<timestamp>.pt, '
                             'where <run_type> is calibration, testing, or forecasting, and <timestamp> is in the format YMD_HMS. '
                             'If not provided, the latest artifact will be used by default.')

    return parser.parse_args()



def validate_arguments(args):
    """
    Validates the parsed command-line arguments for consistency and logical correctness.

    This function checks the combination of provided arguments to ensure they 
    are logically consistent with the intended use of the model pipeline. It 
    exits the program with an error message if any invalid combinations are detected.

    Validations include:
        - If --sweep is flagged, --run_type must be 'calibration'.
        - --sweep cannot be combined with 'testing' or 'forecasting' run types.
        - --evaluate cannot be used with --run_type 'forecasting'.
        - At least one of --train, --evaluate, or --sweep must be set for 
          'calibration' or 'testing' run types.
        - A warning is issued if --forecast is used with 'calibration' or 'testing' run types,
          suggesting the use of 'forecasting' run type instead.

    Arguments:
        args: argparse.Namespace object containing the parsed command-line arguments.

    Side Effects:
        Exits the program with sys.exit(1) and prints an error message if validation fails.

    Returns:
        None
    """
    
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
        print("Error: Forecasting runs cannot evaluate. Use forecast flag -f for true forecasting. Use training flag -t if you need to train a new model artifact. Exiting.")
        print("To fix: Remove --evaluate flag when --run_type is 'forecasting'.")
        sys.exit(1)

    if args.run_type in ['calibration', 'testing'] and not args.train and not args.evaluate and not args.sweep:
        print(f"Error: Run type is {args.run_type} but neither --train, --evaluate, nor --sweep flag is set. Nothing to do... Exiting.")
        print("To fix: Add --train and/or --evaluate flag. Or use --sweep to run both training and evaluation in a WandB sweep loop.")
        sys.exit(1)

    if args.run_type in ['calibration', 'testing'] and args.forecast:
        print(f"WARNING: You are generating true forecast with the [{args.run_type}] run type. Are you sure you don't want to use the forecasting run type? Or alternatively do evaluation with the -e flag?")
        print("For true forecasts: ensure: -r forecasting -f")
        print("For evaluation of calibration partition: ensure: -r calibration -e")
        print("For evaluation of testing partition: ensure: -r testing -e")






#
#def parse_args():
#
#    """
#    CLI parser for model specific main.py scripts.
#    """
#
#    parser = argparse.ArgumentParser(description='Run model pipeline with specified run type.')
#
#    parser.add_argument('-r', '--run_type', # is partition a better name?
#                        choices=['calibration', 'testing', 'forecasting'],
#                        type=str,
#                        default='calibration',
#                        help='Choose the run type for the model: calibration, testing, or forecasting. Default is calibration. '
#                             'Note: If --sweep is flagged, --run_type must be calibration.')
#
#    parser.add_argument('-s', '--sweep',
#                        action='store_true',
#                        help='Set flag to run the model pipeline as part of a sweep. No explicit flag means no sweep.'
#                             'Note: If --sweep is flagged, --run_type must be calibration, and both training and evaluation is automatically implied.')
#    
#    parser.add_argument('-t', '--train',
#                        action='store_true',
#                        help='Flag to indicate if a new model should be trained. '
#                             'Note: If --sweep is flagged, --train will also automatically be flagged.')
#
#    parser.add_argument('-e', '--evaluate',
#                        action='store_true',
#                        help='Flag to indicate if the model should be evaluated. '
#                             'Note: If --sweep is specified, --evaluate will also automatically be flagged. '
#                             'Cannot be used with --run_type forecasting.')
#
#    parser.add_argument('-f', '--forecast',
#                         action='store_true',
#                         help='Flag to indicate if the model should be used for true forecasting.'
#                        'Note: The purpose of this flag is to indicate that the model should generate true forecasts, i.e. predictions for future time steps.' 
#                        'This can in principle be used with any run type, but it is most relevant for forecasting runs. It is dasically and evaluation run, but with no holdout data to evaluate on.')
#
#    parser.add_argument('-a', '--artifact_name',
#                        type=str,
#                        help='Specify the name of the model artifact to be used for evaluation. '
#                             'The file extension will be added in the main and fit with the specific model algorithm.'
#                             'The artifact name should be in the format: <run_type>_model_<timestamp>.pt.'
#                             'where <run_type> is calibration, testing, or forecasting, and <timestamp> is in the format YMD_HMS.'
#                             'If not provided, the latest artifact will be used by default.')
#
#    return parser.parse_args()
#
#def validate_arguments(args):
#    if args.sweep:
#        if args.run_type != 'calibration':
#            print("Error: Sweep runs must have --run_type set to 'calibration'. Exiting.")
#            print("To fix: Use --run_type calibration when --sweep is flagged.")
#            sys.exit(1)
#
#    if args.run_type in ['testing', 'forecasting'] and args.sweep:
#        print("Error: Sweep cannot be performed with testing or forecasting run types. Exiting.")
#        print("To fix: Remove --sweep flag or set --run_type to 'calibration'.")
#        sys.exit(1)
#
#    if args.run_type == 'forecasting' and args.evaluate:
#        print("Error: Forecasting runs cannot evaluate. Use forecast flag -f or true forecast. Use traning flag -t if you need to train a new model artifact. Exiting.")
#        print("To fix: Remove --evaluate flag when --run_type is 'forecasting'.")
#        sys.exit(1)
#
#    if args.run_type in ['calibration', 'testing'] and not args.train and not args.evaluate and not args.sweep:
#        print(f"Error: Run type is {args.run_type} but neither --train, --evaluate, nor --sweep flag is set. Nothing to do... Exiting.")
#        print("To fix: Add --train and/or --evaluate flag. Or use --sweep to run both training and evaluation in a WadnB sweep loop.")
#        sys.exit(1)
#
#    if args.run_type in ['calibration', 'testing'] and args.forecast:
#        print(f"WARNING: you are generating true forcast with the [{args.run_type}] run type. Are you sure you don't want to use the forecasting run type? Or alternatively do evaluation with the -e flag?")           
#        print("For true forecasts: ensure: -r forecasting -f")
#        print("For evaluation of calibration partition: ensure: -r calibration -e")
#        print("For evaluation of testing partition: ensure: -r testing -e")
#
#
#    # notes on stepshifted models:
#    # There will be some thinking here in regards to how we store, denote (naming convention), and retrieve the model artifacts from stepshifted models.
#    # It is not a big issue, but it is something to consider os we don't do something headless. 
#    # A possible format could be: <run_type>_model_s<step>_<timestamp>.pt example: calibration_model_s00_20210831_123456.pt, calibration_model_s01_20210831_123456.pt, etc.
#    # And the rest of the code maded in a way to handle this naming convention without any issues. Could be a simple fix.
#    # Alternatively, we could store the model artifacts in a subfolder for each stepshifted model. This would make it easier to handle the artifacts, but it would also make it harder to retrieve the latest artifact for a given run type.
#    # Lastly, the solution Xiaolong is working on might allow us the store multiple models (steps) in one artifact, which would make this whole discussion obsolete and be the best solution.
#
#
