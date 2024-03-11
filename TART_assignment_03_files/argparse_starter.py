import argparse

def parse_arguments():
    """
    parses arguments provided via command line with argparse

    """
    # setup
    parser = argparse.ArgumentParser(
        prog='BatchRenamer1',
        description='Renames files in specified folder')
    # create a string argument that is required
    parser.add_argument('-fp', '--filepath',
                        required=True,
                        help='filepath to look at.')
    # create a bool argument
    parser.add_argument('-v', '--verbose',
                        action="store_true",
                        help='sets the logger to print to screen')
    # parser
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_arguments()
    print(f'Filepath : {args.filepath}')
    print(f'Verbose : {args.verbose}')