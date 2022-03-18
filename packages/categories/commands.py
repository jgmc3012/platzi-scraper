from cleo import Command
from packages.core.utils.app_loop import AppLoop

from .ctrls import CategoriesScraper

class AllCommands:


    class Scraper(Command):
        """
        Scraper platzi categories

        categories:scraper
        """

        def handle(self):
            AppLoop().get_loop().run_until_complete(
                CategoriesScraper().run()
            )
