import typing

from pydantic import BaseModel


class Bank(BaseModel):

    bank_id: int
    bank_name: str
    bank_accounts: typing.Dict[str, int]
