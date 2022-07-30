from .cheque import Cheque


def dict_to_check(obj, ctx):
    """
    Converts object literal(dict) to a User instance.
    Args:
        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.
        obj (dict): Object literal(dict)
    """
    if obj is None:
        return None

    return Cheque(chk_id=obj['chk_id'],
                  bk_sender_id=obj['bk_sender_id'],
                  bk_receiver_id=obj['bk_receiver_id'],
                  issuer_account_id=obj['issuer_account_id'],
                  issued_account_id=obj['issued_account_id'],
                  date=obj['date'],
                  chk_amount=obj['chk_amount'])


def check_to_dict(cheque: Cheque, ctx):
    """
    Returns a dict representation of a Cheque instance for serialization.

    Args:
        cheque (User): Cheque instance.

        ctx (SerializationContext): Metadata pertaining to the serialization operation.

    Returns:
        dict: Dict populated with cheque attributes to be serialized.

    """

    return dict(chk_id=cheque.chk_id,
                bk_sender_id=cheque.bk_sender_id,
                bk_receiver_id=cheque.bk_receiver_id,
                issuer_account_id=cheque.issuer_account_id,
                issued_account_id=cheque.issued_account_id,
                date=cheque.date,
                chk_amount=cheque.chk_amount)
