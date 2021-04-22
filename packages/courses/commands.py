from cleo import Command
from packages.core.utils.app_loop import AppLoop

from .ctrls import CoursesScraper, ReviewsScraper

class AllCommands:


    class ScraperCourses(Command):
        """
        Scraper platzi courses

        scraper:platzi_courses
        """

        def handle(self):
            AppLoop().get_loop().run_until_complete(
                CoursesScraper().run()
            )

    class ScraperReviews(Command):
        """
        Scraper platzi reviews

        scraper:platzi_reviews
        """

        def handle(self):
            AppLoop().get_loop().run_until_complete(
                ReviewsScraper(sem=5).run()
            )
