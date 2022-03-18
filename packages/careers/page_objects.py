from packages.core.scraper.page_objects import XPathPage


class CareersPage(XPathPage):

    @property
    def names(self):
        return self._get_property('names')

    @property
    def paths(self):
        return self._get_property('paths')
