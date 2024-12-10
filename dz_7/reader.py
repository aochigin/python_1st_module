from common import check_file_exists_throwable, FileObject


class InvalidCSVHeader(ValueError):
    pass

class InvalidCSV(ValueError):
    pass


class CSVParser(FileObject):
    def __init__(self, file_name, delimiter=',', required_fields=[]):
        super().__init__(file_name, "r")

        check_file_exists_throwable(self.file_name)
        self.__delimiter = delimiter
        self.__required_fields = set(required_fields)
        self.__header = {}
        self.__header_size = 0

    def _open_file(self):
        if self._file is None:
            self._file = open(self.file_name, "r")
            self.__read_csv_header()

    def __iter__(self):
        self._open_file()
        for i, line in enumerate(self._file):
            row_fields = line.rstrip('\r\n').split(self.__delimiter)
            self.__validate_csv_row(row_fields, i + 1)
            yield self.__fill_data(row_fields)

    def __validate_csv_header(self):
        header_fields = set(self.__header.values())
        if not all(header_fields):
            raise InvalidCSVHeader(f"CSV file: {self.file_name} with delimiter \"{self.__delimiter}\" has empty field")
        if len(header_fields) != len(self.__header.values()):
            raise InvalidCSVHeader(f"CSV file: {self.file_name} has duplicate field")
        if not all([field in self.header_fields for field in self.__required_fields]):
            raise InvalidCSVHeader(f"CSV file: {self.file_name} missing required field")
        self.__header_size = len(header_fields)

    def __read_csv_header(self):
        header_line = next(self._file).rstrip('\r\n')
        self.__header = {i: val for i, val in enumerate(header_line.split(self.__delimiter))}
        self.__validate_csv_header()

    def __validate_csv_row(self, row, index):
        if len(row) != self.__header_size:
            raise InvalidCSV(f"file: {self.file_name} line: {index} is invalid")

    def __fill_data(self, row):
        for i in range(len(row)):
            if not row[i] or row[i] == '-':
                row[i] = None
        element = {self.__header[i]: value for i, value in enumerate(row)}
        return element
