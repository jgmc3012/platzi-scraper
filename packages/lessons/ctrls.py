import asyncio
import logging

from packages.comments.models import Comment
from packages.core.scraper.ctrls import CtrlPyppetterScraper
from packages.users.models import User

from .models import Lesson
from .page_objects import LessonsPage

logger = logging.getLogger('log_print')


class LessonsScraper(CtrlPyppetterScraper):

    async def run(self):
        await self.init_client()
        lessons = await Lesson.all()
        await asyncio.gather(*map(self.scraper, lessons))
        await self.close_client()

    async def scraper(self, lesson: Lesson):
        url = self.URL_BASE + lesson.path
        html, json_data = await self.visit_page(url, '_ => window.__PRELOADED_STATE__')
        lessons = LessonsPage(html, url, raw_json_data=json_data)
        logger.info(f"Saving Lesson data from {url}")
        for comment_attr in lessons.resolve().comments:
            comment_attr['author'] = User.update_or_create(**comment_attr['author'])
            comment_attr['lesson'] = lesson
            await Comment.update_or_create(**comment_attr)
