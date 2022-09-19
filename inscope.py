#!/usr/bin/python3
import requests


USER_NAME = 'your user name here '
TOKEN = 'your token here'

def extract_assets(handler):

    url = 'https://api.hackerone.com/v1/hackers/programs/'+handler
    headers = {
        'Accept': 'application/json'
    }
    r = requests.get(url, auth=(USER_NAME, TOKEN), headers=headers)
    scope = []
    print('extracting assets')
    for domain in r.json()['relationships']['structured_scopes']['data']:
        scope.append(domain['attributes']['asset_identifier'])
    print(f"Total asset : {len(scope)}")
    for asset in scope:
        print(asset)
    return scope


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', type=str,                        required=True, help='handler of target to extract i')
    return parser.parse_args()


def banner():
    print("="*10)
    print(r"""
▀▀█▀▀ █▀▀█ █▀▀█ █▀▀▀ █▀▀ ▀▀█▀▀ █▀▀ █░█ 
░░█░░ █▄▄█ █▄▄▀ █░▀█ █▀▀ ░░█░░ █▀▀ ▄▀▄ 
░░▀░░ ▀░░▀ ▀░▀▀ ▀▀▀▀ ▀▀▀ ░░▀░░ ▀▀▀ ▀░▀
""")
    print("Extract assets from targets")


def make_project(target, scope):
    import os
    os.mkdir(target)
    with open(target+'/wildcard', 'w') as file:
        for asset in scope:
            file.write(asset.replace("*.", "") + "\n")


def main():
    banner()
    args = parse_args()
    scope = []
    if args.target:
        scope = extract_assets(args.target)
        make_project(args.target, scope)
    else:
        print("python inscope.py -t <program_name> ")


if __name__ == '__main__':
    main()
