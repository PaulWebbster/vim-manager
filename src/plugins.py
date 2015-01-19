#!/usr/bin/python3
# Plugins updater based on plugins list defined in configs/plugins.list file
# Orginal version is created by PaulWebbster
# https://github.com/PaulWebbster/vim-configuration

import sys
import os
from git import Repo
import re


class PluginsManager(object):
    """Manages the connection with the synchronization copy in remote git
    repository. """

    def __init__(self, vimhome=os.getenv('HOME') + '/.vim'):
        """
        __init__

        :param vimhome: the path to user .vim directory
        """
        self.vimhome = vimhome
        self.plugins_list = []
        self.mgit = GitManager(self.vimhome)

    def update_plugins_list(self, vimrc=os.getenv('HOME') + '/.vimrc'):
        """
        update_plugins_list: updates the object plugins list based on plugin
        list in vimrc file.

        :param vimrc: path to .vimrc file
        """
        with open(vimrc, 'r') as fvimrc:
            ppta = re.compile("NeoBundle '([A-z0-9\/\-\.]+)'")
            for line in fvimrc:
                if "NeoBundle '" in line:
                    self.plugins_list.append(ppta.match(line).group(1))

    def save_plugins_config(self):
        """
        save_plugins_config: updates the config file plugins.list with
        plugins added manualy by user in his .vimrc file
        """
        with open(self.vimhome + '/configs/plugins.list', 'w+') as pluglist:
            for plugin in self.plugins_list:
                if not self.check_if_plugin_in_config(plugin):
                    pluglist.writeline("'{}'".format(plugin))
        print('Plugin config list updated...')

    def check_if_plugin_in_config(self, plugin):
        with open(self.vimhome + 'configs/plugins.list', 'r') as plist:
            for plug in plist:
                if plugin in plug:
                    return True
            return False


    def save_plugins_configuration(self, gitinfo=None):
        """save_plugins_configuration: saves plugins information in
        plugin_config file and sends it to git

        :param git_info: Custom git info
        """
        if not gitinfo:
            gitinfo = """
            """

    def update_vimrc_plugis(self):
        with open(self.vimhome + '/configs/plugins.list', 'r') as plist:
            plugins = ["NeoBundle " + plugin for plugin in plist]

        with open(sys.argv[1] + '/configs/vimrc', 'r') as fvimrc:
            vimrc = []
            for index, line in enumerate(fvimrc):
                vimrc.append(line)
                if line.find('Plugins') != -1:
                    pline = index + 1

        vimrc = vimrc[:pline]+plugins+vimrc[pline:]

        with open(os.getenv("HOME") + '/.vimrc', 'w') as fvimrc:
            fvimrc.writelines(vimrc)


class GitManager(object):
    """Manages the connection with the synchronization copy in remote git
    repository. Automates commiting changes into reopository of plugins, changes
    in vim configuration files and vim user disrectory. Uses GitPython framework
    for repository connections"""

    def __init__(self, repopath):
        self.repo = Repo(repopath)

    def commit(self, message=None, files=None):
        self.repo
