import asyncio
import logging

from packages.categories.models import Category
from packages.core.scraper.ctrls import CtrlPyppetterScraper
from packages.courses.models import Course

from .models import Career
from .page_objects.careers.page import CareersPage
from .page_objects.courses.page import CareersCoursesPage

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

class CoursesScraper(CtrlPyppetterScraper):

    async def run(self):
        await self.init_client()
        careers = await Career.all()
        coros = [self.scraper_courses(career) for career in careers]
        await asyncio.gather(*coros)
        await self.close_client()

    async def scraper_courses(self, career: Career):
        url = self.URL_BASE + career.path
        html, raw_json_data = await self.visit_page(url, js_callback='_ => window.initialProps')

        courses = CareersCoursesPage(html, url, raw_json_data=raw_json_data)
        logger.info(f"Saving data from {url}")
        for course in courses.resolve():
            logger.debug(f"Get or create Course {course['title']}")
            course, _ = await Course.get_or_create(**course)
            logger.info(f"Linked course({course['title']}) to career({career}) ")
            await course.careers.add(career)
