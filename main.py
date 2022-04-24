from modules.program_runner import ProgramRunner

import os

PROGRAM_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(PROGRAM_DIR, 'storage', 'config', 'config.json')

if __name__ == '__main__':
    app = ProgramRunner(CONFIG_PATH)
    app.execute()