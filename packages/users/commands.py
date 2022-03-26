from cleo import Command
from packages.core.utils.app_loop import AppLoop

from .ctrls import UserScraper

class AllCommands:

    class Scraper(Command):
        """
        Users

        users:scraper_profile
        """

        def handle(self):
            AppLoop().get_loop().run_until_complete(UserScraper().run())
