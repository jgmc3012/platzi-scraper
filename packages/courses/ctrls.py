import asyncio
from logging import getLogger

from packages.careers.models import Career
from packages.core.scraper.ctrls import CtrlPyppetterScraper

from .models import Course
from .page_objects import CoursesPage

logger = getLogger('log_print')


class CoursesScraper(CtrlPyppetterScraper):

    async def run(self):
        raise NotImplementedError

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
        for course in courses.resolve():
            # TODO: [FEATURE] Include teacher and release date
            logger.debug(f"Get or create Course {row[0]}")
            course = await Course.get_and_update(
                name=row[0],
                path=row[1],
            )
            logger.info(f"Linked course({row[0]}) to career({career}) ")
            await course.careers.add(career)
