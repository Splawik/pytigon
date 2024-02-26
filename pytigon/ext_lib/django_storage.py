import os

from django.conf import settings
from django.core.files.storage import Storage, FileSystemStorage
from django.core.files import File
from django.utils.deconstruct import deconstructible
from django.utils.encoding import filepath_to_uri

from urllib.parse import urljoin

from fs.path import abspath, dirname
from fs.errors import ResourceNotFound as ResourceNotFoundError
from fs.error_tools import unwrap_errors
from fs.osfs import OSFS


class OSFS_EXT(OSFS):
    def __init__(self, path, **argv):
        if not os.path.exists(path):
            os.makedirs(path)
        return super().__init__(path, **argv)


@deconstructible
class ThumbnailFileSystemStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None, *args, **kwargs):
        if location is None:
            location = settings.THUMBNAIL_MEDIA_ROOT or None
        if base_url is None:
            base_url = settings.THUMBNAIL_MEDIA_URL or None
        super().__init__(location, base_url, *args, **kwargs)

    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        url = filepath_to_uri(name)
        url = url.replace(settings.THUMBNAIL_MEDIA_ROOT, "")
        if url is not None:
            url = url.lstrip("/")
        return urljoin(self.base_url, url)


class FSStorage(Storage):
    def __init__(self, fs=None, base_url=None):
        if fs is None:
            fs = settings.DEFAULT_FILE_STORAGE_FS()
        self.fs = fs
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = ""

    def save(self, name, content, max_length=None):
        if name is None:
            name = content.name

        if not hasattr(content, "chunks"):
            content = File(content, name)
        name = self.get_available_name(name, max_length=max_length)
        name = self._save(name, content)
        return name

    def validate_file_name(name, allow_relative_path=True):
        return True

    def get_available_name(self, name, max_length=None):
        name = str(name).replace("\\", "/")
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        while self.exists(name) or (max_length and len(name) > max_length):
            name = dir_name + "/" + self.get_alternative_name(file_root, file_ext)
            if max_length is None:
                continue
            truncation = len(name) - max_length
            if truncation > 0:
                file_root = file_root[:-truncation]
                name = dir_name + "/" + self.get_alternative_name(file_root, file_ext)
        return name

    def exists(self, name):
        return self.fs.isfile(name) or self.fs.isdir(name)

    def isdir(self, name):
        return self.fs.isdir(name)

    def listdir(self, name):
        x = list(self.fs.scandir(name))
        dirs = [pos.name for pos in x if pos.isdir]
        files = [pos.name for pos in x if not pos.isdir]
        return (dirs, files)

    def path(self, name):
        try:
            path = self.fs.getsyspath(name)
        except:
            raise NotImplementedError
        if path is None:
            raise NotImplementedError
        return path

    def size(self, name):
        with unwrap_errors(name):
            size = self.fs.getsize(name)
        return size

    def url(self, name):
        with unwrap_errors(name):
            ret = self.base_url + abspath(name)[1:]
        return ret

    def _open(self, name, mode):
        with unwrap_errors(name):
            f = self.fs.open(name, mode)
        return File(f)

    def _save(self, name, content):
        with unwrap_errors(name):
            self.fs.makedirs(dirname(name), recreate=True)
            self.fs.setbinfile(name, content)
        return name

    def delete(self, name):
        with unwrap_errors(name):
            try:
                self.fs.remove(name)
            except ResourceNotFoundError:
                pass

    def get_accessed_time(self, name):
        info = self.fs.getinfo(name, namespaces=["details"])
        return info.accessed

    def get_created_time(self, name):
        info = self.fs.getinfo(name, namespaces=["details"])
        return info.created

    def get_modified_time(self, name):
        info = self.fs.getinfo(name, namespaces=["details"])
        return info.modified

    def generate_filename(self, filename):
        return filename


class StaticFSStorage(FSStorage):
    def __init__(self, fs=None, base_url=None):
        if fs is None:
            fs = settings.STATIC_FILE_STORAGE_FS()
        self.fs = fs
        super().__init__(fs, settings.STATIC_URL)

    def generate_filename(self, filename):
        return "/static/" + filename

    def url(self, *argi, **argv):
        ret = super().url(*argi, **argv)
        return ret
