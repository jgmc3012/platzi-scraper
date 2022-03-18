from cleo import Command
from packages.core.utils.app_loop import AppLoop

from .ctrls import CommentsScraper


class AllCommands:

    class Scraper(Command):
        """
        Scraper platzi comments lesson

        comments:scraper
        """

        def handle(self):
            AppLoop().get_loop().run_until_complete(
                CommentsScraper().run()
            )
