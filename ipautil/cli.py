#!/usr/bin/env python3
# coding: UTF-8

import argparse
import colorama
import glob
import os

from colorama import Fore, Back, Style
from . import util


def cmd_decode(args):
    print('Decoding IPA...')
    try:
        if util.decode(args.ipa_path):
            print(Fore.CYAN + 'Output: ./Payload')

    except:
        return


def cmd_build(args):
    print('Signing IPA by codesign...')
    try:
        if util.sign(args.payload_dir):
            print(Fore.CYAN + 'Signed\n')
    except:
        return

    print('Building IPA...')
    ipa_path = args.output
    if args.output is None:
        app_path = glob.glob(os.path.join(args.payload_dir, '**.app'))[0]
        ipa_path = app_path.split('/')[-1].replace(' ', '_') + ".patched.ipa"
    try:
        util.build(args.payload_dir, ipa_path)
    except Exception as e:
        return

    print(Fore.CYAN + 'Output: ' + ipa_path)


def cmd_sign(args):
    print('Signing IPA by codesign...')
    try:
        if util.sign(args.payload_dir):
            print(Fore.CYAN + 'Signed')
    except:
        return


def main():
    colorama.init(autoreset=True)
    parser = argparse.ArgumentParser(description='ipa patcher')
    subparsers = parser.add_subparsers()

    parser_decode = subparsers.add_parser('decode', aliases=['d'], help='')
    parser_decode.add_argument('ipa_path', help='')
    parser_decode.set_defaults(handler=cmd_decode)

    parser_build = subparsers.add_parser('build', aliases=['b'], help='')
    parser_build.add_argument('payload_dir', help='')
    parser_build.add_argument('--output', '-o')
    parser_build.set_defaults(handler=cmd_build)

    parser_sign = subparsers.add_parser('sign', aliases=['s'], help='')
    parser_sign.add_argument('payload_dir', help='')
    parser_sign.set_defaults(handler=cmd_sign)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
