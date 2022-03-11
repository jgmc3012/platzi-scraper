import logging
import asyncio
from packages.core.scraper.ctrls  import CtrlPyppetterScraper
from packages.courses.models import Course
from .page_objects import LessonsPage
from .models import Course


logger = logging.getLogger('log_print')


class LessonsScraper(CtrlPyppetterScraper):

    async def run(self):
        await self.init_client()
        courses = await Course.all()
        coros = map(self.scraper, courses)
        await asyncio.gather(*coros)
        await self.close_client()

    async def scraper(self, course: Course):
        url = self.URL_BASE + course.path
        html = await self.visit_page(url)
        lessons = LessonsPage(html, url)
        logger.info(f"Saving data from {url}")
        for index, row in enumerate(zip(lessons.titles, lessons.paths, lessons.durations)):
            logger.debug(f"Get or create Lesson {row[0]}")
            course, _ = await Course.get_or_create(
                title=row[0],
                path=row[1],
                duration_in_seg=row[2],
                track_number=(index+1),
                course=course
            )

class CommentsScraper(CtrlPyppetterScraper):
    pass