import unittest, os
import inspect
from shutil import *

#Set up the path for unittets
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
os.sys.path.insert(0, grandparentdir + '/src')

from plugins import PluginsManager

def copytree(src, dst, symlinks=False, ignore=None):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    if not os.path.isdir(dst): # This one line does the trick
        os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                # Will raise a SpecialFileError for unsupported file types
                copy2(srcname, dstname)
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except (Error, err):
            errors.extend(err.args[0])
        except (EnvironmentError, why):
            errors.append((srcname, dstname, str(why)))
    try:
        copystat(src, dst)
    except (OSError, why):
        if WindowsError is not None and isinstance(why, WindowsError):
            # Copying file access times may fail on Windows
            pass
        else:
            errors.extend((src, dst, str(why)))
    if errors:
        raise (Error, errors)


class TestPluginsManager(unittest.TestCase):

    def setUp(self):
        # Copy fresh configuration for tests
        copytree(parentdir + '/vim-orig', parentdir + '/vim')
        copy(parentdir + '/vimrc-orig', parentdir + '/vimrc')
        self.vimhome = parentdir + '/vim'
        self.vimrc = parentdir + '/vimrc'
        self.pman = PluginsManager(self.vimhome)

    def test_upadte_plugins_list(self):
        print('\nTest plugins read from vimrc')
        self.pman.update_plugins_list(self.vimrc)
        for plugin in self.pman.plugins_list:
            print(plugin)

    def test_save_plugins_config(self):
        print('\nTest plugins wiritng to plugins.list')
        self.pman.update_plugins_list(self.vimrc)
        self.pman.save_plugins_config()
