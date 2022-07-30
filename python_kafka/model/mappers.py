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
                  payee_bank_id=obj['payee_bank_id'],
                  drawee_bank_id=obj['drawee_bank_id'],
                  payee_id=obj['payee_id'],
                  drawee_id=obj['drawee_id'],
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
                payee_bank_id=cheque.payee_bank_id,
                drawee_bank_id=cheque.drawee_bank_id,
                payee_id=cheque.payee_id,
                drawee_id=cheque.drawee_id,
                date=cheque.date,
                chk_amount=cheque.chk_amount)
