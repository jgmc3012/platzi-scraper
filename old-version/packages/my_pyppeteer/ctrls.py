import asyncio
import json
import os
import re
import socket
from glob import glob
from logging import getLogger
from os import environ
from pathlib import Path
from sys import platform

import yaml
from packages.core.utils.singleton import SingletonClass
from pyppeteer import connect, errors, launch

logger = getLogger('log_print')


class MyPyppeteer(metaclass=SingletonClass):
    """
    Clase para simular la navegacion de un usuario en un navegador
    """
    profile = 'Person 1' # This is profile by default when you install chrome

    def __init__(self):
        self.browser = None
        self.oppener = False
        self.max_opened_tabs = 50
        self._yaml = {}
        self.yaml_name = 'storage/pyppetter_browsers.yaml'
        self._profile_dir = ''
        self.ws = None
        self.rotate_enabled = False
        self.TimeoutDefault = 0
        self.pool = {'availables': list()}
        self.flags = [
            '--window-size=1400,980',
            '--no-default-browser-check',
            '--process-per-tab',
            '--new-window',
            '--allow-running-insecure-content',
            '--silent-debugger-extension-api',

            '--disable-add-to-shelf',
            '--disable-background-downloads',
            # Disable crashdump collection (reporting is already disabled in Chromium)
            '--disable-breakpad',
            '--disable-component-update',
            '--disable-datasaver-prompt',
            '--disable-desktop-notifications',
            '--disable-domain-reliability',
            # Disables OOPIF. https://www.chromium.org/Home/chromium-security/site-isolation
            '--disable-features=site-per-process',
            '--disable-hang-monitor',
            '--disable-notifications',
            '--disable-sync',
            '--disable-translate-new-ux',  # No se si existe aun
            '--mute-audio',
            '--safebrowsing-disable-auto-update',
            '--disable-touch-adjustment',
            '--disable-speech-api',
            '--no-first-run',
            '--enable-automation',
            '--no-sandbox'
        ]

    @property
    def yaml(self):
        if not self._yaml:
            if not os.path.exists(self.yaml_name):
                open(self.yaml_name, 'w').close()
            with open(self.yaml_name, 'r') as yamlfile:
                self._yaml = yaml.load(yamlfile)
                self._yaml = self._yaml if self._yaml else {}
        return self._yaml

    async def init_pool_pages(self, number_pages: int) -> dict:
        if not self.browser:
            await self.connect_browser()
        for i in range(number_pages):
            self.pool[i] = await self.browser.newPage()
            self.pool[i].setDefaultNavigationTimeout(self.TimeoutDefault)
            self.pool['availables'].append(i)
        return self.pool

    async def close_pool(self, number_pages):
        """Close number_pages tab on browser"""
        for _ in range(number_pages):
            page_id, page = self.get_page_pool()
            await page.close()

    async def change_page(self, page):
        for page_index in self.pool:
            if (page_index != 'availables') and (self.pool.get(page_index) == page):
                await page.close()
                self.pool[page_index] = await self.browser.newPage()
                self.pool[page_index].setDefaultNavigationTimeout(
                    self.TimeoutDefault)
                return self.pool[page_index]

    def get_page_pool(self) -> tuple:
        """
        Return:
            - id_page: El id de la pagina que se retorna(esta valor debe ser paso en el close_page_pool)
            - page: Una pagina activa del browser
        """
        page_id = self.pool['availables'].pop()
        return page_id, self.pool[page_id]

    def close_page_pool(self, page_id):
        self.pool['availables'].insert(0, page_id)

    def get_ws_profile(self):
        ws = self.yaml.get(self.profile)
        if not ws:
            return

        return re.sub(r'\d+\.\d+\.\d+\.\d+', environ['BROWSER_IP'], ws, 1)

    def set_ws_profile(self, ws):
        # TODO: Multi-browser -> Save ws in redis with key as docker_id
        self.yaml[self.profile] = ws
        with open(self.yaml_name, 'w') as fp:
            yaml.dump(self.yaml, fp, default_flow_style=False)

    def check_ws_opened(self):
        if not self.ws:
            return False

        address = re.search(r'ws://(.+):(\d+)/', self.ws)
        ip = address.group(1)
        port = int(address.group(2))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        err = sock.connect_ex((ip, port))
        return err == 0

    async def connect_browser(self, ws=None, **kwargs):
        if self.browser:
            return await self.get_connection(daemon=False)

        self.ws = ws or self.get_ws_profile()
        if self.check_ws_opened():
            self.browser = await connect(browserWSEndpoint=self.ws)
            return await self.get_connection(daemon=False)

        self.browser = await self.launch_browser(**kwargs)
        return await self.get_connection(daemon=False)

    async def get_attribute(self, obj, attr, page=None):
        if not page:
            page = self.page
        if obj:
            return (await page.evaluate(f'(obj) => obj.getAttribute("{attr}")', obj))

    async def get_property(self, obj, attr, page=None):
        if not page:
            page = self.page
        if obj:
            return (await page.evaluate(f'(obj) => obj.{attr}', obj))

    async def set_property(self, obj, **kwargs):
        page = kwargs.pop('page', self.page)
        for attr, value in kwargs.items():
            await page.evaluate(f'(obj) => obj.{attr} = "{value}"', obj)

    async def get_property_from_querySelector(self, selector: str, attr: str, page=None):
        if not page:
            page = self.page
        return await page.evaluate('''() => {{
            obj = document.querySelector('{selector}')
            if (obj) {{
                return obj.{attr}
            }}
        }}'''.format(selector=selector, attr=attr))

    async def get_property_from_querySelectorAll(self, selector: str, attr: str, page=None):
        if not page:
            page = self.page
        return await page.evaluate('''() => {{
            obj = document.querySelectorAll('{selector}')
            return Array.from(obj).map(node => node.{attr})
        }}'''.format(selector=selector, attr=attr))

    async def count_pages(self):
        self.browser, self.page = await MyPyppeteer().connect_browser()
        pages = await self.browser.pages()
        logger.warn(f'Open pages: {len(pages)}')
        return len(pages)

    async def get_connection(self, daemon):
        if not self.ws:
            self.ws = self.browser.wsEndpoint
            self.set_ws_profile(self.ws)

        logger.warn(f'Profile: {self.profile} --> ws: {self.ws}')
        if daemon:
            input('Oprima (enter) para cerrar: ')
            await self.browser.close()
            return

        self.page = (await self.browser.pages())[0]
        return self.browser, self.page

    def get_profile_dir(self):
        if self._profile_dir:
            return self._profile_dir

        if platform in ['linux', 'linux2']:  # linux
            paths = (
                glob(f'{Path.home()}/.config/google-chrome/*/Preferences') +
                glob(f'{Path.home()}/.config/chromium/*/Preferences') +
                glob(f'{os.getcwd()}/storage/*/Preferences')
            )
        elif platform == "darwin":  # mac
            paths = glob(
                f'{Path.home()}/Library/Application Support/Google/Chrome/*/Preferences')
        elif platform == "win32":  # Windows
            paths = glob(
                f'{Path.home()}\\AppData\\Local\\Chromium\\User Data\\*\\Preferences')

        profile_names = []
        for path in paths:
            with open(path) as f:
                temp = json.load(f)
                profile_name = temp['profile']['name']
                profile_names.append(profile_name)
                if profile_name == self.profile:
                    self._profile_dir = str(Path(path).parent)
                    break

        if not self._profile_dir:
            logger.error(
                f'Please, create a new profile with "{self.profile}" as name.'
            )
            exit(1)
        return self._profile_dir

    async def launch_browser(self, **extra_parameters):
        parameters = {'headless': True, 'args': self.flags, **extra_parameters}
        if self.get_profile_dir():
            parameters['args'] += [
                f'--profile-directory={Path(self.get_profile_dir()).name}']
            parameters['userDataDir'] = str(
                Path(self.get_profile_dir()).parent)
        try:
            return await launch(**parameters)
        except errors.BrowserError as e:
            if not parameters['headless']:
                logger.error(
                    'Not is posible to launch the browser. Is you try to open browser in a environment without graphical interface?')
            raise e

    async def open_browser(self, daemon=True, **kwargs):
        # https://github.com/GoogleChrome/chrome-launcher/blob/master/docs/chrome-flags-for-tools.md

        _ = kwargs.pop('args', [])
        self.browser = await self.launch_browser(**kwargs)
        self.oppener = True
        return await self.get_connection(daemon)

    async def newPage(self, headless=True):
        for _ in range(10):
            count_tabs = len(await self.browser.pages())
            if count_tabs < self.max_opened_tabs:
                return await self.browser.newPage()
            print(
                f'pyppetter {count_tabs} de {self.max_opened_tabs} tabs abiertos,Esperando 5 segundos')
            await asyncio.sleep(5)
        raise Exception(
            'despues de 50 segundos, No hay espacio para abrir un nuevo tab')

    async def click_and_wait(self, obj, **kwargs):
        ''' los kwargs son pra waitForNavigation'''

        page = kwargs.get('page')
        if not page:
            page = self.page
        try:
            return await asyncio.gather(page.waitForNavigation(**kwargs), self.click(obj, page=page))
        except errors.TimeoutError:
            print('ERROR, click_and_wait Timeout Exceeded')

    async def click(self, obj, **kwargs):
        page = kwargs.get('page')
        if not page:
            page = self.page
        return await page.evaluate('(obj) => obj.click()', obj)

    async def skip_error(self, function):
        try:
            return await function
        except errors.TimeoutError:
            print('skip_error, Timeout Exceeded')

    async def start_rotate_pages(self):
        self.rotate_enabled = True
        browser, _ = await self.connect_browser()
        for _ in range(1000):
            pages = await browser.pages()
            if not self.rotate_enabled:
                return
            for page in pages:
                if not page.isClosed():
                    try:
                        await page.bringToFront()
                        await asyncio.sleep(1)
                    except errors.NetworkError:
                        pass

    async def stop_rotate_pages(self):
        self.rotate_enabled = False
