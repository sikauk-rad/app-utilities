from collections.abc import Iterable, Set, Hashable, Mapping
from functools import partial
from os import getenv, environ, PathLike
from pathlib import Path
import re
from typing import Any
import uuid

from beartype import beartype
from msgspec import json


@beartype
def env_string_to_dict(
    env_string: str
) -> dict[str, str]:

    """
    Parse an environment variable string into a dictionary.

    Converts a multi-line string of environment variable assignments into a dictionary,
    where each line is expected to be in the form `KEY=VALUE`. Quotation marks are removed,
    and empty lines are ignored.

    Parameters
    ----------
    env_string : str
        The environment variable string, with each variable assignment on a separate line.

    Returns
    -------
    dict[str, str]
        A dictionary mapping environment variable names to their values.

    Examples
    --------
    >>> env_string = '''
    ... FOO=bar
    ... BAZ=qux
    ... '''
    >>> env_string_to_dict(env_string)
    {'FOO': 'bar', 'BAZ': 'qux'}
    """

    return dict(map(
        partial(re.split, r'[\s+]=[\s+]'), 
        filter(None, env_string.replace('"', '').splitlines())
    ))


def check_keys_not_missing(
    required_keys: Iterable[Hashable],
    mapping: Mapping,
    mapping_name: str | None = None,
) -> None:

    """
    Check if all required keys are present in the given mapping.

    Args:
        required_keys (Iterable[Hashable]): An iterable of keys that must be present in the mapping.
        mapping (Mapping[Hashable, Any]): The mapping (e.g., dictionary) to check against.
        mapping_name (Optional[str]): An optional name for the mapping, used in the error message.

    Raises:
        KeyError: If any required keys are missing from the mapping, an error is raised with a message indicating which keys are missing and from which mapping they are expected.
    """

    if not isinstance(required_keys, Set):
        required_keys = {*required_keys}
    missing_keys = required_keys - mapping.keys()
    if not missing_keys:
        return

    missing_keys_str = ", ".join([*map(str, missing_keys)])
    error_suffix = f' in {mapping_name}.' if mapping_name else '.'
    raise KeyError(f'missing keys {missing_keys_str}{error_suffix}')


def load_id_from_env(
    env_variable_name: str,
) -> uuid.UUID:

    """
    Load a UUID from an environment variable.

    Args:
        env_variable_name (str): The name of the environment variable that contains the UUID.

    Returns:
        uuid.UUID: The UUID loaded from the environment variable.

    Raises:
        KeyError: If the environment variable is not set.
        ValueError: If the value of the environment variable is not a valid UUID.
    """

    if env_variable_name not in environ.keys():
        raise KeyError(f'{env_variable_name} not found in environment variables.')
        
    try:
        return uuid.UUID(getenv(env_variable_name))
    except (TypeError, ValueError):
        raise ValueError(f'The value of {env_variable_name} not a valid UUID.')


def load_config_from_path(
    config_path: PathLike,
    required_keys: Iterable[str],
    config_uuid: uuid.UUID,
) -> dict[str, Any]:

    """
    Load configuration from a JSON file specified in an environment variable.

    Args:
        config_path (PathLike): The path to the configuration file, which must be a JSON.
        required_keys (Iterable[str]): A collection of keys that must be present in the configuration.
        config_uuid (uuid.UUID): The UUID to load the configuration for.

    Returns:
        dict: The configuration corresponding to the provided UUID.

    Raises:
        FileNotFoundError: If the config_path file does not exist.
        TypeError: If the specified file is not a JSON file.
        KeyError: If the config_uuid is not found in the configuration or if required keys are missing.
    """

    if not isinstance(config_path, Path):
        config_path = Path(config_path)

    if not config_path.is_file():
        raise FileNotFoundError(
            f'{config_path} not found.'
        )

    elif config_path.suffix != '.json':
        raise TypeError(
            f'{config_path} must be a .json file.'
        )

    with open(file=config_path, mode='rb') as configs_bytesio:
        configs = json.decode(configs_bytesio.read())

    for config_uuid_, config in configs.items():
        try:
            config_uuid_ = uuid.UUID(config_uuid_)
        except (ValueError, TypeError):
            continue
    
        if config_uuid == config_uuid_:
            break
    else:
        raise KeyError(f'config_uuid {config_uuid} not found as key in app_config.')

    check_keys_not_missing(
        required_keys = required_keys,
        mapping = config,
        mapping_name = 'config'
    )

    return config