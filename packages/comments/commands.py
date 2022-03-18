from cleo import Command
from packages.core.utils.app_loop import AppLoop

from .ctrls import CommentsScraper


class AllCommands:

    class Scraper(Command):
        """
        Scraper platzi comments lesson

        comments:scraper
        {--browser-profile-name= : profile-name}
        """

        def handle(self):
            browser_profile_name = self.option('browser-profile-name')
            AppLoop().get_loop().run_until_complete(
                CommentsScraper(browser_profile_name).run()
            )
