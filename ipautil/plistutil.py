#!/usr/bin/env python3
# coding: UTF-8

from colorama import Fore


def get_package_name(info_plist_dict):
    try:
        print('CFBundleName:')
        print(Fore.BLUE + info_plist_dict['CFBundleName'])
    except KeyError as e:
        print(Fore.BLUE + 'None')
    print('')
    try:
        print('CFBundleDisplayName:')
        print(Fore.BLUE + info_plist_dict['CFBundleDisplayName'])
    except KeyError as e:
        print(Fore.BLUE + 'None')
    print('')


def check_ATS(info_plist_dict):
    print('Checking AppTransportSecurity...')
    try:
        if info_plist_dict['NSAppTransportSecurity']['NSAllowsArbitraryLoads']:
            print(Fore.RED + 'True\n')
            print('NSExceptionDomains:')
            try:
                domains = info_plist_dict['NSAppTransportSecurity']['NSExceptionDomains']
                for d in domains:
                    print(Fore.RED + d)

            except KeyError as e:
                print('None')

            print('')
        else:
            print(Fore.BLUE + 'False\n')

    except KeyError as e:
        print(Fore.BLUE + 'False\n')


def check_custom_schemas(info_plist_dict):
    print('Custom schemas:')
    try:
        for d in info_plist_dict['CFBundleURLTypes']:
            for schema in d['CFBundleURLSchemes']:
                print(Fore.BLUE + schema)
    except KeyError as e:
        print(Fore.BLUE + 'None')
    print('')
