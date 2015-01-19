import unittest, os
import inspect

# Set up the path for unittets
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0, parentdir)

from plugins import PluginsManager

class TestPluginsManager(unittest.TestCase):

    def setUp(self):
        self.pman = PluginsManager(os.getenv('HOME') + '/.vim_test')

    def test_upadte_plugins_list(self):
        self.pman.update_plugins_list(os.getenv('HOME') + '/.vimrc_test')

    def test_save_plugins_config(self):
        self.pman.save_plugins_config()
