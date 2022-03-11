from cleo import Command
from packages.core.utils.app_loop import AppLoop

from .ctrls import LessonsScraper, CommentsScraper

class AllCommands:


    class ScraperLessons(Command):
        """
        Scraper platzi lessons

        lessons:scraper
        {--browser-profile-name= : profile-name}
        """

        def handle(self):
            browser_profile_name = self.option('browser-profile-name')
            AppLoop().get_loop().run_until_complete(
                LessonsScraper(browser_profile_name).run()
            )

    class ScraperComment(Command):
        """
        Scraper platzi comments lesson

        lessons:scraper_comments
        {--browser-profile-name= : profile-name}
        """

        def handle(self):
            browser_profile_name = self.option('browser-profile-name')
            AppLoop().get_loop().run_until_complete(
                CommentsScraper(browser_profile_name).run()
            )
