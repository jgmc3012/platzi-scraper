from logging import getLogger

from aenum import enum

from packages.core.scraper.page_objects import JsonPage
from .utils.datetime import str_to_datetime
from .utils.teacher import url_to_username
from functools import reduce

logger = getLogger('log_print')


class CoursesPage(JsonPage):

    def resolve(self):
        if not hasattr(self, '_resolved'):
            self._resolved = map(self._transform, self.state)
        return self._resolved        

    def _transform(self, course: dict):
        """Update format of course to match database

        Args:
            course (dict): course to transform
        """
        course['release'] = str_to_datetime(course['release'])
        course['teacher']['username'] = url_to_username(course['teacher'].pop('path'))

        course['lessons'] = reduce((lambda memo, cap: memo + cap['lessons']), course.pop('captions'), [])

        for index, lesson in enumerate(course['lessons']):
            lesson['track_number'] = index + 1