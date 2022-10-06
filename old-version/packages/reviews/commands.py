from cleo import Command
from packages.core.utils.app_loop import AppLoop

from .scraper import ReviewsScraper

class AllCommands:

    class Scraper(Command):
        """
        Scraper review for all courses

        reviews:scraper
        """

        def handle(self):
            AppLoop().get_loop().run_until_complete(
                ReviewsScraper().run()
            )
