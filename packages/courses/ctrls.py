import logging
import asyncio
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

    async def run(self):
        await self.init_client()
        courses = await Course.all()
        coros = [self.scraper_reviews(course) for course in courses]
        await asyncio.gather(*coros)
        await self.close_client()

    async def scraper_reviews(self, course: Course):
        page = 1
        review_page = await self.scraper_page_reviews(page, course)
        limit_page = review_page.total_pages
        coros = [self.scraper_page_reviews(n, course) for n in range(page+1, limit_page+1)]
        await asyncio.gather(*coros)

    async def scraper_page_reviews(self, page: int, course: Course):
        url = f'{self.URL_BASE}{course.path}opiniones/{page}/'
        html = await self.visit_page(url)
        reviews = ReviewsPage(html, url)
        logger.info(f"Saving data from {url}")
        for row in zip(reviews.user_profiles, reviews.bodies, reviews.stars):
            username = self.get_username_from_profile_path(row[0])
            logger.debug(f"Get or create Review by {username}")
            user, created = await User.get_or_create(
                username=username
            )
            review, created = await Review.get_or_create(
                course=course,
                user=user,
                comment=row[1],
                stars=row[2]
            )
            if created:
                logger.info(f"Linked user({user}) to course({course}) ")

        return reviews

    def get_username_from_profile_path(self, path_profile:str):
        """
        Transform "/p/bmazariegos/" to "bmazariegos"
        """
        return path_profile[3:-1]
