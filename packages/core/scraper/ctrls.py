import asyncio
import logging
import os

from packages.core.utils.web_client import WebClient
from packages.my_pyppeteer.ctrls import MyPyppeteer

logger = logging.getLogger('log_print')


class CtrlBaseScraper:
    WORK_DIR = os.getcwd()

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
            logger.debug(f'Visit to page {url}')
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


class CtrlPyppetterScraper:
    WORK_DIR = os.getcwd()

    
    USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"
    URL_BASE = "https://platzi.com"

    def __init__(self, sem:int=3):
        self.sem = asyncio.Semaphore(sem)
        self.lock = asyncio.locks.Lock()
        self.client = MyPyppeteer()
        self.number_pages = sem
        self.running_client = False

    async def init_client(self):
        """Init pool tabs"""
        async with self.lock:
            if not self.running_client:
                self.running_client = True
                await self.client.init_pool_pages(self.number_pages)

    async def visit_page(self, url:str):
        """
        Await than semaphore is available.

        Visit the url and return the body html
        """
        while True:
            async with self.sem:
                logger.debug(f'Visit to page {url}')
                page_id, page = self.client.get_page_pool()
                cookies = await page.cookies()
                await page.deleteCookie(*cookies)
                await page.goto(url, options={'waitUntil':'domcontentloaded'})
                html = await page.content()
                await asyncio.sleep(0.5)

                if  ('<title>Please Wait...' in html) or ('Maintance-logo' in html):
                    self.client.close_page_pool(page_id)
                    logger.warning(f'Reloading {url}...')
                    await asyncio.sleep(self.number_pages)
                    continue

                self.client.close_page_pool(page_id)
                return html

    async def close_client(self):
        """Close pool tabs"""
        async with self.lock:
            if self.running_client:
                self.running_client = False
                await self.client.close_pool(self.number_pages)

    async def save_page(self, url, html=''):
        if not html:
            html = await self.visit_page(url)
        with open(f'storage/{url.replace("/", "")}.html', 'w+') as f:
            f.write(html)
