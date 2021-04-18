from packages.core.scraper.page_objects import BasicPage


class CoursesPage(BasicPage):
    type_page = 'courses'

    @property
    def names(self):
        return self._get_property('names')

    @property
    def paths(self):
        return self._get_property('paths')
