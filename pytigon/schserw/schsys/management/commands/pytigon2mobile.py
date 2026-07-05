import contextlib
import os

from django.core.management.base import BaseCommand
from pyquery import PyQuery as pq

from pytigon_lib.schhttptools import httpclient

httpclient.init_embeded_django()

BASE_URL = "http://127.0.0.2"

SCAN_ELEMENTS = (
    ("a", "href"),
    ("button", "href"),
    ("link", "href"),
    ("script", "src"),
    ("img", "src"),
    ("form", "action"),
)

FILES_MAP = {"/": "/index.html", "/schsys/jsi18n/": "/schsys/jsi18n.js"}

SCANNED_URLS = []


class Command(BaseCommand):
    help = "export project to Apache Cordova"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dir",
            help="output path",
        )

    def handle(self, *args, **options):
        if "dir" in options:
            output_path = options["dir"]
        else:
            return

        client = httpclient.HttpClient("")

        parsed = set()

        def parse_url(base_url, path):
            nonlocal client
            url = base_url + path

            if url in SCANNED_URLS:
                return
            SCANNED_URLS.append(url)
            print("X: ", url)

            # if "schsimplecontrols_demo/standardcontrols" in url:
            #    print("X1: ", url)
            if url in parsed:
                return
            parsed.add(url)

            r = client.get(None, url, user_agent="webviewembeded")  # mozilla/0.0.1

            txt_file = False
            if r.ret_content_type and "text" in r.ret_content_type:
                txt_file = True

            # if not "/?" in path:
            if True:
                if path in FILES_MAP:
                    path2 = FILES_MAP[path]
                else:
                    path2 = path.split("?")[0]
                    if path2.endswith("/"):
                        path2 = path2 + "index.html"

                path3 = os.path.join(output_path, *(path2.split("/")))
                path4 = os.path.join(output_path, *(path2.split("/")[:-1]))
                with contextlib.suppress(OSError):
                    os.makedirs(path4, exist_ok=True)

                try:
                    with open(
                        os.path.join(output_path, *(path2.split("/"))), "wb"
                    ) as o:
                        if txt_file:
                            o.write(
                                r.ptr()
                                .replace(b'href="/', b'href="')
                                .replace(b'src="/', b'src="')
                                .replace(b'action="/', b'action="')
                                .replace(b"/?", b"/index.html?")
                                .replace(b'/" target', b'/index.html" target')
                            )
                        else:
                            o.write(r.ptr())
                except OSError:
                    pass

            if not txt_file:
                return

            try:
                buf = r.str()
            except Exception:
                return

            d = pq(buf)

            urls = []

            for scan in SCAN_ELEMENTS:
                x = d(scan[0])
                for item in x:
                    if scan[1] in item.attrib:
                        u = item.attrib[scan[1]]
                        if ".fview" in u:
                            urls.append(u.replace(".fview", ".js"))
                            urls.append(u.replace(".fview", ".html"))
                        else:
                            if "class" in item.attrib:
                                if "menu-href" in item.attrib["class"]:
                                    urls.append(u + "?fragment=page")
                                    continue
                            if (
                                # not "?" in u
                                u not in ("#", "/", "")
                                and not u.startswith("#")
                                and "://" not in u
                            ):
                                if "fragment=page" in u or "static" in u:
                                    urls.append(u)
                                else:
                                    if "?" in u:
                                        urls.append(u + "&fragment=page")
                                    else:
                                        urls.append(u + "?fragment=page")

            for url in urls:
                with contextlib.suppress(Exception):
                    parse_url(base_url, url)

        parse_url(BASE_URL, "/")
        parse_url(
            BASE_URL,
            "/static/fonts/fork-awesome/fonts/forkawesome-webfont.woff2",
        )
        parse_url(
            BASE_URL,
            "/static/fonts/fork-awesome/fonts/forkawesome-webfont.woff",
        )
        parse_url(
            BASE_URL,
            "/static/fonts/fork-awesome/fonts/forkawesome-webfont.ttf",
        )

        bp = "/"
        to_scan = []
        for dirpath, dnames, fnames in os.walk(output_path):
            for fname in fnames:
                if dirpath.endswith("/components"):
                    if fname.endswith(".js"):
                        p = os.path.join(dirpath, fname)
                        with open(p) as f:
                            for line in f.readlines():
                                if "BASE_PATH" in line:
                                    if line.strip().startswith("BASE_PATH"):
                                        with contextlib.suppress(Exception):
                                            bp = line.split('"')[1]
                                    else:
                                        try:
                                            x = line.split('"')
                                            i = 1
                                            while i < len(x):
                                                if x[i] != "|":
                                                    to_scan.append("/" + bp + x[i])
                                                i += 2
                                        except Exception:
                                            pass

        for s in to_scan:
            with contextlib.suppress(Exception):
                parse_url(BASE_URL, s)

        with open(os.path.join(output_path, "index.html")) as f:
            buf = f.read()
        with open(os.path.join(output_path, "index.html"), "w") as f:
            f.write(
                buf.replace(
                    '<script src="schsys/jsi18n.js"></script>',
                    '<script src="cordova.js"></script><script src="schsys/jsi18n.js"></script>',
                )
            )
