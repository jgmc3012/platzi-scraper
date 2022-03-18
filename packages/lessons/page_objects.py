from logging import getLogger
from packages.core.scraper.page_objects import XPathPage
from packages.core.utils.datetime import str_to_seg

logger = getLogger('log_print')


class LessonsPage(XPathPage):

    @property
    def titles(self):
        return self._get_property('titles')

    @property
    def paths(self):
        return self._get_property('paths')

    @property
    def durations(self):
        return map(str_to_seg, self._get_property('durations'))
