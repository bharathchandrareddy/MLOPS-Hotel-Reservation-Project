import os
import yaml
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException


logger = get_logger(__name__)


def read_yaml(file_path:str):
    """
    Reads a YAML file and returns its content as a dictionary.
    
    Args:
        file_path (str): Path to the YAML file.
        
    Returns:
        dict: Content of the YAML file.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Error reading YAML file: {e}")
        raise CustomException(f"Error reading YAML file: {e}")


def load_data(path:str):
    '''
    reads acsv file and return its content in the form of pandas dataframe

    args: file_path
    return: pandas data frame
    '''
    try:
        logger.info('Loading the data')
        return pd.read_csv(path)
    except Exception as e:
        logger.info(f'error loading the data {e}')

        CustomException('Error during loading the data file')

    
