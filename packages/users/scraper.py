import asyncio
import logging

from packages.comments.models import Comment
from packages.core.scraper.web_clients import PyppetterWebClient
from packages.users.models import User

from .models import User
from .page_objects import UsersPage

logger = logging.getLogger('log_print')


class UserScraper(PyppetterWebClient):

    async def run(self):
        await self.init_client()
        users = await User.public_profiles()
        await asyncio.gather(*map(self.scraper, users))
        await self.close_client()

    async def scraper(self, user: User):
        url = self.URL_BASE + user.path
        html, json_data = await self.visit_page(url, '_ => window.data')
        properties = UsersPage(html, url, raw_json_data=json_data).resolve()
        logger.info(f"Saving Lesson data from {url}")
        user.link_courses(properties.pop('courses'))
        user.link_social_medias(properties.pop('social_medias'))
        user.link_careers(properties.pop('careers'))
        user.update(**properties)
