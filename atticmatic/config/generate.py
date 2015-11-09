from collections import namedtuple
import os

from ruamel.yaml import dump, RoundTripDumper

from atticmatic.backends.options import capture_argument_parser, extract_parser_options


Config_option = namedtuple('Config_option', ('name', 'default'))


def dump_config(config):
    '''
    Given a config dict, dump it as YAML and return it.
    '''
    return dump(config, Dumper=RoundTripDumper, default_flow_style=False)


def generate_sample_config_file(backend, config_filename):
    '''
    Given an atticmatic backend, generate a sample config file and write it to the given filename.

    Raise IOError/PermissionError if something file-related goes wrong.
    '''
    # TODO: What about source_directories? Don't we still need that option?
    # TODO: What about repository option? Don't we still need that too?

    if os.path.exists(config_filename):
        raise IOError(
            'File already exists. Move it aside and try again: {}'.format(
                config_filename,
            )
        )

    parser = capture_argument_parser(backend.ARCHIVER_CLASS, backend.ARGUMENT_PARSER_CLASS)
    command_options = extract_parser_options(parser)
    config = sample_config(command_options)

    repository_config = {'repository': 'user@backupserver:sourcehostname.attic'}
    sources_config = {'source_directories': ('/home', '/etc')}

    output_file = open(config_filename, 'w')
    try:
        output_file.write(
            ''.join((
                '# Paths of source directories to backup.\n',
                dump_config(sources_config),  
                '# Path to local or remote repository.\n',
                dump_config(repository_config),
                '# For documentation on the rest of these options, see:\n',
                '# {}\n'.format(backend.USAGE_DOCUMENTATION_URL),
                dump_config(config)
            ))
        )   
    finally:
        output_file.close()


def command_option_to_config(command_option):
    '''
    Given a command-line-style named option as an instance of
    atticmatic.backends.options.Command_option, return a config-style option
    as a Config_option that's more appropriate for use in a configuration file.
    This involves stripping leading punctuation and converting hyphens to
    underscores. Also, any defaults are flattened to strings.

    Example: "--posix-me-harder" becomes "posix_me_harder"
    '''
    name = command_option.name.strip('-').replace('-', '_')

    if isinstance(command_option.default, (tuple, list)):
        return (name, ','.join(str(element) for element in command_option.default))
    if isinstance(command_option.default, dict):
        return (name, None)

    return Config_option(name, command_option.default)


def sample_config(command_options):
    '''
    Given a dict from the name of a backend sub-command to a sequence of supported Command_options
    for that sub-command, return a similar dict with each such sequence tranformed into a dict of
    option name to defaults, suitable for use in a configuration file.

    Example:

        {'create': (Command_option('--foo', 'bar'), Command_option('--baz', 'quux'))}

    ... becomes:

        {'create': {'foo': 'bar', 'baz': 'quux'}}
    '''
    return {
        sub_command_name: dict(command_option_to_config(option) for option in options)
        for sub_command_name, options in command_options.items()
    }
