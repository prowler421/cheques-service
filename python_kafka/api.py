from fastapi import HTTPException, Request, APIRouter

from python_kafka.data import banks_dict
from python_kafka.kafka.producer import to_kafka
from python_kafka.model.cheque import Cheque
from python_kafka.model.mappers import check_to_dict
from python_kafka.utils.logger import get_logger

logger = get_logger(logname=__name__)
router = APIRouter()


@router.get('/accounts', status_code=200)
async def get_all_accounts():
    logger.info('inbound request to get all banks accounts')
    return banks_dict


@router.get('/accounts/{bank_id}/', status_code=200)
async def get_all_bank_accounts(bank_id: int):
    logger.info('inbound request to get all bank accounts')
    return banks_dict[bank_id].bank_accounts


@router.get('/accounts/{bank_id}/{account_id}', status_code=200)
async def get_account_amount(bank_id: int, account_id: str):
    logger.info('inbound request to get a bank account detail')
    return banks_dict[bank_id].bank_accounts[account_id]


@router.post('/cheque-deposit/', status_code=201)
async def deposit_new_check(request: Request):
    try:

        request_json = await request.json()

        logger.info('inbound request to deposit new cheque')

        payee_bank_id = request_json["payee_bank_id"]
        drawee_bank_id = request_json["drawee_bank_id"]

        if payee_bank_id not in banks_dict or drawee_bank_id not in banks_dict:
            raise HTTPException(status_code=400, detail="Receiver / Sender bank id does not exist")

        if request_json["payee_id"] not in banks_dict[payee_bank_id].bank_accounts or request_json["drawee_id"] not in \
                banks_dict[drawee_bank_id].bank_accounts:
            raise HTTPException(status_code=400,
                                detail="Issuer / Issued account ID does not exist at the receiver / sender bank")

        cheque = Cheque(payee_bank_id=payee_bank_id,
                        drawee_bank_id=drawee_bank_id,
                        payee_id=request_json["payee_id"],
                        drawee_id=request_json["drawee_id"],
                        chk_amount=request_json["chk_amount"])

        topic = f'{cheque.drawee_bank_id}.funds.cheques.clearinghouse'

        await to_kafka(topic=topic, key=cheque.payee_id, value=cheque, mapper=check_to_dict)

        logger.info("cheque {0} has been processed successfully".format(cheque.chk_id))

        response_object = {
            "id": cheque.chk_id,
            "description": 'cheque has been processed successfully',
        }
        return response_object

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'cheque process failed {e}')
