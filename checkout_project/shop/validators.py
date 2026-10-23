
import re

CMD = re.compile(
    r"^add\s+(?P<item>[A-Za-z]+)\s+(?P<price>\d+)$",
    re.IGNORECASE
)

CASHIER_PATTERN = re.compile(r"CSH-\d{4}")

PHONE_PATTERN = re.compile(
    r"(?:0(?:70|80|81|90|91)\d{8}|\+?234(?:70|80|81|90|91)\d{8})"
)


def validate_cashier_id(value):
    if not CASHIER_PATTERN.fullmatch(value):
        raise ValueError("Cashier ID must follow CSH-0000 format.")
    return value


def validate_phone(value):
    if not PHONE_PATTERN.fullmatch(value):
        raise ValueError(
            "Enter a valid Nigerian phone number, e.g. 08011223344."
        )
    return value
