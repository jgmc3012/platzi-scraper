import csv
from packages.core.scraper.ctrls  import CtrlBaseScraper
from .page_objects import CareersPage
import logging


logger = logging.getLogger('log_print')


class CareersScraper(CtrlBaseScraper):

    async def run(self):
        with open(f'{self.WORK_DIR}/storage/categories.csv', 'r') as f:
            reader = csv.DictReader(f)
            coros = [self.scraper_career(row['name'], row['path']) for row in reader]

        careers = await asyncio.gather(*coros)

    async def scraper_career(self, category_name, category_path):
        url = self.URL_BASE + category_path
        html = await self.visit_page(url)
        career = CareersPage(html, url)
        with open(f'{self.WORK_DIR}/storage/career_{category_name}.csv', 'w+') as f:
            writer = csv.writer(f, delimiter=',')
            logger.info(f"Saving data from {url}")
            writer.writerow(('category_name' ,'name', 'path'))
            for row in zip(career.names, career.paths):
                writer.writerow((category_name, *row))
