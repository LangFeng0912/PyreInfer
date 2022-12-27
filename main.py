import argparse
import os

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
        g = os.walk(project_path)
        for path, dir_list, file_list in g:
            for dir_name in dir_list:
                # print(os.path.join(path, dir_name))
                author_list.append(os.path.join(path, dir_name))
    else:
        print("Error: Project Path %s does not exist", project_path)
    repo_list = []
    for author_path in author_list:
        if os.path.exists(author_path):
            g = os.walk(author_path)
            for path, dir_list, file_list in g:
                for dir_name in dir_list:
                    # print(os.path.join(path, dir_name))
                    repo_list.append(os.path.join(author_path, dir_name))
        else:
            print("Error: Author Path %s does not exist", author_path)
    for repo in repo_list:
        if os.path.exists(repo):
            pyre_pipeline(repo)
            print("Pyre Infer in %s has done..." % repo)



def main():
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--o', type=str, default=None)
    args = parser.parse_args()
    project_path = args.o
    print(project_path)


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
