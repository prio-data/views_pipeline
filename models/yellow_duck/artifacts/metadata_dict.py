model_metadata = {

    "container_info": {
        "container_type": "apptainer", # Choose appropriate container type
        "container_version": "1.2", # Version of the container
        "container_author": "John Doe", # Author of the container. Likely, but not necessarily, the same as the author of the model.
        "container_date": "2023-04-01", # Date of the last containerization
        "notes": "..." # Include any additional information about the container
    },

    "model_info": {

				"model_flag": "baseline"
        "github_repo": "https://github.com/Jonh_D/RF_VIEWS_models.git", # Link to the GitHub repo where the code to train/test the model is stored
				"github_configs": "https://github.com/Jonh_D/RF_VIEWS_models/tree/main/src/configs" # Link to the GitHub repo where the config is stored - if a standard can be enforced this is not needed
        "model_name": "pink_panther_01012024", # Unique name for the model. Preferably descriptive including algorithm, the temp forecasting window, loa, and date of the training.
        "model_description": "Random Forest Regressor trained for a 36 forecasting window using Stepshifter v.3.0 for pgm loa Africa and Middle East", # Description of the model
        "model_version": "1.0", # Version of the model
        "model_author": "John Doe", # Author of the model
        "model_date": "2023-04-01", # Date of the last model training, testing, and evaluation before containerization.

				"regression_task": True, # note that some models may be solving both regression and classification tasks. In this case, regression_task and classification_task should both be set to True.
        "regression_optimization_criteria": "squared_error", # Chioose appropriate regression criteria. Must reflect the name used in the documentation of the model.
        
        "classification_task": False,# note that some models may be solving both regression and classification tasks. In this case, regression_task and classification_task should both be set to True.
        "classification_optimization_criteria": None, # Choose appropriate classification criteria. Must reflect the name used in the documentation of the model.

        "loa": "pgm", # For instance "pgm" (prio grid month), "cm" (country month), "am" (actor month), "pgy" (prio grid year), "cy" (country year), "ay" (actor year)

        "model_algorithm": "RandomForestRegressor",  # Specify appropriate ML algorithm
        "model_library": "sklearn",  # Specify appropriate ML library
        "model_dependencies": ["numpy 1.19.2", "pandas 1.1.3", "scikit-learn 0.23.2"],  # List of dependencies AND their versions
        "notes": "..." # Include any additional information about the model
    },

		"uncertainty_info": {
        "uncertainty_quantification": False, # If True, the model provides a sample of predictions for each forecasted temporal unit. If False  the model provides a point estimate for each forecasted temporal unit.
        "uncertainty_method": None, # Choose appropriate uncertainty type, for instance "ensemble", "dropout", "bayesian", "bootstrap", conformal prediction", etc. If uncertainty_estimate = False, this should be None.
        "uncertainty_samples": 1, # Number of samples drawn from the uncertainty distribution. If uncertainty_estimate = False, this should be 1.
        "notes": "..." # Include any additional information about the uncertainty
    },

    "feature_info": {
        "feature_names": ["feature_1", "feature_2", "feature_3", "feature_4", "feature_5", "feature_6", "feature_7", "feature_8" ],
        "optained_from": ["VIEWERS API v.3.0"], # If features are from different sources please elaborate in notes
        "optained_date": "2023-04-01",
        "notes" : "..." #Include any additional information about the features. 
        },

    "target_info": {
				"target_names": ["sb_best"], # List of target name(s). If a target is logged, normalized, or otherwise transformed, this should be reflected in the name. eg. "sb_best_ln"
        "target_types": ["continuous"], # Choose the appropriate target type. usually "continuous" or "binary". Noted that the order of this list must match the order of the target_names list.        "optained_from": ["VIEWERS API v.3.0"],
        "optained_from": ["VIEWERS API v.3.0"], #If there are multiple targets and they are from different sources please elaborate in notes
				"optained_date": "2023-04-01",
        "notes": "..." #Include any additional information about the target. 
        },

    "temporal_forecasting_window": { #realtive to end of history.
        "temporal_granularity": "month", # Choose appropriate temporal granularity. Must be consistent with loa.
        "first_step": 0,
        "last_step": 35,
        "notes": "..."
    },

    "geographical_forecasting_window": {
        "geographical_granularity": "prio_grid_cell", # Choose appropriate geographical granularity. Must be consistent with LOA.
        "Africa": True,
        "Middle East": True,
        "Asia": False,
        "Europe": False,
        "Americas": False,
        "Oceania": False,
        "custom": False, # If True, specify custom geographical forecasting window as list under custom_window. 
        "custom_window" : [], # If custom = Flase, leave the list empty. If custom = True, specify the custom geographical forecasting window here. For instance "Ukraine", or a list of countries, a list of prio grid cells ids.
        "notes": "..."
    },

    "actor_forcasting_window": { # only for loa = "am" or "ay"
        "state_actors" : [None], # List of all state actors included in the forecasts. If None, no actors-specific forecasts are included.
        "non_state_actors" : [None], # List of all non-state actors included in the forecasts. If None, no actors-specific forecasts are included.
        "notes": "..."
    },

    "training_info": {
        "start_month_id": 0,
        "end_month_id": 399,
        "notes": "...", #Include special considerations or notes for the training set
    },

    "validation_info": {
        "start_month_id": 400,
        "end_month_id": 599,
        "notes": "...", #Provide any specific details or constraints for the validation set. Particularly whether or not the model was validated across multiple temporal forecasting windows.
    },

    "testing_info": {
        "start_month_id": 600,
        "end_month_id": 635,
        "notes": "...", #Include information about the test set, such as any external factors affecting the data
    },

	"evaluation_metrics":{ 
        "step_wise": # Step is relative to end of history. Suggested step-specific ensemble weights may be supplied by the researcher but these are not necessarily to ones used in a given ensemble down stream.
        [
            {"step": 0, "MSE": 0.79493354, "MAE": 0.42519962, "MSLE": 0.12345678, "KLD": None, "Jeffreys": None, "CRPS": None, "Brier": None, "AP": None, "AUC": None, "ensemble_weight_reg": None, "ensemble_weight_class": None},
            {"step": 1, "MSE": 0.68004244, "MAE": 0.34056406, "MSLE": 0.10353466, "KLD": None, "Jeffreys": None, "CRPS": None, "Brier": None, "AP": None, "AUC": None, "ensemble_weight_reg": None, "ensemble_weight_class": None},
            #...
            {"step": 36, "MSE": 0.5064236, "MAE": 0.23054364, "MSLE": 0.08345464, "KLD": None, "Jeffreys": None, "CRPS": None, "Brier": None, "AP": None, "AUC": None, "ensemble_weight_reg": None, "ensemble_weight_class": None},
        ],
        "mean" : {"MSE": 0.6538689, "MAE": 0.33056365, "MSLE": 0.10345545, "KLD": None, "Jeffreys": None, "CRPS": None, "Brier": None, "AP": None, "AUC": None, "ensemble_weight_reg": None, "ensemble_weight_class": None},
        "std" : {"MSE": 0.0043682, "MAE": 0.00156365, "MSLE": 0.00345563, "KLD": None, "Jeffreys": None, "CRPS": None, "Brier": None, "AP": None, "AUC": None, "ensemble_weight_reg": None, "ensemble_weight_class": None},
        "median" : {"MSE": 0.6538689, "MAE": 0.33056365, "MSLE": 0.10345545, "KLD": None, "Jeffreys": None, "CRPS": None, "Brier": None, "AP": None, "AUC": None, "ensemble_weight_reg": None, "ensemble_weight_class": None},
				"notes" : "..."
    }
}