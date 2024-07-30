def get_hp_config(): 
    hp_config = {
        "name": "white_snow",
        "models": ["lavender_haze", "blank_space"],
        "depvar": "ln_ged_sb_dep",
        "steps": [*range(1, 36 + 1, 1)]
    }
    return hp_config