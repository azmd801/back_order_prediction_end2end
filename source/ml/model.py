import yaml
import sys
import importlib
from source.logger import logging
from source.exception import BackOrderException
from source.constants.training_pipeline import MODULE_OF_MODEL,CLASS_OF_MODEL,TUNED_PARAMS_OF_MODEL,MODEL_CONFIG_FILE_PATH
from source.utils import read_yaml_file


class TunedModel:
    def __init__(self):
        try:
            self.config = read_yaml_file(MODEL_CONFIG_FILE_PATH)
            logging.info(f"Loaded model configuration")
        except Exception as e:
            raise #Exception("Could not load model configuration")
            
    
    def initiate_model(self):
        model_config = self.config.get('model', {})
        
        
        # Dynamically import the module and class
        module_name = model_config.get(MODULE_OF_MODEL)
        class_name = model_config.get(CLASS_OF_MODEL)
        params = model_config.get(TUNED_PARAMS_OF_MODEL)

          
        try:
            # Dynamically import the module and class
            module = importlib.import_module(module_name)
            ModelClass = getattr(module, class_name)
            
            logging.info(f"Instantiating model {class_name} from module {module_name}")
            
            # Instantiate and return the model with the given parameters
            model = ModelClass(**params)
            
            logging.info(f"Model {class_name} instantiated with parameters {params}")

            return model
        
        except Exception as e:
            raise BackOrderException(e, sys)