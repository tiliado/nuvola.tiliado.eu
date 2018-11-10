#!/usr/bin/env python3
# Copyright 2018 Jiří Janoušek <janousek.jiri@gmail.com>
# License: BSD-2-Clause. See file LICENSE for details.

import argparse
import json
import os
from typing import List

from circleci.api import Api

DEFAULT_USERNAME = 'tiliado'
STATUS_SUCCESSFUL = 'successful'
SCREENSHOT_PREFIX = 'home/circleci/workdir/keep/{sdk_branch}/screenshots/'
VCS_TYPE_GITHUB = 'github'
XDG_CONFIG_HOME = os.environ.get(
    'XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
CIRCLE_CI_CONFIG = os.path.join(XDG_CONFIG_HOME, 'circleci/circleci.json')
CIRCLECI_TOKEN_VARIABLE = 'CIRCLECI_TOKEN'


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t', '--token', help='Circle CI token.', type=str)
    parser.add_argument(
        '-u', '--username', help='Circle CI username.',
        type=str, default=DEFAULT_USERNAME)
    parser.add_argument(
        '-a', '--app', help='Web app id, e.g. "google_play_music".', type=str)
    parser.add_argument(
        '-A', '--app-list', help='List of apps.',
        type=str, default='data/apps.json')
    parser.add_argument(
        '-s', '--sdk-branch', help='Nuvola SDK branch.',
        type=str, default='stable')
    parser.add_argument(
        '-b', '--app-branch', help='Web app repository branch.',
        type=str, default='master')
    parser.add_argument(
        '-o', '--output-dir', help='Output directory.',
        type=str, default='./screenshots/apps')
    args = parser.parse_args(argv[1:])

    token = args.token or os.environ.get(CIRCLECI_TOKEN_VARIABLE)
    if not token:
        try:
            with open(CIRCLE_CI_CONFIG) as fh:
                token = json.load(fh).get('token')
        except FileNotFoundError:
            pass
    if not token:
        print('No Circle CI token was specified. Tried:')
        print('1. --token parameter')
        print('2.', CIRCLECI_TOKEN_VARIABLE, 'environment variable')
        print('3. "token" key of', CIRCLE_CI_CONFIG)
        return 1

    if args.app:
        apps = [args.app]
    else:
        with open(args.app_list) as fh:
            apps = [app['id'] for app in json.load(fh)]

    circle = Api(token)
    for app in apps:
        app_path_name = app.replace('_', '-')
        app_repo = 'nuvola-app-' + app_path_name
        output_dir = os.path.join(args.output_dir, app)
        artifacts = get_artifacts(
            circle, args.username, app_repo, args.app_branch)
        download_artifacts(
            circle, artifacts, args.sdk_branch, output_dir)
    return 0


def get_artifacts(
        circle: Api, username: str, app_repo: str, app_branch: str) -> list:
    return circle.get_latest_artifact(
        username, app_repo,
        branch=app_branch,
        status_filter=STATUS_SUCCESSFUL,
        vcs_type=VCS_TYPE_GITHUB)


def download_artifacts(
        circle: Api, artifacts: list, sdk_branch: str,
        output_dir: str) -> None:
    print('Output directory:', output_dir)
    os.makedirs(output_dir, exist_ok=True)

    for artifact in artifacts:
        path: str = artifact['path']
        prefix = SCREENSHOT_PREFIX.format(sdk_branch=sdk_branch)
        if path.startswith(prefix) and path.endswith('.png'):
            url = artifact['url']
            print('Downloading:', url)
            circle.download_artifact(url, destdir=output_dir)


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
