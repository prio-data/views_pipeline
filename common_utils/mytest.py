from model_path import ModelPath
import os


yellow_pikachu = ModelPath("yellow_pikachu", validate=True)
#yellow_pikachu.view_scripts()
yellow_pikachu.get_queryset()
yellow_pikachu.view_directories()



models_path = 'models'


for model_name in os.listdir(models_path):
    model_dir = os.path.join(models_path, model_name)
    
    
    if os.path.isdir(model_dir) and model_name != 'hazel_rabbit' and model_name != 'abundant_abyss' :
        
        exec(f'model_name = ModelPath("{model_name}", validate=True)')
        
        
        #model_name.get_queryset()
        model_name.view_directories()
        model_name.add_paths_to_sys()
        print("after adding HERE")
        model_name.view_directories()
        model_name.remove_paths_from_sys()
    



taco_cat = ModelPath("taco_cat", validate=False)
taco = ModelPath("taco", validate=False)












# Initialize ModelPath with a model name
#yellow_pikachu = ModelPath("yellow_pikachu", validate=True)
#yellow_pikachu.view_scripts()
#yellow_pikachu.get_queryset()

"""
blank_space = ModelPath("blank_space", validate=False)
blank_space.get_queryset()

electric_relaxation = ModelPath("electric_relaxation", validate=False)
electric_relaxation.view_directories()
electric_relaxation.get_queryset()

lavender_haze = ModelPath("lavender_haze", validate=False)
lavender_haze.get_queryset()

orange_pasta = ModelPath("orange_pasta", validate=False)
orange_pasta.get_queryset()

purple_alien = ModelPath("purple_alien", validate=False)
purple_alien.view_directories()
purple_alien.get_queryset()

wildest_dream = ModelPath("wildest_dream", validate=False)
wildest_dream.get_queryset()
"""

#hazel_rabbit = ModelPath("hazel_rabbit")
#hazel_rabbit.get_directories()
#hazel_rabbit.get_queryset()