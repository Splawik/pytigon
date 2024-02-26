def main():
    from django.conf import settings
    from django.core.files.base import ContentFile
    from django.core.files.storage import default_storage

    path1 = default_storage.save("/site_media/test1.txt", ContentFile(b"content1"))
    path2 = default_storage.save(
        "/filer_public_thumbnails/test2.txt", ContentFile(b"content2")
    )
    print("UPLOAD_PATH: ", settings.UPLOAD_PATH)
    print(path1)
    print(path2)
