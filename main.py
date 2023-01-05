import argparse
import os
import pandas as pd
import time

from pyre_utils import new_pyre_config, new_watchman_config, start_watchman, start_pyre_server, pyre_infer, \
    pyre_server_shutdown


def pyre_pipeline(repo_path):
    new_pyre_config(repo_path)
    new_watchman_config(repo_path)
    start_watchman(repo_path)
    start_pyre_server(repo_path)
    pyre_infer(repo_path)
    pyre_server_shutdown(repo_path)


def walk_folder(project_path):
    author_list = []
    if os.path.exists(project_path):
        files = os.listdir(project_path)
        for file in files:
            m = os.path.join(project_path, file)
            if (os.path.isdir(m)):
                author_list.append(m)
    else:
        print("Error: Project Path %s does not exist", project_path)
    authd = pd.DataFrame(data=author_list)
    authd.to_csv('authorlist.csv')
    repo_list = []
    for author_path in author_list:
        if os.path.exists(author_path):
            files = os.listdir(author_path)
            for file in files:
                m = os.path.join(author_path, file)
                if (os.path.isdir(m)):
                    repo_list.append(m)

        else:
            print("Error: Author Path %s does not exist", author_path)
    repod = pd.DataFrame(data=repo_list)
    repod.to_csv('repolist.csv')
    i = 1
    for repo in repo_list:
        if os.path.exists(repo):
            if i%100 == 0:
                print("sleeping...")
                time.sleep(5)
            pyre_pipeline(repo)
            print("Pyre Infer in %s has done..." % repo)
            print("Project %s is finished..." % i)
            i = i+1


def main():
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--o', type=str, default=None)
    args = parser.parse_args()
    project_path = args.o
    print(project_path)
    walk_folder(project_path)


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
