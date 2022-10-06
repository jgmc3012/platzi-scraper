from cleo import Command
from packages.core.utils.app_loop import AppLoop
from packages.my_pyppeteer.ctrls import MyPyppeteer


class AllCommands:

    class OpenPyppeteerBrowser(Command):
        """
        Open Pyppeteer Browser

        pyppeteer:open_browser
        {--args= : nothing extra by default}
        {--gui : Using a graphical user interface?}
        """

        def handle(self):

            headless = not self.option('gui')
            args = self.option('args')
            args = args.split(',') if args else []
            AppLoop().get_loop().run_until_complete(MyPyppeteer().open_browser(headless=headless, args=args))

    class CommandCountPages(Command):
        """
        Run count pages

        pyppeteer:count_pages
        """

        def handle(self):
            AppLoop().get_loop().run_until_complete(MyPyppeteer().count_pages())

    class CommandProfileName(Command):
        """
        Run rotate_pages

        pyppeteer:rotate_pages
        """

        def handle(self):
            AppLoop().get_loop().run_until_complete(MyPyppeteer().start_rotate_pages())