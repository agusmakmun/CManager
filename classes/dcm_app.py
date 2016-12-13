#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2016 Fachrizal Oktavian
#   This file is part of DracOS Connection Manager.
#
#   DracOS Connection Manager is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   DracOS Connection Manager is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with DracOS Connection Manager.  If not, see <http://www.gnu.org/licenses/>.

"""
dcm_app
"""
from colorama import Fore, Back, Style, init
from dcm_interfaces import Dcm_interfaces
from dcm_connection import Dcm_connection
from dcm_network import Dcm_network
from dcm_help import Dcm_help


class Dcm_app(object):

    init(autoreset=True)

    """
    constant declaration
    """
    INFO = 0
    SUCCEED = 1
    FAILED = 2

    LOC_DASHBOARD = 'dashboard'
    LOC_DASHBOARD_WIZARD_WIFI = 'wifi-wizard'

    ACT_SYSTEM = 'system'
    ACT_POS = '+'
    ACT_NEG = '-'

    LIST_CMD_DASHBOARD = ['show', 'wizard', 'exit', 'help']
    LIST_CMD_DASHBOARD_WIZARD_WIFI = [
        'set', 'del', 'save',
        'show', 'use', 'scan',
        'connect', 'back', 'help'
    ]

    def app_header(self):
        header = '\n'
        header += '\t████████▄   ▄████████    ▄▄▄▄███▄▄▄▄   \n'
        header += '\t███   ▀███ ███    ███  ▄██▀▀▀███▀▀▀██▄ \n'
        header += '\t███    ███ ███    █▀   ███   ███   ███ \n'
        header += '\t███    ███ ███         ███   ███   ███ \n'
        header += '\t███    ███ ███         ███   ███   ███ \n'
        header += '\t███    ███ ███    █▄   ███   ███   ███ \n'
        header += '\t███   ▄███ ███    ███  ███   ███   ███ \n'
        header += '\t████████▀  ████████▀    ▀█   ███   █▀  \n'
        header2 = '\tDracOS Connection Manager\n'
        header3 = '------------------------------------------------------------------------------\n'
        header3 += '- Version      : 1.0                                                         -\n'
        header3 += '- Release Date : December 4th, 2016                                          -\n'
        header3 += '- Github       : https://github.com/fachrioktavian/DracOS-Connection-Manager -\n'
        header3 += '- Dev by       : Fachrizal Oktavian                                          -\n'
        header3 += '-                                                     << dracos-linux.org >> -\n'
        header3 += '------------------------------------------------------------------------------\n'
        print (Fore.RED + Style.DIM + header + header2)
        print (Fore.CYAN + Style.DIM + header3)

    def debug(self, indent, actor, deb_type, msg):
        """
        deb_type -> 0:info, 1:succeed, 2:failed
        """
        list_type = [Fore.YELLOW, Fore.GREEN, Fore.RED]
        deb_style = Style.DIM
        deb_color = list_type[deb_type]
        spaces = ' ' * indent
        print (deb_color + deb_style + spaces + '[' + actor + '] ' + msg)

    def __init__(self):
        """
        show app header
        """
        self.app_header()

        self.dcm_interfaces_handler = Dcm_interfaces()
        self.dcm_connection_handler = Dcm_connection()
        self.dcm_network_handler = Dcm_network()
        self.dcm_help_handler = Dcm_help()

        """
        resolve interfaces
        """
        self.dcm_interfaces_handler.resolve_Interfaces()
        self.list_ifaces_wireless = self.dcm_interfaces_handler.get_ifaces_wireless()
        self.list_ifaces_ethernet = self.dcm_interfaces_handler.get_ifaces_ethernet()
        self.list_ifaces_localhost = self.dcm_interfaces_handler.get_ifaces_localhost()

    def pre(self):
        if self.dcm_iface != 'NULL':
            return '(' + self.loc_now + '|' + self.dcm_iface + ') > '
        else:
            return '(' + self.loc_now + ') > '

    def resolve_loc(self):
        index = len(self.history_loc) - 1
        self.loc_now = self.history_loc[index]

    def action_dashboard(self):
        try:
            total_param = len(self.list_param)
            if self.cmd == 'show':
                if self.list_param[0] == 'interfaces' and total_param == 1:
                    self.dcm_interfaces_handler.print_ifaces_wireless_table()
                    self.dcm_interfaces_handler.print_ifaces_ethernet_table()
                    self.dcm_interfaces_handler.print_ifaces_localhost_table()
            elif self.cmd == 'wizard':
                if self.list_param[0] == 'wifi' and total_param == 1:
                    self.history_loc.append(self.LOC_DASHBOARD_WIZARD_WIFI)
            elif self.cmd == 'exit' and total_param == 0:
                self.flagExit = True
            elif self.cmd == 'help' and total_param == 0:
                self.dcm_help_handler.show_help()
        except Exception as e:
            print (e)

    def action_dashboard_wizard_wifi(self):
        try:
            total_param = len(self.list_param)
            if self.cmd == 'set' and total_param >= 2:
                var, value = self.list_param[0], self.list_param[1]
                if var == 'name':
                    self.dcm_connection_handler.set_profile_name(value)
                elif var == 'ssid':
                    value = ' '.join(self.list_param[1::])
                    self.dcm_connection_handler.set_profile_ssid(value)
                elif var == 'type':
                    if value in ['Open', 'WPA']:
                        self.dcm_connection_handler.set_profile_type(value)
                    else:
                        self.debug(1, self.ACT_NEG, 2, 'type should \'Open\' or \'WPA\'')
                elif var == 'passphrase':
                    value = ' '.join(self.list_param[1::])
                    self.dcm_connection_handler.set_profile_passphrase(value)
            elif self.cmd == 'show' and total_param == 1:
                if self.list_param[0] == 'profile':
                    self.dcm_connection_handler.show_profile()
                elif self.list_param[0] == 'options':
                    self.dcm_connection_handler.show_options()
            elif self.cmd == 'save':
                if self.list_param[0] == 'profile' and total_param == 1:
                    flagSave = self.dcm_connection_handler.save_profile()
                    if flagSave:
                        self.debug(1, self.ACT_POS, 1, 'Profile\'s saved')
                    else:
                        self.debug(1, self.ACT_NEG, 2, 'Profile\'s not saved')
            elif self.cmd == 'del':
                if self.list_param[0] == 'profile' and total_param == 2:
                    profile = self.list_param[1]
                    flagDel = self.dcm_connection_handler.delete_profile(profile)
                    if flagDel:
                        self.debug(1, self.ACT_POS, 1, 'Profile\'s deleted')
                else:
                    self.debug(1, self.ACT_NEG, 2, 'Profile\'s couldn\'t be deleted')
            elif self.cmd == 'use' and total_param == 1:
                if self.list_param[0] in self.list_ifaces_wireless:
                    self.dcm_iface = self.list_param[0]
            elif self.cmd == 'scan':
                if self.dcm_iface != 'NULL' and total_param == 0:
                    flagScan = self.dcm_network_handler.get_scanning_result(self.dcm_iface)
                    if not flagScan:
                        self.debug(1, self.ACT_NEG, 2,
                                   'Error\'s occured while scanning available wifi networks')
            elif self.cmd == 'connect':
                profile = self.list_param[0]
                if self.dcm_iface != 'NULL' and total_param == 1:
                    self.debug(1, self.ACT_SYSTEM, 0, 'Connecting interface \'' +
                               self.dcm_iface + '\' to profile \'' + profile + '\'')
                    self.dcm_connection_handler.connect_profile(self.dcm_iface, profile)
            elif self.cmd == 'back' and total_param == 0:
                self.dcm_iface = 'NULL'
                self.history_loc.pop()
            elif self.cmd == 'help' and total_param == 0:
                self.dcm_help_handler.show_help()
        except Exception as e:
            print (e)

    def parsing(self):
        list_command = self.command.split(' ')
        self.list_param = []
        self.cmd = list_command[0]
        del list_command[0]
        for param in list_command:
            self.list_param.append(param)

        if self.loc_now == self.LOC_DASHBOARD and self.cmd in self.LIST_CMD_DASHBOARD:
            self.action_dashboard()
        elif self.loc_now == self.LOC_DASHBOARD_WIZARD_WIFI and self.cmd in self.LIST_CMD_DASHBOARD_WIZARD_WIFI:
            self.action_dashboard_wizard_wifi()

    flagExit = False

    def standby(self):
        self.history_loc = [self.LOC_DASHBOARD]
        self.dcm_iface = 'NULL'

        while True:
            try:
                self.resolve_loc()
                self.command = raw_input(self.pre())
                self.parsing()
            except:
                break

            if self.flagExit:
                break
