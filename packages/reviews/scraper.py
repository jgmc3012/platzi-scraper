import asyncio
from logging import getLogger

from more_itertools import chunked
from packages.core.scraper.web_clients import PyppetterWebClient
from packages.users.models import User
from packages.users.utils import get_username_from_profile_path
from packages.courses.models import Course

from .models import Review
from .page_objects import ReviewsPage

logger = getLogger('log_print')


class ReviewsScraper(PyppetterWebClient):
    REVIEWS_PER_PAGE = 30

    async def run(self):
        await self.init_client()
        all_courses = await Course.all()
        for courses in chunked(all_courses, 3):
            coros = map(self.scraper_reviews, courses)
            await asyncio.gather(*coros)
        await self.close_client()

    async def scraper_reviews(self, course: Course):
        page = 1
        review_page = await self.scraper_page_reviews(page, course)
        limit_page = review_page.total_pages
        total_reviews = review_page.total_reviews
        real_reviews = review_page.total_pages * self.REVIEWS_PER_PAGE
        logger.debug(f"{course}: Current reviews {review_page.total_pages}. Real Reviews {real_reviews}")
        current_reviews = await course.reviews.all().count()

        if current_reviews < total_reviews:
            logger.debug(f"SKIPING COURSE: {course}")
            return

        logger.info(f"Scraping reviews from {course} - > Current reviews {review_page.total_pages}. Total Reviews {total_reviews}")
        coros = [self.scraper_page_reviews(n, course, total_reviews) for n in range(page+1, limit_page+1)]
        await asyncio.gather(*coros)

    async def scraper_page_reviews(self, page: int, course: Course, total_reviews:int=0):
        if total_reviews:
            current_reviews = await course.reviews.all().count()
            if total_reviews <= current_reviews:
                logger.debug(f"SKIP this page. {url}")
                return ReviewsPage("", url)

        url = f'{self.URL_BASE}{course.path}opiniones/{page}/'
        html = await self.visit_page(url)
        reviews = ReviewsPage(html, url)

        if len(reviews.user_profiles) != self.REVIEWS_PER_PAGE:
            logger.warning(f"Review this page: {url}")

        for row in zip(reviews.user_profiles, reviews.bodies, reviews.stars):
            username = get_username_from_profile_path(row[0])

            user, _ = await User.get_or_create(username=username)
            await Review.get_or_create(
                course=course,
                user=user,
                comment=row[1],
                stars=row[2]
            )
