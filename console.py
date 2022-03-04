#!/usr/local/bin/python
from cleo import Application
from packages.core.utils.app_loop import AppLoop
from packages.core.modules import ModuleManager
from packages.core.utils.logger import Logger
from packages.core.db import init_db
from tortoise import run_async
from socket import gaierror
from clikit.args.argv_args import ArgvArgs

if __name__ == '__main__':
    application = Application("Commands", 0.1, complete=True)
    AppLoop()
    ModuleManager().import_commands(application)
    Logger()
    try:
        AppLoop().get_loop().run_until_complete(init_db())
    except gaierror as e:
        if 'pyppeteer:open_browser' not in ArgvArgs().tokens:
            raise e 
    application.run()
