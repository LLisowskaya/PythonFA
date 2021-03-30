from pathlib import Path
import os

import configparser

from core import FMCore

CONFIG_DIR = os.path.join(Path.home(), '.own-fm')
CONFIG_FILE = 'config.ini'
CONFIG_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE)
DEFAULT_STRUCT = {
    'default': {
        'work_dir': ''
    }
}

def main():
    # Create config file, if it doesn't exist.
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'a'):
            os.utime(CONFIG_PATH, None)

    # Create config parser.
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    if not config.sections():
        for v, k in DEFAULT_STRUCT.items():
            config[v] = k

    # Create File Manager instance.
    fmcore = FMCore()

    # Set work and current directories.
    fmcore.work_dir = config['default']['work_dir']
    fmcore.current_dir = fmcore.work_dir

    fmcore.message("Type 'show_help' to display help.")
    while True:
        # If work_dir isn't in the config, promt user.
        if not fmcore.work_dir:
            fmcore.work_dir = fmcore.prompt(
                "Choose work directory (absolute path):")

            # Save config, if dir exists.
            if os.path.isdir(fmcore.work_dir):
                config['default']['work_dir'] = fmcore.work_dir
                fmcore.current_dir = fmcore.work_dir
                with open(CONFIG_PATH, 'w') as file:
                    config.write(file)
            else:
                fmcore.error("Wrong path, try again.")
                continue
        
        # User input.
        stdin = fmcore.prompt(f"{fmcore.current_dir} >")
        params = stdin.split()

        # If var 'params' has less than 3 args, then add empty str.
        if len(params) < 3:
            params.extend(['', ''])

        if 'show_help' in params:
            fmcore.show_help()

        elif 'create_dir' in params:
            fmcore.create_dir(params[1])

        elif 'delete_dir' in params:
            fmcore.delete_dir(params[1])

        elif 'show_content' in params:
            fmcore.show_content(params[1])

        elif 'change_cur_dir' in params:
            fmcore.change_cur_dir(params[1])

        elif 'change_work_dir' in params:
            fmcore.change_work_dir(params[1])
            config['default']['work_dir'] = fmcore.work_dir
            with open(CONFIG_PATH, 'w') as file:
                config.write(file)

        elif 'show_cur_dir' in params:
            fmcore.show_cur_dir()

        elif 'show_work_dir' in params:
            fmcore.show_work_dir()

        elif 'create_emptyf' in params:
            fmcore.create_emptyf(params[1])

        elif 'delete_file' in params:
            fmcore.delete_file(params[1])

        elif 'copy_file' in params:
            fmcore.copy_file(params[1], params[2])

        elif 'move_file' in params:
            fmcore.move_file(params[1], params[2])

        elif 'rename_file' in params:
            fmcore.rename_file(params[1], params[2])

        elif 'write_to_file' in params:
            fmcore.write_to_file(params[1], params[2])

        elif 'quit' in params:
            fmcore.quit()

if __name__ == '__main__':
    main()
