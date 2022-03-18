from cleo import Command
from packages.core.utils.app_loop import AppLoop

from .ctrls import LessonsScraper

class AllCommands:


    class Scraper(Command):
        """
        Scraper platzi lessons

        lessons:scraper
        """

        def handle(self):
            AppLoop().get_loop().run_until_complete(
                LessonsScraper().run()
            )
