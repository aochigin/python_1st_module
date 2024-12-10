import os


def check_file_exists_throwable(file_name):
    if file_name is None:
        raise ValueError("file_name argument can not be None")
    if not isinstance(file_name, str):
        # may throw error if file_name does not have __str__ right? too lazy for that
        raise ValueError(f"file_name: {file_name} has to be str type")
    if not file_name:
        raise ValueError("file_name argument can not be empty")
    if not os.path.isfile(file_name):
        raise ValueError(f"Specified file: {file_name} is not accessible")


def check_file_exists(file_name):
    try:
        check_file_exists_throwable(file_name)
    except ValueError:
        return False
    return True


class FileObject():
    def __init__(self, file_name, mode):
        self.file_name = file_name
        self._file = None
        self._mode = mode

    def _open_file(self):
        if self._file is None:
            self._file = open(self.file_name, self._mode)

    def _close_file(self):
        if self._file is not None and not self._file.closed:
            self._file.close()

    def __enter__(self):
        self._open_file()
        return self

    def __exit__(self, type_unused, value_unused, traceback_unused):
        self._close_file()

    def __del__(self):
        self._close_file()
