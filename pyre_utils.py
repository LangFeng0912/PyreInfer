from typing import Optional, Tuple

from os.path import join, exists

from libcst import List

import json
import subprocess


def run(cmd_args: List[str], timeout: Optional[int] = None
        ) -> Tuple[str, str, int]:
    process = subprocess.run(cmd_args, shell=True, capture_output=True, timeout=timeout)
    return process.stdout.decode(), process.stderr.decode(), process.returncode


def new_pyre_config(project_path):
    # add pyre initiation file for the path
    pyre_dict = {
        "site_package_search_strategy": "pep561",
        "source_directories": [
            "."
        ],
        "typeshed": "/pyre-check/stubs/typeshed/typeshed-master"
    }

    if not exists(join(project_path, '.pyre_configuration')):
        with open(join(project_path, '.pyre_configuration'), "w") as f:
            json.dump(pyre_dict, f)


def new_watchman_config(project_path):
    # add the watchman config to the project
    watchman_dict = {"root": "."}
    if not exists(join(project_path, '.watchmanconfig')):
        with open(join(project_path, '.watchmanconfig'), "w") as f:
            json.dump(watchman_dict, f)


def start_watchman(project_path: str):
    # start watchman for the project
    stdout, stderr, r_code = run(
        "cd %s; watchman watch-project ." % project_path)
    print(f"[WATCHMAN] started at {project_path} ", stdout, stderr)


def start_pyre_server(project_path: str):
    # start pyre server for the project
    stdout, stderr, r_code = run(
        "cd %s; pyre start" % project_path)
    print(f"[PYRE_SERVER] initialized at {project_path} ", stdout, stderr)


def pyre_infer(project_path: str):
    # start pyre server for the project
    stdout, stderr, r_code = run(
        "cd %s; pyre infer; pyre infer -i --annotate-from-existing-stubs" % project_path)
    print(f"[PYRE_SERVER] initialized at {project_path} ", stdout, stderr)


def pyre_server_shutdown(project_path: str):
    # stop pyre server in the project path
    stdout, stderr, r_code = run("cd %s ; pyre stop" % project_path)
    print(f"[PYRE_SERVER] initialized at {project_path} ", stdout, stderr)
