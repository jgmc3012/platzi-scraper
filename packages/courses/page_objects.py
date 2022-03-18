from logging import getLogger
from packages.core.scraper.page_objects import XPathPage


logger = getLogger('log_print')


class CoursesPage(XPathPage):

    @property
    def names(self):
        return self._get_property('names')

    @property
    def paths(self):
        return self._get_property('paths')
