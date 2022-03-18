from cleo import Command
from packages.core.utils.app_loop import AppLoop

from .ctrls import CoursesScraper

class AllCommands:


    class Scraper(Command):
        """
        Scraper platzi courses

        courses:scraper
        """

        def handle(self):
            AppLoop().get_loop().run_until_complete(
                CoursesScraper().run()
            )
