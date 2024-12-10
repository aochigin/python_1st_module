import argparse

from common import check_file_exists_throwable
from reader import CSVParser
from printer import TemplatePrinter


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file', help='File path to CSV database', required=True, type=str)
    parser.add_argument('-o','--output', help='File path to output TXT file', required=True, type=str)
    args = parser.parse_args()
    check_file_exists_throwable(args.file)
    return args

# Business logic that is not appliable as template but has to be applied
def format_row(field, value):
    # I would actually do this as global, but task probitis
    DEVICE_TYPE_MAP = {
        "mobile": "мобильного",
        "tablet": "планшетного",
        "laptop": "ноутбучного",
        "desktop": "десктопного"
    }
    SEX_MAP = {
        "male": "мужского пола",
        "female": "женского пола"
    }
    # First all as is
    if field == "device_type":
        return DEVICE_TYPE_MAP[value]
    elif field == "sex":
        return SEX_MAP[value]
    elif field == "age":
        if value.endswith("1") and not value.endswith("11"):
            return value + " года"
        else:
            return value + " лет"
    elif field == "bill":
        return value + " у.е."
    elif field == "region":
        if value is None:
            return "регион не определен"
    return value


def main():
    args = parse_arguments()
    # template is task specific, but let's hardcode the one for this homework
    template = "Пользователь %name% %sex%, %age% совершил%gender_ending% покупку на %bill% с %device_type% браузера %browser%. Регион, из которго совершалась покупка: %region%."
    with CSVParser(args.file) as parser, TemplatePrinter(args.output, template, format_row) as writer:
        for data in parser:
            writer.write(data)


if __name__ == "__main__":
    main()
