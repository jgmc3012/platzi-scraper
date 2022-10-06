from cleo import Command
from packages.core.utils.app_loop import AppLoop

from .scraper import CareersScraper, CoursesScraper


class AllCommands:

    class Scraper(Command):
        """
        Scraper platzi careers for all categories

        careers:scraper
        """

        def handle(self):
            AppLoop().get_loop().run_until_complete(
                CareersScraper().run()
            )


    class CourseScraper(Command):
        """
        Create and linked all careers with their courses

        careers:link_courses
        """

        def handle(self):
            AppLoop().get_loop().run_until_complete(
                CoursesScraper().run()
            )
