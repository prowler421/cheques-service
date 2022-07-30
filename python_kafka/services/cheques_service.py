from python_kafka.model.cheque import Cheque
from ..data import banks_dict


def is_cheque_stable(cheque: Cheque) -> bool:
    amount = banks_dict[cheque.bk_receiver_id].bank_accounts[cheque.issuer_account_id]
    return amount - cheque.chk_amount > 0
