import os
import pandas as pd
from google.cloud import storage
from src.logger import get_logger
from src.custom_exception import CustomException
from utils.common_functions import read_yaml
from sklearn.model_selection import train_test_split
from config.paths_config import *

logger = get_logger(__name__) # this always needs to initialized

class DataIngestion:
    def __init__(self,config):
        """
        Initializes the DataIngestion class with configuration settings.
        
        Args:
            config (dict): Configuration settings for data ingestion.
        """
        self.config = config['data_ingestion']
        self.bucket_name = self.config['bucket_name']
        self.bucket_file_name = self.config['bucket_file_name']
        self.train_ratio = self.config['train_ratio']
        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info("DataIngestion class initialized with configuration settings.")
    def download_data(self):
        """
        Downloads data from Google Cloud Storage and saves it to the local filesystem.
        """
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)
            blob.download_to_filename(os.path.join(RAW_DIR, self.bucket_file_name))
            logger.info("Data downloaded successfully.")
        except Exception as e:
            logger.error(f"Error downloading data: {e}")
            raise CustomException(f"Error downloading data: {e}")
    def split_data(self):
        """
        Splits the downloaded data into training and testing sets.
        """
        try:
            df = pd.read_csv(os.path.join(RAW_DIR, self.bucket_file_name))
            train_df, test_df = train_test_split(df, train_size=self.train_ratio, random_state=42)
            train_df.to_csv(os.path.join(RAW_DIR, "train.csv"), index=False)
            test_df.to_csv(os.path.join(RAW_DIR, "test.csv"), index=False)
            logger.info("Data split into training and testing sets.")
        except Exception as e:
            logger.error(f"Error splitting data: {e}")
            raise CustomException(f"Error splitting data: {e}")
        
    def run(self):
        """
        Executes the data ingestion process: downloading and splitting data.
        """
        try:
            self.download_data()
            self.split_data()
            logger.info("Data ingestion process completed successfully.")
        except Exception as e:
            logger.error(f"Error in data ingestion process: {e}")
            raise CustomException(f"Error in data ingestion process: {e}")
        finally:
            logger.info("Data ingestion process finished.")
    
if __name__ == "__main__":
    config = read_yaml(CONFIG_FILE_PATH)
    data_ingestion = DataIngestion(config)
    data_ingestion.run()