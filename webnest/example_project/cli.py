import argparse
import shutil
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from path import append_file, CopyFiles
import state_colors

def collect_app(name):
    # Define paths
    base_path = os.path.dirname(__file__)
    files_to_copy = ['__init__.py','models.py','handle.py','routes.py','Mydb.sqlite3']
    folders_to_copy = []

    # Define target directory based on the provided name
    target_dir = f'{name}'
    os.makedirs(target_dir, exist_ok=True)

    # Copy
    def Copy(file_name ,func):
        return CopyFiles(file_name,func, base_path=base_path,target_dir=target_dir)

    for file_name in files_to_copy:Copy(file_name,shutil.copy)
    append_file(Copy('settings.py',shutil.copy) ,f"APP_NAME = '{name}'")

    # Copy template files , static
    Copy('templates',shutil.copytree)
    Copy('static',shutil.copytree)

    print(f"{state_colors.CYAN} - Your Project Created successfully {state_colors.WHITE}{target_dir}")

def main():
    parser = argparse.ArgumentParser(description="Collect an example project from the package.")
    subparsers = parser.add_subparsers(dest='command', help='Subcommand to execute')
    
    createproject_parser = subparsers.add_parser('createproject', help='Create a new project')
    createproject_parser.add_argument('project_name', help='Name of the project to create')

    args = parser.parse_args()

    if args.command == "createproject":
        collect_app(args.project_name)
    else:
        parser.print_help()
if __name__ == '__main__':
    main()
