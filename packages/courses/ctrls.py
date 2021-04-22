import logging
import asyncio
from packages.core.scraper.ctrls  import CtrlPyppetterScraper
from packages.careers.models import Career

from .page_objects import CoursesPage
from .models import Course


logger = logging.getLogger('log_print')


class CoursesScraper(CtrlPyppetterScraper):

    async def run(self):
        await self.init_client()
        careers = await Career.all()
        coros = [self.scraper_courses(career) for career in careers]
        await asyncio.gather(*coros)
        await self.close_client()

    async def scraper_courses(self, career: Career):
        url = self.URL_BASE + career.path
        html = await self.visit_page(url)
        courses = CoursesPage(html, url)
        logger.info(f"Saving data from {url}")
        for row in zip(courses.names, courses.paths):
            logger.info(f"Get or create Course {row[0]}")
            course = Course.get_or_create(
                name=row[0],
                path=row[1],
            )
            logger.info(f"Linked course({row[0]}) to career({career}) ")
            await course.careers.add(career)
