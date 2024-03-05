def split_hurdle_parameters(parameters_dict):
    cls_dict = {}
    reg_dict = {}
    
    for key, value in parameters_dict.items():
        if key.startswith('cls_'):
            cls_key = key.replace('cls_', '')
            cls_dict[cls_key] = value
        elif key.startswith('reg_'):
            reg_key = key.replace('reg_', '')
            reg_dict[reg_key] = value
            
    return cls_dict, reg_dict