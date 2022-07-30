from datetime import datetime
import uuid

from pydantic import BaseModel


class Cheque(BaseModel):

    chk_id = str(uuid.uuid4())
    payee_bank_id: int
    drawee_bank_id: int
    payee_id: str
    drawee_id: str
    date = datetime.now().isoformat()
    chk_amount: int
