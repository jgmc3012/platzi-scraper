import csv
from packages.core.scraper.ctrls  import CtrlBaseScraper
from .page_objects import CategoriesPage
import logging


logger = logging.getLogger('log_print')


class CategoriesScraper(CtrlBaseScraper):

    async def run(self):
        url = self.URL_BASE + '/cursos/'
        html = await self.visit_page(url)
        categories = CategoriesPage(html, url)
        with open(f'{self.WORK_DIR}/storage/categories.csv', 'w+') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(('name', 'path'))
            for row in zip(categories.names, categories.paths):
                writer.writerow(row)
