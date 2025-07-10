from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessor
from src.model_training import ModelTraining
from config.paths_config import *
from utils.common_functions import read_yaml


if __name__ == "__main__":
    ########################## DATA INGESTION #################################
    data_ingestion = DataIngestion(read_yaml(CONFIG_FILE_PATH))
    data_ingestion.run()


    ########################## DATA PROCESSING ############################
    processor = DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_FILE_PATH)
    processor.preprocess_pipeline()




    ########################### MODEL TRAINING ##############################

    model_training = ModelTraining(PROCESSED_TRAIN_DATA,PROCESSED_TEST_DATA,MODEL_OUTPUT_PATH)
    model_training.run()