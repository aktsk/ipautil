#!/usr/bin/env python3
# coding: UTF-8

import plistlib

from colorama import Fore


class InfoPlistUtil(object):

    def __init__(self, info_plist_path):
        self.info_plist_dict = ""
        with open(info_plist_path, 'rb') as fp:
            self.info_plist_dict = plistlib.load(fp)

    def get_package_name(self):
        print('CFBundleName:')
        try:
            print(Fore.CYAN + self.info_plist_dict['CFBundleName'])
        except KeyError as e:
            print(Fore.RED + 'None')

        print('\nCFBundleDisplayName:')
        try:
            print(Fore.CYAN + self.info_plist_dict['CFBundleDisplayName'])
        except KeyError as e:
            print(Fore.RED + 'None')
        print('')


    def check_ATS(self):
        print('Checking AppTransportSecurity...')
        try:
            if self.info_plist_dict['NSAppTransportSecurity']['NSAllowsArbitraryLoads']:
                print(Fore.RED + 'True\n')
                print('NSExceptionDomains:')
                try:
                    domains = self.info_plist_dict['NSAppTransportSecurity']['NSExceptionDomains']
                    for d in domains:
                        print(Fore.RED + d)

                except KeyError as e:
                    print('None')

                print('')
            else:
                print(Fore.BLUE + 'False\n')

        except KeyError as e:
            print(Fore.BLUE + 'False\n')


    def check_custom_schemas(self):
        print('Custom schemas (CFBundleURLSchemes):')
        try:
            for d in self.info_plist_dict['CFBundleURLTypes']:
                for schema in d['CFBundleURLSchemes']:
                    print(Fore.CYAN + schema)
        except KeyError as e:
            print(Fore.CYAN + 'None')
        print('')

    def check_all(self):
        self.get_package_name()
        self.check_ATS()
        self.check_custom_schemas()