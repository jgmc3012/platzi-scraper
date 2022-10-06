
import logging
import os
from .utils.preload_stage import resolve as resolve_preload_stage, get_preload_state
from lxml import html
from packages.core.utils.selectors import Selector

logger = logging.getLogger('log_print')


class BasicPage:

    def __init__(self, html: str, url: str):
        logger.debug(f"Init Scraper url - {url}")
        self._raw_html = html
        self._url = url

    def _save_html(self):
        with open(f'{os.getcwd()}/storage/{self._url.replace("/","")}.html', 'w+') as f:
            f.write(self._raw_html)

    @property
    def _selectors(self):
        return Selector().get(self.__class__)


class XPathPage(BasicPage):

    def __init__(self, *args, **kwargs):
        self._properties = dict()
        super().__init__(*args, **kwargs)

    @property
    def _parsed_html(self):
        if not hasattr(self, '__parsed_html'):
            self.__parsed_html = html.fromstring(self._raw_html)
        return self.__parsed_html

    def _get_value_from_xpath(self, xpath: str):
        return self._parsed_html.xpath(xpath)

    def _get_xpath(self, property_name: str):
        return self._selectors[property_name]['xpath']

    def _get_value_from_property(self, property_name: str):
        return self._get_value_from_xpath(
            self._get_xpath(property_name)
        )

    def _get_property(self, property_name: str):
        if not self._properties.get(property_name):
            result = self._get_value_from_property(property_name)
            if not result:
                logger.warning(
                    f"Property {property_name} don't match on {self._url}")
            self._properties[property_name] = result

        return self._properties[property_name]


class JsonPage(BasicPage):

    def __init__(self, *args, raw_json_data=None, **kwargs):
        self._raw_data = raw_json_data
        super().__init__(*args, **kwargs)

    @property
    def state(self):
        if not hasattr(self, '_state'):
            self._state = resolve_preload_stage(self._selectors, self.raw_data)
        return self._state

    @property
    def raw_data(self):
        if not self._raw_data:
            self._raw_data = get_preload_state(self._raw_html)
        return self._raw_data
