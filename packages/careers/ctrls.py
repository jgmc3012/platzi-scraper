import asyncio
import logging

from packages.categories.models import Category
from packages.core.scraper.ctrls import CtrlPyppetterScraper

from .models import Career
from .page_objects import CareersPage

logger = logging.getLogger('log_print')


class CareersScraper(CtrlPyppetterScraper):

    async def run(self):
        categories = await Category.all()
        await self.init_client()
        coros = [self.scraper_career(category) for category in categories]
        await asyncio.gather(*coros)
        await self.close_client()

    async def scraper_career(self, category: Category):
        url = self.URL_BASE + category.path
        html = await self.visit_page(url)
        career = CareersPage(html, url)
        logger.info(f"Saving data from {url}")
        for row in zip(career.names, career.paths):
            logger.debug(f"Get or create Career {row[0]}")
            await Career.get_or_create(
                name=row[0],
                path=row[1],
                category=category,
            )
