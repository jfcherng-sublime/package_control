import sys
import os
from os.path import dirname
from zipimport import zipimporter

import sublime

if os.name == 'nt':
    from ctypes import windll, create_unicode_buffer


data_dir = None
cache_dir = None
packages_path = None
installed_packages_path = None
pc_package_path = None


def decode(path):
    return path


def encode(path):
    return path


# Unpacked install of Sublime Text
if not isinstance(__loader__, zipimporter):
    pc_package_path = dirname(dirname(__file__))
    packages_path = dirname(pc_package_path)
    # For a non-development build, the Installed Packages are next
    # to the Packages dir
    _possible_installed_packages_path = os.path.join(dirname(packages_path), 'Installed Packages')
    if os.path.exists(_possible_installed_packages_path):
        installed_packages_path = _possible_installed_packages_path

# When loaded as a .sublime-package file, the filename ends up being
# Package Control.sublime-package/Package Control.package_control.sys_path
else:
    pc_package_path = dirname(dirname(__file__))
    installed_packages_path = dirname(pc_package_path)
    # For a non-development build, the Packages are next
    # to the Installed Packages dir
    _possible_packages_path = os.path.join(dirname(installed_packages_path), 'Packages')
    if os.path.exists(_possible_packages_path):
        packages_path = _possible_packages_path

if packages_path is None:
    import Default.sort

    if not isinstance(Default.sort.__loader__, zipimporter):
        packages_path = dirname(dirname(Default.sort.__file__))

if installed_packages_path is None:
    _data_base = None
    if sys.platform == 'darwin':
        _data_base = os.path.expanduser('~/Library/Application Support')
    elif sys.platform == 'win32':
        _data_base = os.environ.get('APPDATA')
    else:
        _data_base = os.environ.get('XDG_CONFIG_HOME')
        if _data_base is None:
            _data_base = os.path.expanduser('~/.config')

    if _data_base is not None:
        for _leaf in ['Sublime Text Development', 'Sublime Text 3 Development']:
            if sys.platform not in set(['win32', 'darwin']):
                _leaf = _leaf.lower().replace(' ', '-')
            _possible_data_dir = os.path.join(_data_base, _leaf)
            if os.path.exists(_possible_data_dir):
                data_dir = _possible_data_dir
                _possible_installed_packages_path = os.path.join(data_dir, 'Installed Packages')
                if os.path.exists(_possible_installed_packages_path):
                    installed_packages_path = _possible_installed_packages_path
                break

if installed_packages_path and data_dir is None:
    data_dir = dirname(installed_packages_path)


def lib_paths():
    """
    Returns a dict of version-specific lib folders

    :return:
        A dict with the key "3.3" and possibly the key "3.8"
    """

    if int(sublime.version()) >= 4000:
        return {
            "3.3": os.path.join(sys_path.data_dir, "Lib", "python33"),
            "3.8": os.path.join(sys_path.data_dir, "Lib", "python38"),
        }

    return {
        "3.3": os.path.join(sys_path.data_dir, "Lib", "python3.3"),
    }


def pc_cache_dir():
    """
    Returns the cache directory for Package Control files

    :return:
        A unicode string of the Package Control cache dir
    """

    global cache_dir

    if cache_dir is None:
        cache_dir = sublime.cache_path()

    return os.path.join(cache_dir, 'Package Control')


def user_config_dir():
    """
    Returns the directory for the user's config

    :return:
        A unicode string of the user's config dir
    """

    return os.path.join(sublime.packages_path(), 'User')
