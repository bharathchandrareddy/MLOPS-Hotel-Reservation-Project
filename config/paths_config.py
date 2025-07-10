'''
we can list the paths of the files in the project
to make it easier to access them in the code.
'''

import os

############################### DATA INGESTION PATHS ###############################

RAW_DIR = 'artifacts/raw'
RAW_FILE_PATH = os.path.join(RAW_DIR, 'Hotel_Reservations.csv')
TRAIN_FILE_PATH = os.path.join(RAW_DIR, 'train.csv')
TEST_FILE_PATH = os.path.join(RAW_DIR, 'test.csv')

CONFIG_FILE_PATH = 'config/config.yaml'

################################## DATA PROCESSING ################################

from pathlib import Path

PROCESSED_DIR = Path('artifacts') / 'processed'
PROCESSED_TRAIN_DATA = PROCESSED_DIR / 'processed_train.csv'
PROCESSED_TEST_DATA = PROCESSED_DIR / 'processed_test.csv'




# PROCESSED_DIR = 'artifacts\processed'
# PROCESSED_TRAIN_DATA = os.path.join(PROCESSED_DIR,'processed_train.csv')
# PROCESSED_TEST_DATA = os.path.join(PROCESSED_DIR,'processed_test.csv')


################################## MODEL TRAINING ##########################

MODEL_OUTPUT_PATH = "artifacts/models/lgbm_model.pkl"