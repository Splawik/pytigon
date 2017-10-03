from django.conf import settings
from django.core.files.storage import Storage
from django.core.files import File

from fs.path import abspath, dirname
from fs.errors import ResourceNotFound as ResourceNotFoundError
from fs.error_tools import unwrap_errors

class FSStorage(Storage):
    def __init__(self, fs=None, base_url=None):
        if fs is None:
            fs = settings.DEFAULT_FILE_STORAGE_FS
        if base_url is None:
            base_url = settings.MEDIA_URL
        base_url = base_url.rstrip('/')
        self.fs = fs
        self.base_url = base_url

    def exists(self, name):
        return self.fs.isfile(name)

    def path(self, name):
        path = self.fs.getsyspath(name)
        if path is None:
            raise NotImplementedError
        return path

    #@unwrap_errors
    def size(self, name):
        with unwrap_errors(name):
            size = self.fs.getsize(name)
        return size
        #return self.fs.getsize(name)

    #@unwrap_errors
    def url(self, name):
        with unwrap_errors(name):
            ret = self.base_url + abspath(name)
        return ret
        #return self.base_url + abspath(name)

    #@unwrap_errors
    def _open(self, name, mode):
        with unwrap_errors(name):
            f = self.fs.open(name, mode)
        return File(f)
        #return File(self.fs.open(name, mode))

    #@unwrap_errors
    def _save(self, name, content):
        with unwrap_errors(name):
            self.fs.makedir(dirname(name), allow_recreate=True, recursive=True)
            self.fs.setcontents(name, content)
        return name

    @unwrap_errors
    def delete(self, name):
        with unwrap_errors(name):
            try:
                self.fs.remove(name)
            except ResourceNotFoundError:
                pass
            
