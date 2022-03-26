from cleo import Command
from packages.core.utils.app_loop import AppLoop

from .scraper import LessonsScraper

class AllCommands:


    class Scraper(Command):
        """
        Get all information about lessons

        lessons:link_comments
        """

        def handle(self):
            AppLoop().get_loop().run_until_complete(
                LessonsScraper().run()
            )
