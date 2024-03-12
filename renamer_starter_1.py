"""
Batch Renamer Script
"""

import os
import argparse
import shutil
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


def parse_arguments():
    """
    Parses arguments provided via commadnd line with argparse

    """
    # Setup
    parser = argparse.ArgumentParser(
        prog = 'BatchRenamer',
        description = 'Renames files in specified folder')
    # Create a required string argument
    # filepath
    parser.add_argument('-fp', '--filepath',
                        required = True,
                        help = 'Filepath to look at')
    # new_folder
    parser.add_argument('-nf', '--new_folder',
                        required = True, 
                        help = "Filepath to move to")
    # string_to_find
    parser.add_argument('-find', '--strings_to_find',
                        action = 'append',
                        help = 'Strings to be replaced')
    # string_to_replace
    parser.add_argument('-rep', '--string_to_replace', 
                        default = '',
                        help = 'String to replace found strings with')
    # filetypes
    parser.add_argument('-type', '--filetypes',
                        action = 'append',
                        help = "Types of files to modify")
    # prefix
    parser.add_argument('-pfx', '--prefix',
                        default = '',
                        help = 'String to add to beginning of modified file')
    # suffix
    parser.add_argument('-sfx', '--suffix',
                        default = '',
                        help = 'String to add to end of modified file')

    # Create a bool argument
    parser.add_argument('-v', '--verbose',
                        action = 'store_true', 
                        help = 'Sets the logger to the print screen')
    # copy_mode
    parser.add_argument('-copy', '--copy_mode',
                        action = 'store_true',
                        help = "Enable copy mode")
    return parser.parse_args()
    

def modify_file(logger, existing_name, new_name, copy_mode=True, force=False):
    """
    Renames a file if it exists
    Only overwrites files if force is True
    
    Args:
        existing_name: full filepath for a file that should already exist
        new_name: full filepath for new name
        copy_mode: copy instead of rename
        force: allows overwriting files

    """
    # Verify the current file
    current = os.path.isfile(existing_name)
    if current == False:
        logger.error(f"The file,'{existing_name}' does not exist.")
        return
        
    # Verify the new name does not exist
    new_file = os.path.isfile(new_name)
    if new_file:
        logger.warning(f"The file, '{new_name}' already exists. Set force to true to overwrite")
        if force:
            os.remove(new_name)
            logger.info(f"Existing file '{new_name}' was deleted to allow overwrite")
                         
    # Set the action for copy_mode
    if copy_mode: 
        shutil.copy(existing_name, new_name)
        logger.info(f"File copied from '{existing_name}' to '{new_name}'.")
    else:
        shutil.move(existing_name, new_name)
        logger.info(f"file copied from '{existing_name}' to '{new_name}'.")


def process_folder(logger,
                   filepath, 
                   new_folder,
                   copy_files, 
                   overwrite, 
                   filetypes, 
                   strings_to_find,
                   string_to_replace,
                   prefix,
                   suffix):
    """
    Checks the given folder
    Gathers files in the folder
    Optionally limits files to modify
    Optionally does find and replace
    Optionally adds prefixes and suffixes

    Args:
        filepath: full filepath to a folder to find files in
        new_folder: full filepath to a folder to copy or move files to
        copy_mode: setting to copy files instead of rename them
        filetypes: filetypes to modify
        strings_to_find: list of strings to find in filename
        string_to_replace: string to replace and strings_to_find with
        prefix: string to add to the beginning of all modified files
        suffix: string to add to the end of all modified files
    """
    source_path = os.path.join(filepath)
    target_path = os.path.join(new_folder)

    # Check if the filepath is valid
    if not os.path.exists(source_path):
        logger.error(f"'{filepath}'is not a valid directory")
        return

    # Runs a for loop for each item in the filepath
    for file_name in os.listdir(filepath):
        # Split the path into file type and path
        file, file_ext = os.path.splitext(file_name)
        logger.info(f"Split the file path: {file}, {file_ext}")
        
        # Limit files to be modified
        if file_ext in filetypes:
            if strings_to_find:
                strings_to_find.sort(reverse=True)
                file = file.replace(strings_to_find, string_to_replace)
                logger.info(f"{strings_to_find} has been replaced with {string_to_replace}")
            if prefix:
                file = prefix + file
                logger.info(f"Prefix has been added to {file}")
            if suffix:
                file = file + suffix
                logger.info(f"Suffix has been added to {file}")
        new_name = os.path.join(target_path, file + file_ext)
        
    if source_path != new_name:
        modify_file(logger,
                source_path,
                target_path,
                copy_mode=copy_files,
                force=overwrite)
  



def main(renamer_args):
      # Logger
    logger = initialize_logger(True)
    logger.info('Logger Initiated')
    # Using dictionary here to make it easy to run main with a single arg
    process_folder(
        logger,
        filepath = renamer_args['filepath'],
        new_folder = renamer_args['new_folder'],
        copy_files = renamer_args['copy_files'],
        overwrite = renamer_args['overwrite'],
        filetypes = renamer_args['filetypes'],
        strings_to_find = renamer_args['strings_to_find'],
        string_to_replace = renamer_args['string_to_replace'],
        prefix = renamer_args['prefix'],
        suffix = renamer_args['suffix']
    )


if __name__ == '__main__':
    arguments = parse_arguments()
    # converting argparse data to a dictionary
    renamer_args_dict = {
        'filepath' : arguments.filepath,
        'new_folder' : arguments.new_folder,
        'copy_files' : arguments.copy_files,
        'overwrite' : arguments.overwrite,
        'filetypes' : arguments.filetypes,
        'strings_to_find' : arguments.strings_to_find,
        'string_to_replace' : arguments.string_to_replace,
        'prefix' : arguments.prefix,
        'suffix' : arguments.suffix
    }
    main(renamer_args_dict)