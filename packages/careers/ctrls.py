import logging
from packages.core.scraper.ctrls  import CtrlBaseScraper
from packages.categories.models import Category

from .page_objects import CareersPage
from .models import Career


logger = logging.getLogger('log_print')


class CareersScraper(CtrlBaseScraper):

    async def run(self):
        await categories = Category.all()
        coros = [self.scraper_career(category) for category in categories]

        await asyncio.gather(*coros)

    async def scraper_career(self, category: Category):
        url = self.URL_BASE + category.path
        html = await self.visit_page(url)
        career = CareersPage(html, url)
        logger.info(f"Saving data from {url}")
        for row in zip(career.names, career.paths):
            logger.info(f"Get or create Career {row[0]}")
            Career.get_create(
                name=row[0],
                path=row[1],
                category=category,
            )
