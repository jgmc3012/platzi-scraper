import asyncio
import logging
import os
from lxml import html
from packages.core.utils.config import Config
from packages.core.utils.web_client import WebClient
import csv

logger = logging.getLogger('log_print')

WORK_DIR = os.path.dirname(os.path.realpath(__file__))

class BasicPage:
    path_selectors = f'{WORK_DIR}/selectors.yml'
    type_page = 'field to match with selector yaml config'

    def __init__(self, html:str, url:str):
        logger.info(f"Init Scraper url - {url}")
        self._raw_html = html
        self._parsed_html = self._get_parsed_html(html)
        self._url = url
        self._properties = dict()

    @property
    def _selectors(self):
        return Config().config_yaml(self.path_selectors)

    def _get_parsed_html(self, body_html):
        return html.fromstring(body_html)

    def _get_value_from_xpath(self, property_name:list):
        return self._parsed_html.xpath(
            self._selectors[self.type_page][property_name]['xpath']
        )

    def _get_property(self, property_name:str):
        if not self._properties.get(property_name):
            result = self._get_value_from_xpath(property_name)
            if not result:
                logger.warning(f"Property {property_name} don't match on {self._url}")
            self._properties[property_name] = result
        return self._properties[property_name]

    def _save_html(self):
        with open(f'{WORK_DIR}/storage/{self._url.replace("/","")}.html', 'w+') as f:
            f.write(self._raw_html)

class Categories(BasicPage):
    type_page = 'category'

    @property
    def names(self):
        return self._get_property('names')

    @property
    def paths(self):
        return self._get_property('paths')

class LearningPath(BasicPage):
    type_page = 'learning_path'

    @property
    def names(self):
        return self._get_property('names')

    @property
    def paths(self):
        return self._get_property('paths')


class Courses(BasicPage):
    type_page = 'courses'

    @property
    def names(self):
        return self._get_property('names')

    @property
    def paths(self):
        return self._get_property('paths')


class CtrlBaseScraper:
    client = WebClient()
    USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"
    URL_BASE = "https://platzi.com"

    def __init__(self, sem:int=3):
        self.sem = asyncio.Semaphore(sem)
        self.token_cdn = "b6f700d21c835cdb85e1dd4ffba169e5835acd67-1618699169-1800-AV/JsX5SBfrWcHQHR1cnZYnqLuvet+VnsTrG7s7LdjTbpNf6ME15yj0l2R2Dqt33rfm3YY5ytPj8v1H3NpDwcpN0ZHaNdRDMTL+XCDiGDiqttPMKwGm91iiMe5XAS6JMN9zyQ1o2nASWcAsZn/aL56VGaNpXVpeOwPAVfkLv6IIaNdPMNi8hN8fOJ6XwMcA23A=="
    async def visit_page(self, url:str):
        """
        Await than semaphore is available.

        Visit the url and return the body html
        """
        async with self.sem:
            logger.info(f'Visit to page {url}')
            while True:
                html = await self.client.do_request(
                    url, return_data='text', 
                    headers={
                        'User-Agent': self.USER_AGENT,
                        'Cookie': f"__cf_bm={self.token_cdn}"
                    })
                if 'Maintance-logo' not in html:
                    break
                logger.warning('Reloading cookies')
                await self._refresh_token()
            return html

    async def _refresh_token(self):
        url = f'https://platzi.com/cdn-cgi/bm/cv/result'
        headers = {
            'User-Agent': self.USER_AGENT,
            'Cookie': f"__cf_bm={self.token_cdn}",
            'Content-Type': 'application/json',
        }
        data = '{"m":"3616224aa9db014acad9f174334f5eefbd15d1f4-1618695270-1800-AUcBr7XvzRjbXx3z7I0B2dyBo8nKY76XWS7iCgnX9/xDiW0kirnVpaYz606HSqvcgbx4Q/nbNnpyAcFNXH7SkbEq8k+TOTteO+t0GJBbKEhs3fVlTQUe9p1i6/TEtMQNLw==","results":["7630098eab88512b9beab589cf8f5753","9391affe53ccfa2b0f0cc30b64ea65b3"],"timing":47,"fp":{"id":3,"e":{"r":[1680,1050],"ar":[1023,1680],"pr":1,"cd":24,"wb":false,"wp":false,"wn":false,"ch":false,"ws":false,"wd":false}}}'
        async with (await self.client.get_session()).post(
                    url,
                    headers=headers,
                    verify_ssl=False,
                    data=data
                ) as resp:
            if not resp.ok:
                logger.warning(f'Error getting token. Status {resp.status}')
                return

            new_token = getattr(resp.cookies.get('__cf_bm'), 'value', None)
            if not new_token:
                logger.warning(f"New token does not exist on response. Cookies {resp.cookies}")
            self.token_cdn = new_token


    async def save_page(self, url, html=''):
        if not html:
            html = await self.visit_page(url)
        with open(f'storage/{url.replace("/", "")}.html', 'w+') as f:
            f.write(html)


class CategoriesScraper(CtrlBaseScraper):

    async def run(self):
        url = self.URL_BASE + '/cursos/'
        html = await self.visit_page(url)
        categories = Categories(html, url)
        with open(f'{WORK_DIR}/storage/categories.csv', 'w+') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(('name', 'path'))
            for row in zip(categories.names, categories.paths):
                writer.writerow(row)

class LearningPathScraper(CtrlBaseScraper):

    async def run(self):
        with open(f'{WORK_DIR}/storage/categories.csv', 'r') as f:
            reader = csv.DictReader(f)
            coros = [self.scraper_learning_path(row['name'], row['path']) for row in reader]

        learning_paths = await asyncio.gather(*coros)

    async def scraper_learning_path(self, category_name, category_path):
        url = self.URL_BASE + category_path
        html = await self.visit_page(url)
        learning_path = LearningPath(html, url)
        with open(f'{WORK_DIR}/storage/learning_path_{category_name}.csv', 'w+') as f:
            writer = csv.writer(f, delimiter=',')
            logger.info(f"Saving data from {url}")
            writer.writerow(('category_name' ,'name', 'path'))
            for row in zip(learning_path.names, learning_path.paths):
                writer.writerow((category_name, *row))

class CoursesScraper(CtrlBaseScraper):

    async def run(self):
        with open(f'{WORK_DIR}/storage/categories.csv', 'r') as f:
            reader = csv.DictReader(f)
            categories = list(reader)
        
        coros = []
        for category in categories:
            with open(f'{WORK_DIR}/storage/learning_path_{category["name"]}.csv', 'r') as f:
                reader = csv.DictReader(f)
                coros += [self.scraper_courses(row['category_name'], row['name'], row['path']) for row in reader]

        learning_paths = await asyncio.gather(*coros)

    async def scraper_courses(self, category_name, career_name, career_path):
        url = self.URL_BASE + career_path
        html = await self.visit_page(url)
        course = Courses(html, url)
        with open(f'{WORK_DIR}/storage/courses_{career_name}.csv', 'w+') as f:
            writer = csv.writer(f, delimiter=',')
            logger.info(f"Saving data from {url}")
            writer.writerow(('category_name' , 'career_name', 'course_name', 'course_path'))
            for row in zip(course.names, course.paths):
                writer.writerow((category_name, career_name, *row))
