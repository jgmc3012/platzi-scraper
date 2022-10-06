from logging import getLogger

from packages.core.scraper.page_objects import JsonPage
from packages.users.utils import get_username_from_avatar

from .utils import str_to_datetime

logger = getLogger('log_print')


class LessonsPage(JsonPage):

    def resolve(self):
        comments = self.state
        for comment in comments:
            comment['writed_at'] = str_to_datetime(comment['writed_at'])
            comment['author']['username'] = get_username_from_avatar(comment['author'].pop('avatar'))
        return {
            'comments': comments
        }
