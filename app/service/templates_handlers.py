import os.path

from config import config


def get_greeting_text() -> str:
    path = os.path.join(os.getcwd(), "templates", "greeting.txt")
    if not os.path.exists(path):
        return config.MESSAGE_GREETING_DEFAULT_TEMPLATE

    with open(path) as f:
        template = f.read()

    if template:
        return template

    return config.MESSAGE_GREETING_DEFAULT_TEMPLATE


def get_bill_text(bill_url: str) -> str:
    path = os.path.join(os.getcwd(), "templates", "bill.txt")
    if not os.path.exists(path):
        return config.MESSAGE_BILL_DEFAULT_TEMPLATE

    with open(path) as f:
        template = f.read()

    template = template or config.MESSAGE_BILL_DEFAULT_TEMPLATE
    return template.format(
        bill_url=bill_url
    )


def get_cancel_text() -> str:
    path = os.path.join(os.getcwd(), "templates", "cancel.txt")
    if not os.path.exists(path):
        return config.MESSAGE_CANCEL_TEMPLATE

    with open(path) as f:
        template = f.read()

    template = template or config.MESSAGE_CANCEL_TEMPLATE
    return template


def get_paid_text() -> str:
    path = os.path.join(os.getcwd(), "templates", "paid.txt")
    if not os.path.exists(path):
        return config.MESSAGE_CANCEL_TEMPLATE

    with open(path) as f:
        template = f.read()

    template = template or config.MESSAGE_CANCEL_TEMPLATE
    return template
