
import os
import logging
from lxml import html
from packages.core.utils.config import Config


logger = logging.getLogger('log_print')


class BasicPage:
    WORK_DIR = os.getcwd()
    path_selectors = f'{os.path.dirname(os.path.realpath(__file__))}/selectors.yml'
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
        with open(f'{self.WORK_DIR}/storage/{self._url.replace("/","")}.html', 'w+') as f:
            f.write(self._raw_html)
