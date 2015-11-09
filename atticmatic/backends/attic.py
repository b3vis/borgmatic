import sys

from functools import partial

try:
    from attic.archiver import Archiver, argparse
except ImportError:
    print('Error: Cannot import attic. Try: pip install Attic', file=sys.stderr)
    sys.exit(1)

from atticmatic.backends import shared


# An atticmatic backend that supports Attic for actually handling backups.

COMMAND = 'attic'
USAGE_DOCUMENTATION_URL = 'https://attic-backup.org/usage.html'
ARCHIVER_CLASS = Archiver
ARGUMENT_PARSER_CLASS = argparse.ArgumentParser
CONFIG_FORMAT = shared.CONFIG_FORMAT
DEFAULT_CONFIG_FILENAME = '/etc/{}matic/config'.format(COMMAND)
DEFAULT_EXCLUDES_FILENAME = '/etc/{}matic/excludes'.format(COMMAND)

initialize = partial(shared.initialize, command=COMMAND)
create_archive = partial(shared.create_archive, command=COMMAND)
prune_archives = partial(shared.prune_archives, command=COMMAND)
check_archives = partial(shared.check_archives, command=COMMAND)
