import os
import json
from pathlib import Path
import libcore.job
import libcore.capture
from .maintainer import Maintainer
from .updateserver import UpdateServer

from libcore import _version

__version__ = _version.__version__


def notify(notification, *args, **kwargs):
    """
    Make a notification to the user

    Args:
        notification(list or dict): dicts must be encodable to JSON.
    Example:
        >>> import libcore
        >>> libcore.notify([{'msg':'Hello'}])
        [{"msg":"Hello!"}]
    """
    if type(notification) != list:
        raise TypeError('must be a list of JSON encodable objects.')
    kwargs['flush'] = True
    print(json.dumps(notification), *args, **kwargs)


_default_heartbeat_file = Path('/home/cybercore-pi/heartbeat')


def _default_heartbeat(*args, **kwargs):
    _default_heartbeat_file.touch()


_heartbeat_function = _default_heartbeat


def set_heartbeat_function(f):
    """
    Set heartbeat action.

    Args:
        f(function): function which executes heartbeat action.

    Example:
        >>> import libcore
        >>> def heartbeat(): print("working!")
        ...
        >>> libcore.set_heartbeat_function(heartbeat)
        >>> libcore.heartbeat()
        working!
    """
    global _heartbeat_function
    _heartbeat_function = f


def heartbeat(*args, **kwargs):
    """
    Execute heartbeat action.

    Notes:
        Defalut action is 'touch /home/cybercore-pi/heartbeat'
    """
    _heartbeat_function(*args, **kwargs)
