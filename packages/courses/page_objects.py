from functools import reduce
from logging import getLogger
import re

from packages.core.scraper.page_objects import JsonPage

from .utils.datetime import str_to_datetime
from .utils.teacher import url_to_username

logger = getLogger('log_print')


class CoursesPage(JsonPage):

    def resolve(self):
        """Update format of course(state) to match database

        Args:
            course (dict): course to transform
        """
        if not hasattr(self, '_course'):
            course = self.state
            course['release'] = str_to_datetime(course['release'])
            course['teacher']['username'] = url_to_username(course['teacher'].pop('path'))
            course['teacher']['role'] = 'teacher'

            lessons = reduce((lambda memo, cap: memo + cap['lessons']), course.pop('captions'), [])
            course['lessons'] = filter(lambda lesson: bool(lesson.get('id')), lessons)
            for index, lesson in enumerate(course['lessons']):
                lesson['track_number'] = index + 1
            self._course = course
        return self._course
