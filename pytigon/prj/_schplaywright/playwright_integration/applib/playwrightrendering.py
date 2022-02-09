from playwright.sync_api import sync_playwright
import pytigon_lib.schhtml.htmlviewer
from playwright.sync_api import sync_playwright
import io

class PlayWrightRendering(pytigon_lib.schhtml.htmlviewer.BaseRenderingLib):
    def render(
        html,
        output_stream=None,
        css=None,
        width=int(210 * 72 / 25.4),
        height=int(297 * 72 / 25.4),
        stream_type="pdf",
        base_url=None,
        info=None
    ):
        with sync_playwright() as p:
            browser_type = p.chromium
            browser = browser_type.launch()
            page = browser.new_page()
            if type(html) == str:
                html2 = html
            else:
                html2 = html.decode("utf-8")

            if html2.startswith("http"):
                page.goto(html2.split("\n")[0].strip())
            else:
                page.set_content(html2)
            buf = page.pdf()
            result = io.BytesIO(buf)
            browser.close()
            return result

    def accept(html, stream_type="pdf", base_url=None, info=None):
        if stream_type == "pdf":
            return True
        return False

pytigon_lib.schhtml.htmlviewer.set_endering_lib(PlayWrightRendering)
