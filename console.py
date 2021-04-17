from cleo import Application
from packages.core.utils.app_loop import AppLoop
from packages.core.modules import ModuleManager
from packages.core.utils.logger import Logger
from packages.core.db import init_db


if __name__ == '__main__':
    application = Application("Commands", 0.1, complete=True)
    AppLoop()
    ModuleManager().import_commands(application)
    Logger()
    # AppLoop().get_loop().run_until_complete(init_db())
    application.run()
