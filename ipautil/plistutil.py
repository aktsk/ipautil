#!/usr/bin/env python3
# coding: UTF-8

from colorama import Fore


def check_ATS(info_plist):
    try:
        if info_plist['NSAppTransportSecurity']['NSAllowsArbitraryLoads']:
            print(Fore.RED + 'True\n')
            print('NSExceptionDomains:')
            try:
                domains = info_plist['NSAppTransportSecurity']['NSExceptionDomains']
                for d in domains:
                    print(Fore.RED + d)

            except KeyError as e:
                print('None')

            print('')
        else:
            print(Fore.BLUE + 'False\n')

    except KeyError as e:
        print(Fore.BLUE + 'False\n')


def check_custom_schemas(info_plist):
    print('Custom schemas:')
    try:
        for d in info_plist['CFBundleURLTypes']:
            for schema in d['CFBundleURLSchemes']:
                print(Fore.BLUE + schema)
    except KeyError as e:
        print(Fore.BLUE + 'None')
    print('')
