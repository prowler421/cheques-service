from datetime import datetime
import uuid

from pydantic import BaseModel


class Cheque(BaseModel):

    chk_id = str(uuid.uuid4())
    bk_sender_id: int
    bk_receiver_id: int
    issuer_account_id: str
    issued_account_id: str
    date = datetime.now().isoformat()
    chk_amount: int
