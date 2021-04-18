import logging

from packages.core.scraper.ctrls  import CtrlBaseScraper
from packages.careers.models import Career

from .page_objects import CoursesPage
from .models import Course


logger = logging.getLogger('log_print')


class CoursesScraper(CtrlBaseScraper):

    async def run(self):
        coros = [self.scraper_courses(career) for career in careers]
        await asyncio.gather(*coros)

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
            logger.info(f"Linked course({row[0]}) to career({carrer}) ")
            await course.careers.add(career)
