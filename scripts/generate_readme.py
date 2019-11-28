#!/usr/bin/env python

import argparse
import io
import os
import re
import sys

AUR_USER = 'aexl'

# Prefer to show links to the development repository instead
# to e.g. PyPI
PROJECT_LINKS = {
    'kodi-addon-checker': 'https://github.com/xbmc/addon-check',
    'python-tableone': 'https://github.com/tompollard/tableone',
}


def main():
    parser = argparse.ArgumentParser(
        description='Generate README.md for github')
    parser.add_argument(
        '--check', '-c', action='store_true',
        help='Check if the current README.md matches the output of the script')
    args = parser.parse_args()
    if args.check:
        if check():
            print('No update of README.md needed.')
        else:
            print('README.md needs to be updated.')
            sys.exit(1)
    else:
        print(generate_readme(), end='')


def get_dir_names():
    return sorted([d for d in os.listdir('..') if os.path.isdir(
        os.path.join('..', d)) and '.SRCINFO' in os.listdir(
            os.path.join('..', d))])


def parse_package_info(pkgname):
    srcinfo = os.path.join('..', pkgname, '.SRCINFO')
    d = {
        'name': pkgname,
    }
    regex_template = r'%s\s*=\s*(.+)'
    with open(srcinfo, 'r') as f:
        content = f.read()
        for k in ('pkgdesc', 'pkgver', 'url', 'license'):
            reg = regex_template % k
            value = re.search(reg, content).group(1)
            d.update({k: value})
    return d


def generate_readme():
    title = '# AUR (Arch User Repository) Packages'
    description = ('My [aur](https://aur.archlinux.org/packages/'
                   '?K=%s&SeB=m) packages.' % AUR_USER)
    packages = [parse_package_info(name) for name in get_dir_names()]

    sio = io.StringIO('')
    sio.writelines([title, '\n\n', description, '\n\n## Packages\n\n'])

    sio.writelines(
        '| Name | Description | License | Project page | AUR page | Version |')
    sio.writelines('\n')
    sio.writelines('|---|---|---|:---:|:---:|---:|')
    sio.writelines('\n')

    pline_template = ('| **%s** | %s | %s | [:heavy_check_mark:](%s) '
                      '| [:heavy_check_mark:](%s) | %s |')
    for p in packages:
        url = PROJECT_LINKS.get(p['name'])
        url = url if url else p['url']
        line = pline_template % (
                p['name'], p['pkgdesc'], p['license'],
                url, 'https://aur.archlinux.org/packages/%s/' % p['name'],
                p['pkgver'])
        sio.writelines(line)
        sio.writelines('\n')

    sio.seek(0)
    output = sio.read()
    sio.close()
    return output


def check():
    with open(os.path.join('..', 'README.md'), 'r') as f:
        current = f.read()
    return current == generate_readme()


if __name__ == '__main__':
    main()
