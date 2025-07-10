import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, precision_score,recall_score,f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml, load_data
from scipy.stats import randint
import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class ModelTraining:
    '''
    this class is created to 
    load the data --> split_data --> train model--> evaluate model --> save the model

    '''
    def __init__(self,train_path,test_path,model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.params_distribution = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_split_data(self):
        try:
            logger.info(f"Loading data from {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading data from {self.test_path}")
            test_df = load_data(self.test_path)

            X_train= train_df.drop(columns=["booking_status"])
            y_train = train_df["booking_status"]

            X_test = test_df.drop(columns=["booking_status"])
            y_test = test_df["booking_status"]

            logger.info("Data splitted successfully for model training")

            return X_train,X_test,y_train,y_test
        
        except Exception as e:
            logger.error(f"Error during splitting the data {e}")
            raise CustomException(f"failed to load data {e}")
        
    def train_lgbm(self,X_train,y_train):
        try:
            logger.info("started training the model")

            lgbm_model = lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])

            logger.info("starting our hyperparameter tuning")

            random_search = RandomizedSearchCV(
                estimator= lgbm_model,
                param_distributions= self.params_distribution,
                n_iter = self.random_search_params["n_iter"],
                cv = self.random_search_params["cv"],
                n_jobs = self.random_search_params["n_jobs"],
                verbose = self.random_search_params["verbose"],
                random_state= self.random_search_params["random_state"],
                scoring = self.random_search_params["scoring"]
            )

            logger.info("starting our hyperparameter tuning")

            random_search.fit(X_train,y_train)
            logger.info("Hyperparameter tuning")
            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_

            logger.info(f"Best parameters are :{best_params}")
            logger.info(f"Best lgbm model are :{best_lgbm_model}")
            return  best_lgbm_model
        
        except Exception as e:
            logger.error(f"Error during training model {e}")
            raise CustomException(f"failed to train model, {e}")
        
    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info(f"Evaluating out model")
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test,y_pred)
            precision = precision_score(y_test,y_pred)
            recall = recall_score(y_test,y_pred)
            f1 = f1_score(y_test,y_pred)

            logger.info(f"Accuracy score :{accuracy}")
            logger.info(f"Precision score :{precision}")
            logger.info(f"recall score :{recall}")
            logger.info(f"f1 score score :{f1}")

            return {
                "accuracy": accuracy,
                "precision":precision,
                "recall": recall,
                "f1 score": f1
            }
        except Exception as e:
            logger.error(f"Error during evaluating model model {e}")
            raise CustomException(f"failed to evaluate model, {e}")
        
    def save_model(self,model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            logger.info(f"saving the model")
            joblib.dump(model,self.model_output_path)
            logger.info(f"Model saved to {self.model_output_path}")
        except Exception as e:
            logger.error(f"Error during saving the model {e}")
            raise CustomException(f"failed to save model, {e}")
        
    def run(self):
        try:
            with mlflow.start_run():
                logger.info("starting running the model training pipeline and MLFlow experiment")

                logger.info("Logging the training and testing dataset to MLFlow")
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path,artifact_path="datasets")

                X_train,X_test,y_train,y_test = self.load_split_data()
                best_lgbm_model = self.train_lgbm(X_train, y_train)
                metrics = self.evaluate_model(best_lgbm_model,X_test,y_test)
                self.save_model(best_lgbm_model)

                logger.info(f"Logging the model into MLflow")
                mlflow.log_artifact(self.model_output_path)

                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(metrics)
                logger.info("Model training pipeline executed succefully")
        except Exception as e:
            logger.error(f"Error during model training pipeline {e}")
            raise CustomException(f"failed during model training pipeline, {e}")
        
if __name__ == "__main__":
    model_training = ModelTraining(PROCESSED_TRAIN_DATA,PROCESSED_TEST_DATA,MODEL_OUTPUT_PATH)
    model_training.run()

