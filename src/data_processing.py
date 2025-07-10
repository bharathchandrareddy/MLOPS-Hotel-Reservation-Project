import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import load_data, read_yaml
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier

logger = get_logger(__name__)

class DataProcessor:
    '''
    this class handles the important data preprocessing steps

    '''

    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def preprocess_data(self,df):
        try:
            logger.info('starting our data processing step')
            df.drop(columns=['Booking_ID'], inplace = True)
            
            df.drop_duplicates(inplace = True)
            logger.info('Dropped unwanted columns and duplicates')

            cat_columns = self.config["data_processing"]["categorical_columns"]
            num_columns = self.config["data_processing"]["numerical_columns"]

            logger.info("Applying Label Encoder")
            label_encoder = LabelEncoder()
            mappings={}

            for col in cat_columns:
                df[col] = label_encoder.fit_transform(df[col])

                mappings[col] = {label:code for label,code in zip(label_encoder.classes_ , label_encoder.transform(label_encoder.classes_))}

            logger.info(f'Label mappings are done')
            for col, mapping in mappings.items():
                logger.info(f"{col}: {mapping}")

            logger.info("Started Skewness Handling")

            skew_threshold = self.config["data_processing"]["skewness_threshold"]
            skewness= df[num_columns].apply(lambda x:x.skew())

            for column in skewness[skewness > skew_threshold].index:
                df[column] = np.log1p(df[column])

            return df
        
        except Exception as e:
            logger.error(f"Error during preprocessing {e}")
            raise CustomException("Error while processing data",e)
        
    def balace_data(self, df):
        try:
            logger.info("Started handling imbalance data")
            X = df.drop(columns='booking_status')
            y = df["booking_status"]
            smote = SMOTE(random_state=42)
            X_resampled , y_resampled = smote.fit_resample(X,y)
            balanced_df = pd.DataFrame(X_resampled , columns=X.columns)
            balanced_df["booking_status"] = y_resampled

            logger.info("Data balanced successfully")
            return balanced_df


        except Exception as e:
            logger.error(f"Error during balancing data {e}")
            raise CustomException("Error while balancing data",e)

    def feature_selection(self,df):
        try:

            logger.info("Starting feature selection")
            X = df.drop(columns='booking_status')
            y = df["booking_status"]
            model =  RandomForestClassifier(random_state=42)
            model.fit(X,y)
            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                        'feature':X.columns,
                        'importance':feature_importance
                             })
            top_features_importance_df = feature_importance_df.sort_values(by="importance" , ascending=False)
            num_of_features_to_select = self.config["data_processing"]["no_of_features"]
            top_10_features = top_features_importance_df["feature"].head(num_of_features_to_select).values

            top_10_df = df[top_10_features.tolist() + ["booking_status"]]
            logger.info("feature selection completed successfully")

            return top_10_df
        
        except Exception as e:
            logger.error(f"Error during feature selection of data {e}")
            raise CustomException("Error while feature selection of data",e)
        
    def save_data(self,df,file_path):
        try:
            logger.info("saving our data in processed folder")
            df.to_csv(file_path, index = False)

            logger.info(f"data saved successfully to {file_path}")

        except Exception as e:
            logger.error(f"Error durring saving the csv file {e}")
            raise CustomException("Error while saving csv file of data",e)
        
    def preprocess_pipeline(self):
        try:
            logger.info("Loading the data from raw directory")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balace_data(train_df)

            train_df = self.feature_selection(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df,PROCESSED_TRAIN_DATA)
            self.save_data(test_df,PROCESSED_TEST_DATA)

            logger.info("Data Processing completed sucessfully")

        except Exception as e:
            logger.error(f"Error durring preprocessing pipeline data {e}")
            raise CustomException("Error while data preprocessing pipeline",e)
        

if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_FILE_PATH)
    processor.preprocess_pipeline()



        





            
