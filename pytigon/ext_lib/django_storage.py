from django.conf import settings
from django.core.files.storage import Storage
from django.core.files import File

from fs.path import abspath, dirname
from fs.errors import ResourceNotFound as ResourceNotFoundError
from fs.error_tools import unwrap_errors


class FSStorage(Storage):
    def __init__(self, fs=None, base_url=None):
        if fs is None:
            fs = settings.DEFAULT_FILE_STORAGE_FS()
        # print("U1: ", base_url, settings.MEDIA_URL)
        # if base_url is None:
        #    base_url = settings.MEDIA_URL
        # base_url = base_url.rstrip("/")
        # base_url = ""
        self.fs = fs
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = ""
        # print("BASE:", self.base_url)

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
        path = self.fs.getsyspath(name)
        if path is None:
            raise NotImplementedError
        return path

    def size(self, name):
        with unwrap_errors(name):
            size = self.fs.getsize(name)
        return size

    def url(self, name):
        with unwrap_errors(name):
            ret = self.base_url + abspath(name)
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
        return "/" + filename


class StaticFSStorage(FSStorage):
    def __init__(self, fs=None, base_url=None):
        super().__init__(fs, "/static")

    def generate_filename(self, filename):
        return "/static/" + filename

    def url(self, *argi, **argv):
        ret = super().url(*argi, **argv)
        print(ret)
        return ret


class MediaFSStorage(FSStorage):
    def __init__(self, fs=None, base_url=None):
        super().__init__(fs, "/media")

    def generate_filename(self, filename):
        return "/media/" + filename
