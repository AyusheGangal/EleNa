import logging
import json

with open("./config.json") as f:
    config = json.load(f)

logging.basicConfig(filename=config["log_path"],
                    filemode="a",
                    format='%(asctime)s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d')

logger = logging.getLogger("ViewLogger")
logger.info("Hello")
