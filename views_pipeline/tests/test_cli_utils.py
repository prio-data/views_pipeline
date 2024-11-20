# FILE: tests/test_cli_utils.py

import pytest
import sys
from views_pipeline.cli.utils import parse_args, validate_arguments

def test_parse_args_default():
    """
    Test the default behavior of parse_args.
    """
    sys.argv = ["main.py"]
    args = parse_args()
    
    # Default values
    assert args.run_type == "calibration"
    assert args.sweep is False
    assert args.train is False

def test_parse_args_run_type_calibration():
    """
    Test the run_type argument with value 'calibration'.
    """
    sys.argv = ["main.py", "--run_type", "calibration"]
    args = parse_args()
    
    assert args.run_type == "calibration"

def test_parse_args_run_type_testing():
    """
    Test the run_type argument with value 'testing'.
    """
    sys.argv = ["main.py", "--run_type", "testing"]
    args = parse_args()
    
    assert args.run_type == "testing"

def test_parse_args_run_type_forecasting():
    """
    Test the run_type argument with value 'forecasting'.
    """
    sys.argv = ["main.py", "--run_type", "forecasting"]
    args = parse_args()
    
    assert args.run_type == "forecasting"

def test_parse_args_sweep_flag():
    """
    Test the --sweep flag.
    """
    sys.argv = ["main.py", "--sweep"]
    args = parse_args()
    
    assert args.sweep is True
    assert args.run_type == "calibration"  # --sweep implies calibration

def test_parse_args_train_flag():
    """
    Test the --train flag.
    """
    sys.argv = ["main.py", "--train"]
    args = parse_args()
    
    assert args.train is True

def test_parse_args_sweep_and_train_flags():
    """
    Test the combination of --sweep and --train flags.
    """
    sys.argv = ["main.py", "--sweep", "--train"]
    args = parse_args()
    
    assert args.sweep is True
    assert args.train is True
    assert args.run_type == "calibration"  # --sweep implies calibration

def test_parse_args_run_type_and_sweep():
    """
    Test the combination of --run_type and --sweep flags.
    """
    sys.argv = ["main.py", "--run_type", "calibration", "--sweep"]
    args = parse_args()
    
    assert args.run_type == "calibration"
    assert args.sweep is True

def test_parse_args_invalid_run_type_with_sweep():
    """
    Test invalid combination of --run_type and --sweep flags.
    """
    sys.argv = ["main.py", "--run_type", "testing", "--sweep"]
    with pytest.raises(SystemExit):
        args = parse_args()
        validate_arguments(args)

def test_parse_args_invalid_run_type():
    """
    Test invalid run_type value.
    """
    sys.argv = ["main.py", "--run_type", "invalid"]
    with pytest.raises(SystemExit):
        parse_args()

def test_validate_arguments_sweep_with_non_calibration():
    """
    Test validate_arguments with --sweep and non-calibration run_type.
    """
    sys.argv = ["main.py", "--run_type", "testing", "--sweep"]
    args = parse_args()
    with pytest.raises(SystemExit):
        validate_arguments(args)

def test_validate_arguments_evaluate_with_forecasting():
    """
    Test validate_arguments with --evaluate and forecasting run_type.
    """
    sys.argv = ["main.py", "--run_type", "forecasting", "--evaluate"]
    args = parse_args()
    with pytest.raises(SystemExit):
        validate_arguments(args)

def test_validate_arguments_no_train_evaluate_sweep():
    """
    Test validate_arguments with no --train, --evaluate, or --sweep flags.
    """
    sys.argv = ["main.py", "--run_type", "calibration"]
    args = parse_args()
    with pytest.raises(SystemExit):
        validate_arguments(args)

def test_validate_arguments_train_and_artifact_name():
    """
    Test validate_arguments with both --train and --artifact_name flags.
    """
    sys.argv = ["main.py", "--train", "--artifact_name", "calibration_model_20230101_120000.pt"]
    args = parse_args()
    with pytest.raises(SystemExit):
        validate_arguments(args)

def test_validate_arguments_forecast_with_non_forecasting():
    """
    Test validate_arguments with --forecast and non-forecasting run_type.
    """
    sys.argv = ["main.py", "--run_type", "calibration", "--forecast"]
    args = parse_args()
    with pytest.raises(SystemExit):
        validate_arguments(args)

def test_validate_arguments_ensemble_with_sweep():
    """
    Test validate_arguments with --ensemble and --sweep flags.
    """
    sys.argv = ["main.py", "--ensemble", "--sweep"]
    args = parse_args()
    with pytest.raises(SystemExit):
        validate_arguments(args)

def test_validate_arguments_no_train_no_saved():
    """
    Test validate_arguments with neither --train nor --saved flags.
    """
    sys.argv = ["main.py"]
    args = parse_args()
    with pytest.raises(SystemExit):
        validate_arguments(args)