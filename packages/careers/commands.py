from cleo import Command
from packages.core.utils.app_loop import AppLoop

from .ctrls import CareersScraper


class AllCommands:

    class Scraper(Command):
        """
        Scraper platzi careers for all categories

        careers:scraper
        {--browser-profile-name= : profile-name}
        """

        def handle(self):
            browser_profile_name = self.option('browser-profile-name')
            AppLoop().get_loop().run_until_complete(
                CareersScraper(browser_profile_name).run()
            )
