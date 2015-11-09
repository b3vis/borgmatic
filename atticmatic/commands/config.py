from __future__ import print_function
from argparse import ArgumentParser
import os
import sys

from atticmatic.backends.load import load_backend
from atticmatic.config.generate import generate_sample_config_file
from atticmatic.config.validate import Configuration_error, validate_config_file


def parse_arguments(default_config_filename, *arguments):
    '''
    Given the default configuration filename and the script's command-line arguments, parse the
    arguments and return them as an ArgumentParser instance.
    '''
    parser = ArgumentParser()
    parser.add_argument(
        '-c', '--config',
        dest='config_filename',
        default=default_config_filename,
        help='Configuration filename (default: {})'.format(default_config_filename),
    )
    subparsers = parser.add_subparsers(dest='operation')
    subparsers.required = True
 
    subparsers.add_parser(
        'generate',
        help='Generate a sample configuration file containing defaults',
    )

    subparsers.add_parser(
        'validate',
        help='Perform syntax and option validation of a configuration file',
    )

    subparsers.add_parser(
        'upgrade',
        help='Upgrade a legacy ini-style configuration file to the new YAML syntax',
    )

    return parser.parse_args(arguments)


def main():
    '''
    Perform an operation on an atticmatic configuration file.
    '''
    try:
        command_name = os.path.basename(sys.argv[0])
        backend = load_backend(command_name)
        args = parse_arguments(backend.DEFAULT_CONFIG_FILENAME, *sys.argv[1:])

        operation_function = {
            'generate': generate_sample_config_file,
            'validate': validate_config_file,
            'upgrade': lambda: None,   # TODO
        }.get(args.operation)

        operation_function(backend, args.config_filename)
    except (IOError, Configuration_error) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
