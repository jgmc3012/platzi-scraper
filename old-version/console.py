#!/usr/local/bin/python
from cleo import Application
from clikit.args.argv_args import ArgvArgs
from tortoise import Tortoise

from packages.core.db import init_db
from packages.core.modules import ModuleManager
from packages.core.utils.app_loop import AppLoop
from packages.core.utils.logger import Logger

if __name__ == '__main__':
    application = Application("Commands", 0.1, complete=True)
    AppLoop()
    ModuleManager().import_commands(application)
    Logger()
    
    command_pyppeteer = 'pyppeteer:open_browser' in ArgvArgs().tokens
    if not command_pyppeteer:
        AppLoop().get_loop().run_until_complete(init_db())

    application.run()

    if not command_pyppeteer:
        AppLoop().get_loop().run_until_complete(Tortoise.close_connections())
