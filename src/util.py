from pathlib import Path


def get_storage_file_path() -> Path:
    root_path = Path(os.environ.get("ROOT_PATH"))
    storage_file = Path(os.environ.get("STORAGE_FILE"))
    storage_path = root_path / storage_file
    return storage_path
