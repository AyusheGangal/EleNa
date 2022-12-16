"""
Defines logger and logger config
"""
import logging
import json

with open("./config.json") as f:
    config = json.load(f)

logging.root.handlers = []
logging.basicConfig(format='%(asctime)s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d',
                    handlers=[
                        logging.FileHandler(config["log_path"], mode="a"),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger("ViewLogger")
logger.info("Starting Logger")
