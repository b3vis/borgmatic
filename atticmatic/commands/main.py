from __future__ import print_function
from argparse import ArgumentParser
import os
from subprocess import CalledProcessError
import sys

from atticmatic.backends.load import load_backend
from atticmatic.config.legacy import parse_configuration


def parse_arguments(default_config_filename, default_excludes_filename, *arguments):
    '''
    Given default configuration and excludes filenames, and the script's command-line arguments,
    parse the arguments and return them as an ArgumentParser instance.
    '''
    if os.path.exists(default_excludes_filename):
        default_excludes_filename = None

    parser = ArgumentParser()
    parser.add_argument(
        '-c', '--config',
        dest='config_filename',
        default=default_config_filename,
        help='Configuration filename (default: {})'.format(default_config_filename),
    )
    parser.add_argument(
        '--excludes',
        dest='excludes_filename',
        default=default_excludes_filename,
        help='Excludes filename' + (
            ' (default: {})'.format(default_excludes_filename)
            if default_excludes_filename
            else ''
        ),
    )
    parser.add_argument(
        '-v', '--verbosity',
        type=int,
        help='Display verbose progress (1 for some, 2 for lots)',
    )

    return parser.parse_args(arguments)


def main():
    try:
        command_name = os.path.basename(sys.argv[0])
        backend = load_backend(command_name)
        args = parse_arguments(backend, *sys.argv[1:])
        # TODO: Validate and load new-style configuration here.
        config = parse_configuration(args.config_filename, backend.CONFIG_FORMAT)
        repository = config.location['repository']

        backend.initialize(config.storage)
        backend.create_archive(
            args.excludes_filename, args.verbosity, config.storage, **config.location
        )
        backend.prune_archives(args.verbosity, repository, config.retention)
        backend.check_archives(args.verbosity, repository, config.consistency)
    except (ValueError, IOError, CalledProcessError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
