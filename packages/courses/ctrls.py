import logging
import asyncio
from more_itertools import chunked
from tortoise.exceptions import DoesNotExist, IntegrityError
from packages.core.scraper.ctrls  import CtrlPyppetterScraper
from packages.careers.models import Career
from packages.users.models import  User
from .page_objects import CoursesPage, ReviewsPage
from .models import Course, Review


logger = logging.getLogger('log_print')


class CoursesScraper(CtrlPyppetterScraper):

    async def run(self):
        await self.init_client()
        careers = await Career.all()
        coros = [self.scraper_courses(career) for career in careers]
        await asyncio.gather(*coros)
        await self.close_client()

    async def scraper_courses(self, career: Career):
        url = self.URL_BASE + career.path
        html = await self.visit_page(url)
        courses = CoursesPage(html, url)
        logger.info(f"Saving data from {url}")
        for row in zip(courses.names, courses.paths):
            logger.debug(f"Get or create Course {row[0]}")
            course, created = await Course.get_or_create(
                name=row[0],
                path=row[1],
            )
            logger.info(f"Linked course({row[0]}) to career({career}) ")
            await course.careers.add(career)

class ReviewsScraper(CtrlPyppetterScraper):
    reviews_per_page = 30
    async def run(self):
        await self.init_client()
        all_courses = await Course.all()
        for courses in chunked(all_courses, 3):
            coros = [self.scraper_reviews(course) for course in courses]
            await asyncio.gather(*coros)
        await self.close_client()

    async def scraper_reviews(self, course: Course):
        page = 1
        review_page = await self.scraper_page_reviews(page, course)
        limit_page = review_page.total_pages
        total_reviews = review_page.total_reviews
        real_reviews = review_page.total_pages * self.reviews_per_page
        logger.info(f"COURSE {course}: Current reviews {review_page.total_pages}. Real Reviews {real_reviews}")
        current_reviews = await course.reviews.all().count()
        reviews = await Review.filter(course=course)
        if total_reviews > current_reviews:
            logger.info(f"Scraping reviews from {course}.")
            logger.info(f"COURSE {course}: Current reviews {review_page.total_pages}. Total Reviews {total_reviews}")
            coros = [self.scraper_page_reviews(n, course, total_reviews) for n in range(page+1, limit_page+1)]
            await asyncio.gather(*coros)
        else:
            logger.info(f"SKIPING COURSE: {course}")

    async def scraper_page_reviews(self, page: int, course: Course, total_reviews:int=0):
        if total_reviews:
            current_reviews = await course.reviews.all().count()
            if total_reviews <= current_reviews:
                logger.info(f"SKIP this page. {url}")
                return ReviewsPage("", url)
        url = f'{self.URL_BASE}{course.path}opiniones/{page}/'
        html = await self.visit_page(url)
        reviews = ReviewsPage(html, url)
        logger.info(f"Scraping data from {url}")
        if len(reviews.user_profiles) != 30:
            logger.warning(f"Review this page: {url}")
        for row in zip(reviews.user_profiles, reviews.bodies, reviews.stars):
            username = self.get_username_from_profile_path(row[0])
            logger.debug(f"Get or create Review by {username}")

            # Create User
            try:
                user = await User.get(
                    username=username
                )
            except DoesNotExist:
                try:
                    user = await User.create(
                        username=username
                    )
                    logger.info(f"User({user}) created")
                    logger.debug(f"User Exist - ({username})")
                except IntegrityError as err:
                    logger.error(f"{err} - Cant Create User ({username})")

            # Create Review
            try:
                await Review.get(
                    course=course,
                    user=user,
                )
                logger.info(f"Review Exist - User ({user}) to course({course}) ")
            except DoesNotExist:
                try:
                    await Review.create(
                        course=course,
                        user=user,
                        comment=row[1],
                        stars=row[2]
                    )
                    logger.debug(f"Linked user({user}) to course({course}) ")
                except IntegrityError as err:
                    logger.error(f"{err} - Cant Link User({user}) with the Course({course}) ")

        return reviews

    def get_username_from_profile_path(self, path_profile:str):
        """
        Transform "/p/bmazariegos/" to "bmazariegos"
        """
        return path_profile[3:-1]
