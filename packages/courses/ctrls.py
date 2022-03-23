import asyncio
from logging import getLogger

from packages.core.scraper.ctrls import CtrlPyppetterScraper
from packages.users.models import User
from packages.lessons.models import Lesson

from .models import Course
from .page_objects import CoursesPage

logger = getLogger('log_print')


class CoursesScraper(CtrlPyppetterScraper):

    async def run(self):
        await self.init_client()
        courses = await Course.all()
        await asyncio.gather(*map(self.update_courses, courses))
        await self.close_client()

    async def update_courses(self, course: Course):
        url = self.URL_BASE + course.path
        html = await self.visit_page(url)
        courses = CoursesPage(html, url)
        logger.info(f"Saving data from {url}")
        for properties in courses.resolve():
            lessons_props = properties.pop('lessons')

            properties['teacher'], _ = await User.get_or_create(**properties['teacher'])
            course, _ = await Course.update_or_create(**properties)

            lessons_props = map(lambda x: x.update({'course': course}), lessons_props)
            await asyncio.gather(*(
                Lesson.update_or_create(**properties) for properties in lessons_props
            ))
