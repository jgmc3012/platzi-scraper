from cleo import Command
from packages.core.utils.app_loop import AppLoop

from .ctrls import CtrlBaseScraper, CategoriesScraper, CoursesScraper

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

    class ScraperCategories(Command):
        """
        Scraper platzi categories

        scraper:platzi_categories
        """

        def handle(self):
            AppLoop().get_loop().run_until_complete(
                CategoriesScraper().run()
            )


    class ScraperPathLearn(Command):
        """
        Scraper platzi courses

        scraper:platzi_courses
        """

        def handle(self):
            AppLoop().get_loop().run_until_complete(
                CoursesScraper().run()
            )
