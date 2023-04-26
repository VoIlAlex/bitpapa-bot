from datetime import datetime

from pydantic import BaseModel


class BillAmount(BaseModel):
    currency: str
    value: str


class BillStatus(BaseModel):
    value: str
    changedDateTime: datetime


class BillCustomer(BaseModel):
    email: str
    phone: str
    account: str


class Bill(BaseModel):
    siteId: str
    billId: str
    amount: BillAmount
    status: BillStatus
    customer: BillCustomer
    customFields: dict
    comment: str
    creationDateTime: datetime
    expirationDateTime: datetime
    payUrl: str
