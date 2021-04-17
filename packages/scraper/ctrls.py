import asyncio
import logging
import os
from lxml import html
from packages.core.utils.config import Config
from packages.core.utils.web_client import WebClient
import csv

URL_BASE = "https://platzi.com"

WORK_DIR = os.path.dirname(os.path.realpath(__file__))

class BasicPage:
    path_selectors = f'{WORK_DIR}/selectors.yml'
    type_page = 'field to match with selector yaml config'
    _properties = {}

    def __init__(self, html:str):
        self._raw_html = html
        self._parsed_html = self._get_parsed_html(html)

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
            self._properties[property_name] = self._get_value_from_xpath(property_name)
        return self._properties[property_name]

    def _save_html(self):
        with open(f'{WORK_DIR}/storage/{self.type_page}.html', 'w+') as f:
            f.write(self._raw_html)

class Categories(BasicPage):
    type_page = 'category'

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

    def __init__(self, sem:int=1):
        self.sem = asyncio.Semaphore(sem)

    async def visit_page(self, url:str):
        """
        Await than semaphore is available.

        Visit the url and return the body html
        """
        async with self.sem:
            await asyncio.sleep(1)
            return await self.client.do_request(url, return_data='text')

    async def save_page(self, url, html=''):
        if not html:
            html = await self.visit_page(url)
        with open(f'storage/{url.replace("/", "")}.html', 'w+') as f:
            f.write(html)


class CategoriesScraper(CtrlBaseScraper):

    async def run(self):
        html = await self.visit_page(URL_BASE + '/cursos/')
        categories = Categories(html)
        with open(f'{WORK_DIR}/storage/categories.csv', 'w+') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(('name', 'path'))
            for row in zip(categories.names, categories.paths):
                writer.writerow(row)

class CoursesScraper(CtrlBaseScraper):

    async def run(self):
        with open(f'{WORK_DIR}/storage/categories.csv', 'r') as f:
            reader = csv.DictReader(f)
            coros = [self.scraper_learning_paths(row['name'], row['path']) for row in reader]

        learning_paths = await asyncio.gather(*coros)
        for learn_path, category_name in learning_paths:
            with open(f'{WORK_DIR}/storage/courses_{category_name}.csv', 'w+') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerow(('category_name' ,'name', 'path'))
                for row in zip(learn_path.names, learn_path.paths):
                    writer.writerow((category_name, *row))

    async def scraper_learning_paths(self, category_name, category_path):
        html = await self.visit_page(URL_BASE + category_path)
        return Courses(html), category_name
