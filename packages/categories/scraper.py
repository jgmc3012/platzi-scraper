import logging

from packages.core.scraper.web_clients import PyppetterWebClient

from .models import Category
from .page_objects import CategoriesPage

logger = logging.getLogger('log_print')


class CategoriesScraper(PyppetterWebClient):

    async def run(self):
        await self.init_client()
        url = self.URL_BASE + '/cursos/'
        html = await self.visit_page(url)
        categories_page = CategoriesPage(html, url)
        for row in zip(categories_page.names, categories_page.paths):
            logger.debug(f"Get or create Category {row[0]} on DB")
            await Category.get_or_create(
                name=row[0],
                path=row[1],
            )
        await self.close_client()
