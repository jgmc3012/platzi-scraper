from logging import getLogger
from packages.core.scraper.page_objects import BasicPage


logger = getLogger('log_print')


class CoursesPage(BasicPage):
    type_page = 'courses'

    @property
    def names(self):
        return self._get_property('names')

    @property
    def paths(self):
        return self._get_property('paths')

class ReviewsPage(BasicPage):
    type_page = 'reviews'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stars = []

    @property
    def user_profiles(self):
        return self._get_property('user_profiles')
    
    @property
    def bodies(self):
        return self._get_property('bodies')
    
    @property
    def stars(self):
        if not self._stars:
            full_xpath_base = self._get_xpath('full_stars')
            half_xpath_base = self._get_xpath('half_star')
            for i, user in enumerate(self.user_profiles):
                full_stars = self._get_value_from_xpath(
                    full_xpath_base.format(review_number=i+1)
                )
                if not full_stars:
                    logger.warning(f"Property full_stars don't match on {self._url}")
                stars = len(full_stars)
                if stars < 5:
                    half_star = self._get_value_from_xpath(
                        half_xpath_base.format(review_number=i+1)
                    )
                    stars += len(half_star)*0.5
                self._stars.append(stars)
        return self._stars

    @property
    def total_pages(self):
        total_pages = self._get_property('total_pages')
        logger.info(f"TOTAL PAGES {total_pages} on {self._url}")
        if len(total_pages) == 0:
            if len(self.user_profiles) < 30:
                logger.warning(f"WARNNIG - Verify that {self._url} don't has more of one page.")
            return 0
        return int(total_pages[0])
