import threading

from fastapi import FastAPI, Request, HTTPException

from .kafka.admin import create_kafka_topics
from .kafka.consumer import from_kafka
from .model.cheque import Cheque
from .model.mappers import check_to_dict
from .data import banks_dict
from .kafka.producer import to_kafka
import asyncio

from .utils.logger import get_logger

app = FastAPI()
logger = get_logger(logname=__name__)


async def invoke_kafka_consumer():
    await from_kafka()


def invoke_callbacks():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(invoke_kafka_consumer())
    loop.close()


@app.on_event("startup")
async def startup_event():
    await create_kafka_topics()

    thread = threading.Thread(target=invoke_callbacks)
    thread.start()


@app.get('/accounts', )
async def get_all_accounts():
    logger.info('inbound request to get all banks accounts')
    return banks_dict


@app.get('/accounts/{bank_id}/', )
async def get_all_bank_accounts(bank_id: int):
    logger.info('inbound request to get all bank accounts')
    return banks_dict[bank_id].bank_accounts


@app.get('/accounts/{bank_id}/{account_id}', )
async def get_account_amount(bank_id: int, account_id: str):
    logger.info('inbound request to get a bank account detail')
    return banks_dict[bank_id].bank_accounts[account_id]


@app.post('/cheque-deposit/')
async def deposit_new_check(request: Request):

    try:

        request_json = await request.json()

        logger.info('inbound request to deposit new cheque')

        payee_bank_id = request_json["payee_bank_id"]
        drawee_bank_id = request_json["drawee_bank_id"]

        if payee_bank_id not in banks_dict or drawee_bank_id not in banks_dict:
            raise HTTPException(status_code=400, detail="Receiver / Sender bank id does not exist")

        if request_json["payee_id"] not in banks_dict[payee_bank_id].bank_accounts or request_json["drawee_id"] not in banks_dict[drawee_bank_id].bank_accounts:
            raise HTTPException(status_code=400,
                                detail="Issuer / Issued account ID does not exist at the receiver / sender bank")

        cheque = Cheque(payee_bank_id=payee_bank_id,
                        drawee_bank_id=drawee_bank_id,
                        payee_id=request_json["payee_id"],
                        drawee_id=request_json["drawee_id"],
                        chk_amount=request_json["chk_amount"])

        topic = f'{cheque.drawee_bank_id}.funds.cheques.clearinghouse'

        await to_kafka(topic=topic, key=cheque.payee_id, value=cheque, mapper=check_to_dict)

    except Exception as e:
        raise e
