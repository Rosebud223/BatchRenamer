import os
import logging

def initialize_logger(print_to_screen = False):
    """
    Creates a logger

    Args:
        print_to_screen: for printing to screen as well as file
    """

    ###############
    # Basic Setup #
    ###############
    app_title = 'Test'
    version_number = '1.0.0'
    # get the path the script was run from, storing with forward slashes
    source_path = os.path.dirname(os.path.realpath(__file__))
    # create a log filepath
    logfile_name = f'{app_title}.log'
    logfile = os.path.join(source_path, logfile_name)

    # tell the user where the log file is
    print(f'Logfile is {logfile}')

    # more initialization
    logger = logging.getLogger(f'{app_title} Logger')
    logger.setLevel(logging.INFO)
    
    ###############################
    # Formatter and Handler Setup #
    ###############################
    file_handler = logging.FileHandler(logfile)
    file_handler.setLevel(logging.INFO)
    # formatting information we want (time, logger name, version, etc.)
    formatter = logging.Formatter(f'%(asctime)s - %(name)s {version_number} - '
                                  '%(levelname)s - %(message)s')
    # setting the log file format
    file_handler.setFormatter(formatter)
    # clean up old handlers
    logger.handlers.clear()

    # add handler
    logger.addHandler(file_handler)

    # allowing to print to screen
    if print_to_screen:
        # create a new "stream handler" for logging/printing to screen
        console = logging.StreamHandler()
        logger.addHandler(console)
        # setting the print log format
        console.setFormatter(formatter)

    # return logger so it can be used
    return logger

if __name__ == '__main__':
    # Test log
    logger = initialize_logger(True)
    logger.info('Logger Initiated')

'''
Output:
Logfile is D:/.../Test.log
2024-03-02 10:21:11,089 - Test Logger 1.0.0 - INFO - Logger Initiated
'''