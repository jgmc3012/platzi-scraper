import csv
from packages.core.scraper.ctrls  import CtrlBaseScraper
from .page_objects import CoursesPage
import logging


logger = logging.getLogger('log_print')


class CoursesScraper(CtrlBaseScraper):

    async def run(self):
        with open(f'{self.WORK_DIR}/storage/categories.csv', 'r') as f:
            reader = csv.DictReader(f)
            categories = list(reader)
        
        coros = []
        for category in categories:
            with open(f'{self.WORK_DIR}/storage/career_{category["name"]}.csv', 'r') as f:
                reader = csv.DictReader(f)
                coros += [self.scraper_courses(row['category_name'], row['name'], row['path']) for row in reader]

        await asyncio.gather(*coros)

    async def scraper_courses(self, category_name, career_name, career_path):
        url = self.URL_BASE + career_path
        html = await self.visit_page(url)
        course = CoursesPage(html, url)
        with open(f'{self.WORK_DIR}/storage/courses_{career_name}.csv', 'w+') as f:
            writer = csv.writer(f, delimiter=',')
            logger.info(f"Saving data from {url}")
            writer.writerow(('category_name' , 'career_name', 'course_name', 'course_path'))
            for row in zip(course.names, course.paths):
                writer.writerow((category_name, career_name, *row))
