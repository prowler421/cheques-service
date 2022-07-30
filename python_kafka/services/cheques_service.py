from python_kafka.model.cheque import Cheque
from ..data import banks_dict


def is_cheque_stable(cheque: Cheque) -> bool:
    amount = banks_dict[cheque.drawee_bank_id].bank_accounts[cheque.drawee_id]
    return amount - cheque.chk_amount > 0
