from flexmock import flexmock

from atticmatic.config import parse as module


def test_command_option_to_config_should_convert_name_for_config():
    default = flexmock()
    command_option = flexmock(name='--posix-me-harder', default=default)

    config_option = module.command_option_to_config(command_option)

    assert config_option == module.Config_option('posix_me_harder', default)


def test_command_option_to_config_should_convert_list_default_to_string():
    default = ['foo', 3, 'bar']
    command_option = flexmock(name='--opt', default=default)

    config_option = module.command_option_to_config(command_option)

    assert config_option == module.Config_option('opt', 'foo,3,bar')


def test_command_option_to_config_should_convert_dict_default_to_none():
    default = {1: 2}
    command_option = flexmock(name='--opt', default=default)

    config_option = module.command_option_to_config(command_option)

    assert config_option == module.Config_option('opt', None)


def test_sample_config_should_convert_command_options_to_config_dict():
    flexmock(module).command_option_to_config = \
        lambda option: module.Config_option(option.name, option.default)

    config = module.sample_config(
        {
            'create': (flexmock(name='foo', default='a'), flexmock(name='bar', default='b')),
            'prune': (flexmock(name='baz', default='c'), flexmock(name='quux', default='d')),
        }
    )

    assert sorted(config) == ['create', 'prune']
    assert sorted(config['create']) == ['bar', 'foo']
    assert sorted(config['prune']) == ['baz', 'quux']
