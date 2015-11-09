from collections import namedtuple


class Capture_parser_exception(Exception):
    '''
    An exception intended to be raised by a monkeypatched parse_args() below.
    '''
    def __init__(self, parser):
        self.parser = parser


def fake_parse_args(self, args=None, namespace=None):
    '''
    A fake ArgumentParser.parse_args() that doesn't actually parse arguments, but instead captures
    the Attic/Borg parser in an exception for later consumption.
    '''
    raise Capture_parser_exception(self)


def capture_argument_parser(archiver_class, argument_parser_class):
    '''
    Given an Attic/Borg Archiver class imported from Attic/Borg internals, return the ArgumentParser
    instance that Attic/Borg uses to parse its command-line arguments. This requires monkeypatching
    because Attic/Borg do not expose this parser directly.
    '''
    original_parse_args = argument_parser_class.parse_args
    try:
        argument_parser_class.parse_args = fake_parse_args
        archiver_class().run()
    except Capture_parser_exception as exception:
        return exception.parser
    finally:
        argument_parser_class.parse_args = original_parse_args


INCLUDED_SUB_COMMANDS = {'create', 'prune', 'check'}
EXCLUDED_OPTIONS = {'--help', '--verbose', '--stats', '--progress', '--exclude', '--exclude-from'}
SUB_COMMANDS_ACTION_INDEX = -1  # Index of sub-commands parser action.
LONG_OPTION_NAME_INDEX = -1     # Index of the long option name (e.g. "--help" vs. "-h").


Command_option = namedtuple('Command_option', ('name', 'default'))


def extract_parser_options(parser):
    '''
    Given an ArgumentParser instance from Attic/Borg, return its supported options for the
    sub-commands that we're interested in. Exclude positional arguments and a few specific
    options that we handle separately.

    Return the options as a dict from the name of the sub-command to a sequence of supported
    Command_options for that sub-command. For example:

    {
        'create': (
            Command_option(name='--no-files-cache', default=True),
            Command_option(name='--umask', default=63),
            ...
        ),
        'prune': ...
    }
    '''
    return {
        sub_command_name: tuple(
            Command_option(action.option_strings[LONG_OPTION_NAME_INDEX], action.default)
            for action in sub_command._actions
            if action.option_strings
            if action.option_strings[LONG_OPTION_NAME_INDEX] not in EXCLUDED_OPTIONS
        )
        for sub_command_name, sub_command in parser._actions[SUB_COMMANDS_ACTION_INDEX].choices.items()
        if sub_command_name in INCLUDED_SUB_COMMANDS
    }
