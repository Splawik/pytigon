from pathlib import Path


def pytest_ignore_collect(collection_path, config):
    if collection_path.name == "context_processors.py":
        return True
    return None

