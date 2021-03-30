import os
import sys
import logging
from loguru import logger
from prediction import nlp
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.logger import logger
from uvicorn import Config, Server
from files.token import token_prive


logger.add("out.log", backtrace=True, diagnose=True)

app = FastAPI()


LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG"))
JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging():
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(LOG_LEVEL)

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])


class Item(BaseModel):
    text: str
    token: str


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/sentiment")
async def read_item(item: Item):
    token = item.token
    text = item.text
    logger.warning(f"L'utilisateur a entré le token {token}, et le text {text}")

    # checking if token is the good one
    if token != token_prive:
        logger.error(f"L'utilisateur a entré un mauvais token {token}")
        return {
            "Message": "Token Invalide",
            "Status Code": 401
        }
    else:
        prediction = nlp(text)[0]['label'].capitalize()
        logger.waring(f"La prédiciton de  {text} est {prediction}")
        return {
            "text": text,
            "prediction": prediction,
            "Status Code": 200
        }


if __name__ == '__main__':
    server = Server(
        Config(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            debug=True,
            log_level=LOG_LEVEL,
        ),
    )
    # setup logging last, to make sure no library overwrites it
    # (they shouldn't, but it happens)
    setup_logging()
    server.run()

#if __name__ == "__main__":
#    import uvicorn

#    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, debug=True)