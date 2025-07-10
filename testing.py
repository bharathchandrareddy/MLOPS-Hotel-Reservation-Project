from src.logger import get_logger
from src.custom_exception import CustomException
import sys
logger = get_logger(__name__)

def test_custom_exception(a,b):
    try:
        result = a/b
        logger.info('dividing two numbers')
        return result
    except Exception as e:
        logger.error(f'Error occurred: {e}')
        raise CustomException(e, sys)
    
if __name__ == "__main__":
    test_custom_exception(10, 1)