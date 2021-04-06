from cleo import Command
from packages.core.utils.app_loop import AppLoop

from .ctrls import CtrlBaseScraper

class AllCommands:

    class ScraperPage(Command):
        """
        Navega hasta una pagina determida y obtiene el valor de body

        scraper:save_page
        {url : url}
        """

        def handle(self):
            url = self.argument('url')
            AppLoop().get_loop().run_until_complete(
                CtrlBaseScraper().save_page(url)
            )
