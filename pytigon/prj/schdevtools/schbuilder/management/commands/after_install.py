import sys
import os.path
from pathlib import Path
import shutil


from django.core.management.base import BaseCommand
from pytigon_lib.schtools.main_paths import get_main_paths
from pytigon_lib.schfs.download import download_and_process_file

FILES_AUBE = [
    { 
        "os": "Linux",
        "url": "https://github.com/jdx/aube/releases/download/v1.22.0/aube-v1.22.0-x86_64-unknown-linux-musl.tar.gz",
        "path": "",
        "unpack": "tgz"
    },
    { 
        "os": "Windows",
        "url": "https://github.com/jdx/aube/releases/download/v1.22.0/aube-v1.22.0-x86_64-pc-windows-msvc.zip",
        "path": "",
        "unpack": "zip"
    }        
]

FILES_ESBUILD = [
    { 
        "os": "Linux",
        "url": "https://registry.npmjs.org/@esbuild/linux-x64/-/linux-x64-0.28.1.tgz",
        "path": "",
        "unpack": "tgz",
    },
    { 
        "os": "Windows",
        "url": "https://registry.npmjs.org/@esbuild/win32-x64/-/win32-x64-0.28.1.tgz",
        "path": "",
        "unpack": "tgz",
    }        
]


class Command(BaseCommand):
    help = "Install additional tools"

    def handle(self, *args, **options):
        paths = get_main_paths("schdevtools")
        data_path = paths["DATA_PATH"]
        prg_path = os.path.join(data_path, "prg")
        FILES_AUBE[0]["path"] = prg_path
        FILES_AUBE[1]["path"] = prg_path
        FILES_ESBUILD[0]["path"] = prg_path
        FILES_ESBUILD[1]["path"] = prg_path
        download_and_process_file(FILES_AUBE)
        download_and_process_file(FILES_ESBUILD)
        source = Path(os.path.join(prg_path, "package", "bin"))
        dest = Path(prg_path)
        for f in source.glob("*"):
            shutil.move(f, dest)
        shutil.rmtree(os.path.join(prg_path, "package"))
