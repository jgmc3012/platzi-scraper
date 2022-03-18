import asyncio
import logging

from packages.core.scraper.ctrls import CtrlPyppetterScraper
from packages.users.models import User

from .models import Comment, Lesson
from .page_objects import CommentsPage

logger = logging.getLogger('log_print')


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
