import sys

from functools import partial

try:
    from borg.archiver import Archiver, argparse
except ImportError:
    print('Error: Cannot import borg. Try: pip install borgbackup', file=sys.stderr)
    sys.exit(1)

from atticmatic.config.legacy import Section_format, option
from atticmatic.backends import shared


# An atticmatic backend that supports Borg for actually handling backups.

COMMAND = 'borg'
USAGE_DOCUMENTATION_URL = 'https://borgbackup.readthedocs.org/en/latest/usage.html'
ARCHIVER_CLASS = Archiver
ARGUMENT_PARSER_CLASS = argparse.ArgumentParser
CONFIG_FORMAT = (
    shared.CONFIG_FORMAT[0],  # location
    Section_format(
        'storage',
        (
            option('encryption_passphrase', required=False),
            option('compression', required=False),
        ),
    ),
    shared.CONFIG_FORMAT[2],  # retention
    Section_format(
        'consistency',
        (
            option('checks', required=False),
            option('check_last', required=False),
        ),
    )
)
DEFAULT_CONFIG_FILENAME = '/etc/{}matic/config'.format(COMMAND)
DEFAULT_EXCLUDES_FILENAME = '/etc/{}matic/excludes'.format(COMMAND)

initialize = partial(shared.initialize, command=COMMAND)
create_archive = partial(shared.create_archive, command=COMMAND)
prune_archives = partial(shared.prune_archives, command=COMMAND)
check_archives = partial(shared.check_archives, command=COMMAND)
