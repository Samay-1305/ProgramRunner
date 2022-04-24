import argparse
import shutil
import json
import stat
import uuid
import os


class ColorCodes:
    """
    List of colors to modify look of the terminal output
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DEFAULT = '\033[0m'


class ErrorCodes:
    """
    Error texts for program runner
    """
    script_not_found = f'{ColorCodes.FAIL}ERROR: NO CONFIG FOUND{ColorCodes.DEFAULT}'
    help_text = 'Execute pr --help for more info'


class ProgramRunner:
    """
    Class to handle running of program scripts
    """
    def __init__(self, config_path:str) -> None:
        """
        To initialize an instance of Program Runner
        """
        self.__config_path = config_path
        self.__config = json.load(open(config_path, 'r'))
        self.__storage_dir = self.__config.get('storage-dir', None)
        if self.__storage_dir is None:
            self.__storage_dir = "/".join(config_path.split("/")[:-2] +\
                ['scripts'])
            self.__config['storage-dir'] = self.__storage_dir
            self.save()

    def create_parser(self)->dict:
        """
        To parse command line arguments
        """
        ap = argparse.ArgumentParser()
        ap.add_argument('-n', '--new',
            action='store_true',
            help='Create a new config')
        ap.add_argument('-d', '--del',
            action='store_true',
            help='Edit current config')
        ap.add_argument('-e', '--edit',
            action='store_true',
            help='Delete a config')
        ap.add_argument('-p', '--print',
            action='store_true',
            help='Print a config')
        ap.add_argument('-s', '--setup',
            action='store_true',
            help='Run the setup')
        ap.add_argument('-f', '--file',
            type=str,
            default=None,
            help='Input config file')
        return ap

    def execute(self) -> None:
        """
        To manage shell scripts
        """
        parser = self.create_parser()
        args = vars(parser.parse_args())
        path = os.getcwd()
        path_key = f"key{path.replace('/', '-')}"
        script_name = self.__config['scripts'].get(path_key, None)
        if ((args['new'] or args['edit'] or args['file']) and args['del']) or \
            (args['edit'] and args['file']):
            parser.print_help()
            quit()
        if args['setup']:
            storage_dir = input(f'Script storage dir [{self.__storage_dir}]:')
            if len(storage_dir.strip()) > 0:
                self.__storage_dir = storage_dir.strip()
                self.__config['storage-dir'] = self.__storage_dir
            self.save()
        if not any(args.values()):
            if script_name is None:
                print(ErrorCodes.script_not_found)
                print(f'{ErrorCodes.help_text}\n')
                quit()
            script_dir = os.path.join(self.__storage_dir, 'scripts')
            os.system(f'{script_dir}/./{script_name}')
        if args['del']:
            if script_name is None:
                print(ErrorCodes.script_not_found)
                print(f'{ErrorCodes.help_text}\n')
                quit()
            inp = input('Found existing script, delete? [Y/n]')\
                .lower().strip()
            if inp == 'n':
                quit()
            script_path = os.path.join(self.__storage_dir, 'scripts',
                script_name)
            os.remove(script_path)
            self.__config['scripts'].pop(path_key)
            self.save()
            print('Succesfully deleted script')
        if args['new']:
            if script_name is not None:
                inp = input('Found existing script, overwrite? [Y/n]')\
                    .lower().strip()
                if inp == 'n':
                    quit()
            else:
                script_name = f'{uuid.uuid4()}.sh'
            self.__config['scripts'][path_key] = script_name
            script_path = os.path.join(self.__storage_dir, 'scripts',
                script_name)
            with open(script_path, 'w') as f:
                f.write("echo 'Program Runner v0.1-alpha'\n")
                f.write(f"echo 'Script Name: {script_name}'\n")
            st = os.stat(script_path)
            os.chmod(script_path, st.st_mode | stat.S_IEXEC)
            self.save()
            if args['file']:
                shutil.copyfile(args['file'], script_path)
        if args['edit']:
            if script_name is None:
                print(ErrorCodes.script_not_found)
                print(f'{ErrorCodes.help_text}\n')
                quit()
            if args['file']:
                shutil.copyfile(args['file'], script_path)
            else:
                script_path = os.path.join(self.__storage_dir, 'scripts',
                    script_name)
                os.system(f'vim {script_path}')
        if args['print']:
            script_path = os.path.join(self.__storage_dir, 'scripts',
                script_name)
            with open(script_path, 'r') as f:
                print(f.read())
        

    def save(self):
        """
        To save the new config file
        """
        with open(self.__config_path, 'w') as fp:
            json.dump(self.__config, fp, indent=4)
            