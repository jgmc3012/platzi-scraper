import logging
from packages.core.scraper.ctrls  import CtrlPyppetterScraper
from .page_objects import CategoriesPage
from .models import Category


logger = logging.getLogger('log_print')


class CategoriesScraper(CtrlPyppetterScraper):

    async def run(self):
        url = self.URL_BASE + '/cursos/'
        html = await self.visit_page(url)
        categories_page = CategoriesPage(html, url)
        for row in zip(categories_page.names, categories_page.paths):
            logger.info(f"Get or create Category {row[0]} on DB")            
            await Category.get_or_create(
                name=row[0],
                path=row[1],
            )
