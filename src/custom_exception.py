import traceback  #to track the error we need this library
import sys

class CustomException(Exception):
    '''Custom exception class to handle exceptions in the application.'''
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def get_detailed_error_message(error_message:str,error_detail:sys)->str:
        """
        Function to get a detailed error message.
        :param error_message: The error message
        :param error_detail: The error details from sys
        :return: Formatted error message
        """
        tb = error_detail.exc_info()[2]
        file_name = tb.tb_frame.f_code.co_filename
        line_number = tb.tb_lineno
        #formatted_traceback = ''.join(traceback.format_list(tb))
        return f"Error occurred in script: {file_name} at line number: {line_number}\nError Message: {error_message}"
    
    def __str__(self):
        return self.error_message