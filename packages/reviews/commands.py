from cleo import Command
from packages.core.utils.app_loop import AppLoop

from .ctrls import ReviewsScraper

class AllCommands:

    class Scraper(Command):
        """
        Scraper review for all courses

        reviews:scraper
        {--browser-profile-name= : profile-name}
        """

        def handle(self):
            browser_profile_name = self.option('browser-profile-name')
            AppLoop().get_loop().run_until_complete(
                ReviewsScraper(browser_profile_name).run()
            )
