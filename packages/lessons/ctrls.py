import asyncio
import logging

from packages.core.scraper.ctrls import CtrlPyppetterScraper
from packages.courses.models import Course
from packages.users.models import  User

from .models import Lesson, Comment
from .page_objects import LessonsPage, CommentsPage

logger = logging.getLogger('log_print')


class LessonsScraper(CtrlPyppetterScraper):

    async def run(self):
        await self.init_client()
        courses = await Course.actives()
        coros = map(self.scraper, courses)
        await asyncio.gather(*coros)
        await self.close_client()

    async def scraper(self, course: Course):
        url = self.URL_BASE + course.path
        html = await self.visit_page(url)
        lessons = LessonsPage(html, url)
        logger.info(f"Saving Lesson data from {url}")
        for index, row in enumerate(zip(lessons.titles, lessons.paths, lessons.durations)):
            await Lesson.get_or_create(
                title=row[0],
                path=row[1],
                duration_in_seg=row[2],
                track_number=(index+1),
                course=course
            )

class CommentsScraper(CtrlPyppetterScraper):

    async def run(self):
        await self.init_client()
        lessons = await Lesson.all()
        coros = map(self.scraper, lessons)
        await asyncio.gather(*coros)
        await self.close_client()

    async def scraper(self, lesson: Lesson):
        url = self.URL_BASE + lesson.path
        html = await self.visit_page(url)
        comments = CommentsPage(html, url)
        logger.info(f"Saving Comment data from {url}")
        for comment in comments.as_list():
            author, _ = await User.get_or_create(username=comment['author'])
            await Comment.get_or_create(
                lesson=lesson,
                content=comment['content'],
                author=author,
                likes=int(comment['likes']),
            )
