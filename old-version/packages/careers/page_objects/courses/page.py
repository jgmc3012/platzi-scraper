from logging import getLogger
from packages.core.scraper.page_objects import JsonPage
from functools import reduce

logger = getLogger('log_print')


class CareersCoursesPage(JsonPage):
    
    def resolve(self):
        levels = self.state
        return reduce((lambda memo, level: memo + level['courses']), levels, [])
