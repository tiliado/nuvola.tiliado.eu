#!/usr/bin/env python3
import json
import shlex
from argparse import ArgumentParser
from typing import List, Any, Dict
import subprocess
import os
import yaml


def load_yaml(fp) -> Any:
    return yaml.load(fp, Loader = getattr(yaml, "CLoader", yaml.Loader))


def update_all(apps_list: str, branch: str, apps_dir: str, output: str) -> str:
    with open(apps_list) as f:
        recipes = load_yaml(f)

    list_of_apps: List[str] = recipes["apps"][branch]
    apps: List[Dict[str, Any]] = [update_app(apps_dir, app, "master") for app in list_of_apps]
    apps.sort(key=lambda item: item["name"])
    data = json.dumps(apps, indent=2, separators=(',', ': '), sort_keys=True, ensure_ascii=False)
    with open(output, "wt") as f:
        f.write(data)
        f.write("\n")
    return data


def update_app(apps_dir: str, app_spec: str, default_branch: str) -> Dict[str, Any]:
    app, branch = [s.strip() for s in app_spec.split("@")] if ("@" in app_spec) else (app_spec, default_branch)
    meta = json.loads(git_read_file(os.path.join(apps_dir, "nuvola-app-" + app), branch, "metadata.in.json"))
    return {
        "id": meta["id"],
        "uid": get_uid(meta["id"]),
        "name": meta["name"],
        "version": "%s.%s" % (meta["version_major"], meta.get("version_minor", 0)),
        "maintainer": meta["maintainer_name"],
        "maintainer_link": meta["maintainer_link"],
    }


def git_read_file(repo: str, branch: str, path:str) -> str:
    return getstdout("git -C {0} --no-pager show {1}:{2}".format(*[shlex.quote(x) for x in (repo, branch, path)]))


def getstdout(command: str, *, verbose: bool = False) -> str:
    if verbose:
        print(">", command)
    argv = shlex.split(command)
    try:
        return subprocess.check_output(argv, stderr=subprocess.STDOUT).decode("utf-8")
    except subprocess.CalledProcessError as e:
        e.output = e.output.decode("utf-8")
        raise e


def get_uid(app_id: str) -> str:
    app_id_unique = ["eu.tiliado.NuvolaApp"]
    for part in app_id.split("_"):
        app_id_unique.append(part[0].upper())
        app_id_unique.append(part[1:].lower())
    return "".join(app_id_unique)


def main(argv: List[str]) -> int:
    parser = ArgumentParser(prog=argv[0])
    parser.add_argument(
        "-l", "--apps-list", required=True,
        help="Path list of apps.")
    parser.add_argument(
        "-d", "--apps-dir", required=True,
        help="Path to directory with apps.")
    parser.add_argument(
        "-b", "--branch", default="stable",
        help="Branch of the flatpak repository.")
    parser.add_argument(
        "-o", "--output", default="data/apps.json",
        help="Path to output data file [data/apps.json].")
    params = parser.parse_args(argv[1:])
    print(update_all(params.apps_list, params.branch, params.apps_dir, params.output))
    return 0


if __name__ == "__main__":
    import sys

    # noinspection PyBroadException
    try:
        code = main(sys.argv)
    except Exception as e:
        import traceback

        print("Unexpected failure:", file=sys.stderr)
        traceback.print_exc()
        code = 2
    sys.exit(code)
