from functools import reduce
from logging import getLogger

from packages.core.scraper.page_objects import JsonPage

from .utils.datetime import str_to_datetime
from .utils.teacher import url_to_username

logger = getLogger('log_print')


class CoursesPage(JsonPage):

    def resolve(self):
        if not hasattr(self, '_resolved'):
            self._resolved = self._course_properties
        return self._resolved

    def _course_properties(self):
        """Update format of course(state) to match database

        Args:
            course (dict): course to transform
        """
        course = self.state
        course['release'] = str_to_datetime(course['release'])
        course['teacher']['username'] = url_to_username(
            course['teacher'].pop('path'))

        lessons = reduce((lambda memo, cap: memo + cap['lessons']), course.pop('captions'), [])
        course['lessons'] = filter(lambda lesson: bool(lesson.get('id')), lessons)
        for index, lesson in enumerate(course['lessons']):
            lesson['track_number'] = index + 1
