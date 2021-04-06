import asyncio
import logging
import os

from packages.core.utils.web_client import WebClient

from .utils import get_yaml

class CtrlBaseScraper:
    path_selectors = f'{os.path.dirname(os.path.realpath(__file__))}/storage/selectors.yaml'

    client = WebClient()
    _selectors = None

    def __init__(self, sem:int=2):
        self.sem = asyncio.Semaphore(sem)

    @property
    def selectors(self):
        if not self._selectors:
            self._selectors = get_yaml(self.path_selectors)
        return self._selectors

    async def run_on_page(self, url:str, callback, *args, **kwargs):
        """
        Espera que alla una pestaña disponible en el navegador.

        Navega a la url indicada y ejecuta el callback una vez la
        pagina cargue correctamente.

        Todas los callback deben tener como primer parametro
        el objecto page de pyppeteer.
        """
        async with self.sem:
            body_html = await self.client.do_request(url, return_data='text')
            response = await callback(body_html, *args, **kwargs)
        return response

    async def get_data(self, body_html, *args, **kwargs)->tuple:
        selectors = self.selectors
        elements = dict()
        # for item in selectors:
        #     if selectors[item]['multiple']:
        #         elements[item] = await self.my_pyppeteer.get_property_from_querySelectorAll(
        #             selector=selectors[item]['css'],
        #             attr=selectors[item]['pyppeteer'],
        #             page=page
        #         )
        #     else:
        #         element = await self.my_pyppeteer.get_property_from_querySelector(
        #             selector=selectors[item]['css'],
        #             attr=selectors[item]['pyppeteer'],
        #             page=page
        #         )
        #         elements[item] = element if element else ''

        return elements, body_html

    async def save_page(self, url):
        elements, bodyHTML = await self.run_on_page(url, self.get_data)
        with open('storage/example.html', 'w') as f:
            f.write(bodyHTML)
