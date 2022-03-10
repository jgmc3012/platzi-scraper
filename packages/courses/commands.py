from cleo import Command
from packages.core.utils.app_loop import AppLoop

from .ctrls import CoursesScraper, ReviewsScraper

class AllCommands:


    class ScraperCourses(Command):
        """
        Scraper platzi courses

        courses:scraper
        {--browser-profile-name= : profile-name}
        """

        def handle(self):
            browser_profile_name = self.option('browser-profile-name')
            AppLoop().get_loop().run_until_complete(
                CoursesScraper(browser_profile_name).run()
            )

    class ScraperReviews(Command):
        """
        Scraper platzi reviews

        courses:scraper_reviews
        {--browser-profile-name= : profile-name}
        """

        def handle(self):
            browser_profile_name = self.option('browser-profile-name')
            AppLoop().get_loop().run_until_complete(
                ReviewsScraper(browser_profile_name).run()
            )
