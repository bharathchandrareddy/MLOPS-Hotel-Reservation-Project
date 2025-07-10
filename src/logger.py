'''
this file is used for logging purpose.
file requirements:
-to create a log file, you need to create a directory named 'LOGS' in the current working directory.
-logs will be stored in the 'LOGS' directory with the name 'logfile-datetime.log

'''

import logging
import os
from datetime import datetime

logs = 'LOGS'

os.makedirs(logs,exist_ok=True)
log_file_name = os.path.join(logs,f'logfile-{datetime.now().strftime("%Y-%m-%d")}.log')

logging.basicConfig(
    filename=log_file_name,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    level = logging.INFO,    
)
def get_logger(name):
    """
    Function to get a logger with the specified name.
    :param name: Name of the logger
    :return: Logger object
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
