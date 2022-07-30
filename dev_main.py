import uvicorn
from dotenv import load_dotenv

from python_kafka.utils.logger import get_logger

load_dotenv()

if __name__ == "__main__":

    logger = get_logger(logname=__name__)

    uvicorn.run(
        "python_kafka.main:app", host="0.0.0.0", port=8004, log_level="debug", reload=True
    )

