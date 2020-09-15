#!/usr/bin/env python3
# coding: UTF-8

import glob
import json
import os
import plistlib
import shutil
import subprocess

from . import plistutil
from colorama import Fore


def decode(ipa_path):
    if os.path.isdir('./Payload'):
        input_pattern = {'y': True, 'yes': True, 'n': False, 'no': False}
        answer = input('The Payload directory already exists. Do you want to delete it? [Y/n]: ').lower()
        if input_pattern[answer]:
            shutil.rmtree('./Payload')
            print('Deleted Payload directory.')
        else:
            return False
        
    unzip_cmd = ['unzip']
    unzip_cmd.extend([ipa_path])

    try:
        proc = subprocess.Popen(unzip_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outs, errs = proc.communicate()
        if (outs is not None) and (len(outs) != 0):
            print(outs.decode('ascii'))
        
        if (errs is not None) and (len(errs) != 0):
            print(errs.decode('ascii'))
            raise Exception

    except FileNotFoundError as e:
        print('unzip not found.')
    
    print('Checking AppTransportSecurity...')
    app_path = glob.glob(os.path.join('./Payload', '**.app'))[0]
    info_plist_path = os.path.join(app_path, 'Info.plist')
    with open(info_plist_path, 'rb') as fp:
        pl = plistlib.load(fp)
        plistutil.check_ATS(pl)
        plistutil.check_custom_schemas(pl)


    return True


def build(payload_dir, ipa_name):
    zip_cmd = ['zip']
    zip_cmd.extend(['-ry', ipa_name, payload_dir])
    try:
        proc = subprocess.Popen(zip_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outs, errs = proc.communicate()
        if (outs is not None) and (len(outs) != 0):
            print(outs.decode('ascii'))
        
        if (errs is not None) and (len(errs) != 0):
            print(errs.decode('ascii'))
            raise Exception

    except FileNotFoundError as e:
        print('zip not found.')


def sign(payload_path):
    home_dir = os.environ['HOME']
    entitlements_plist_path = ''
    embedded_mobileprovision_path = ''

    try:
        with open(home_dir + "/ipautil.json") as f:
            config = json.load(f)
            entitlements_plist_path = config['entitlements-plist'].replace('~', home_dir)
            embedded_mobileprovision_path = config['embedded-mobileprovision'].replace('~', home_dir)

    except:
        print('Please place `~/ipautil.json` containing entitlements.plist path and embedded.mobileprovision path')
        return False

    try:
        if not os.path.isdir(payload_path):
            print('{0} is not found.'.format(payload_path))
            raise Exception

        if not os.path.isfile(entitlements_plist_path):
            print('{0} is not found.'.format(entitlements_plist_path))
            raise Exception

        if not os.path.isfile(embedded_mobileprovision_path):
            print('{0} is not found.'.format(embedded_mobileprovision_path))
            raise Exception

        signature_string = fetch_signature_string()
        if not signature_string:
            print('Codesigning is not found.')
            raise Exception

        app_path = glob.glob(os.path.join(payload_path, '**.app'))[0]        
        shutil.copyfile(embedded_mobileprovision_path, os.path.join(app_path, 'embedded.mobileprovision'))
        
        for framework_file in glob.glob(os.path.join(app_path, 'Frameworks/*')):
            outs, errs = run_codesign(framework_file, signature_string, entitlements_plist_path)
            if (outs is not None) and (len(outs) != 0):
                print(outs.decode('ascii'), end='')
            
            if (errs is not None) and (len(errs) != 0):
                print(errs.decode('ascii'), end='')

        for plugin_file in glob.glob(os.path.join(app_path, 'PlugIns/*')):
            outs, errs = run_codesign(plugin_file, signature_string, entitlements_plist_path)
            if (outs is not None) and (len(outs) != 0):
                print(outs.decode('ascii'))
            
            if (errs is not None) and (len(errs) != 0):
                print(errs.decode('ascii'))
        
        outs, errs = run_codesign(app_path, signature_string, entitlements_plist_path)
        if (outs is not None) and (len(outs) != 0):
            print(outs.decode('ascii'), end='')
        
        if (errs is not None) and (len(errs) != 0):
            print(errs.decode('ascii'), end='')
        
        return True

    except (IndexError, FileNotFoundError) as e:
        print('codesign not found.')
        return False
    

def fetch_signature_string():
    security_cmd = ['security']
    security_cmd.extend(['find-identity', '-p', 'codesigning', '-v'])
    proc = subprocess.Popen(security_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errs = proc.communicate()
    if (errs is not None) and (len(errs) != 0):
        print(errs.decode('ascii'))
        return False

    outs = outs.decode('ascii')
    begin = outs.find('1) ') + 3
    end = outs.find(' "iPhone Developer')
    return outs[begin: end]


def run_codesign(target_path, signature_string, entitlements_plist_path):
    codesign_cmd = ['codesign']
    codesign_cmd.extend(['--force', '--sign', signature_string, '--entitlements', entitlements_plist_path])
    codesign_cmd.extend([target_path])
    proc = subprocess.Popen(codesign_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errs = proc.communicate()
    return outs, errs
    