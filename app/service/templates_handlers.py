import os.path

from config import config


def get_template(name: str, default: str):
    path = os.path.join(os.getcwd(), "templates", f"{name}.txt")
    if not os.path.exists(path):
        return default

    with open(path) as f:
        template = f.read()

    template = template or default
    return template


def get_greeting_text() -> str:
    return get_template("greeting", config.MESSAGE_GREETING_DEFAULT_TEMPLATE)


def get_bill_text(bill_url: str) -> str:
    template = get_template("bill", config.MESSAGE_BILL_DEFAULT_TEMPLATE)
    return template.format(
        bill_url=bill_url
    )


def get_cancel_text() -> str:
    return get_template("cancel", config.MESSAGE_CANCEL_TEMPLATE)


def get_paid_text() -> str:
    return get_template("paid", config.MESSAGE_PAID_TEMPLATE)


def get_wrong_phone_format_text() -> str:
    return get_template("wrong_phone", config.MESSAGE_WRONG_PHONE_FORMAT)


def get_phone_success_text() -> str:
    return get_template("phone_success", config.MESSAGE_PHONE_SUCCESS)

