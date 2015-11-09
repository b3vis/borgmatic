from importlib import import_module


def load_backend(command_name):
    '''
    Given the name of the command with which this script was invoked, return the corresponding
    backend module responsible for actually dealing with backups.
    '''
    backend_name = {
        'atticmatic': 'attic',
        'borgmatic': 'borg',
    }.get(command_name.split('-')[0], 'attic')

    return import_module('atticmatic.backends.{}'.format(backend_name))
