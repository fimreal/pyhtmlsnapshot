# -*- coding:utf-8 -*-

import tempfile
import asyncio
from os.path import realpath, exists
from pyppeteer import launch
# from base64 import decode as bs64decode


class AHTMLConverter:
    def __init__(self, launch_options={}):
        self.launch_options = launch_options

    async def init(self):
        self.browser = await launch(
            **(
                {
                    "headless": True,
                    "handleSIGINT": False,
                    "handleSIGTERM": False,
                    "handleSIGHUP": False,
                    "args": ["--no-sandbox"],
                }
            ) | self.launch_options
        )

    async def finish(self):
        await self.browser.close()

    async def __aenter__(self):
        await self.init()
        return self

    async def __aexit__(self, *args):
        await self.finish()

    async def scrape_info(self, page, url, goto_options={}):
        goto_options = {
            "waitUntil": "load",
            "timeout": 0,
        } | goto_options
        await page.goto(url, **goto_options)
        await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')

    async def _out_from_page(self, page, outfile=None, render_options={}):
        if outfile:
            render_options["path"] = outfile
            if outfile.endswith(".pdf"):
                render_options = {
                    "format": "A4",
                } | render_options
                return await page.pdf(**render_options)

            render_options = {
                "fullPage": True
            } | render_options
        return await page.screenshot(**render_options)

    async def from_url(self, url: str, *args, goto_options={}, render_options={}):
        page = await self.browser.newPage()
        await self.scrape_info(page, url, goto_options)
        out = await self._out_from_page(page, args, render_options)
        await page.close()
        return out

    async def from_file(self, file_path: str, *args, goto_options={}, render_options={}):
        url = "file://" + realpath(file_path)
        return await self.from_url(url, args, goto_options=goto_options, render_options=render_options)

    async def from_string(self, content: str, *args, goto_options={}, render_options={}):
        with tempfile.NamedTemporaryFile(suffix=".html", delete=True) as f:
            f.write(content.encode())
            f.flush()
            return await self.from_file(file_path=f.name, args=args, goto_options=goto_options, render_options=render_options)


class HTMLConverter:
    def __init__(self, launch_options={}):
        self.converter = AHTMLConverter(launch_options)
        try:
            asyncio.get_event_loop().run_until_complete(self.converter.init())
        except RuntimeError:
            asyncio.set_event_loop((loop := asyncio.new_event_loop()))
            loop.run_until_complete(self.converter.init())

    def __del__(self):
        asyncio.get_event_loop().run_until_complete(self.converter.finish())

    def from_url(self, url: str, *args, goto_options={}, render_options={}):
        return asyncio.get_event_loop().run_until_complete(
            self.converter.from_url(args, goto_options, render_options)
        )

    def from_file(self, file_path: str, *args, goto_options={}, render_options={}):
        return asyncio.get_event_loop().run_until_complete(
            self.converter.from_file(args, goto_options, render_options)
        )

    def from_string(self, content: str, *args, goto_options={}, render_options={}):
        return asyncio.get_event_loop().run_until_complete(
            self.converter.from_string(args, goto_options, render_options)
        )


def snapshot(origin: str, *args,
             launch_options={},
             goto_options={},
             render_options={}):
    converter = HTMLConverter(launch_options)
    if origin.startswith("http"):
        return converter.from_url(origin, args, goto_options, render_options)
    if exists(origin):
        return converter.from_file(origin, args, goto_options, render_options)
    if origin != "":
        # origin = str(bs64decode(origin))
        return converter.from_string(origin, args, goto_options, render_options)
