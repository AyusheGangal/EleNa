from datetime import datetime, date
import json
from glob import glob
import os

config = json.load(open("./config.json"))

log_file = open(config["log_path"])
cache_files = glob(config["cache_path"])

for log in log_file:

    if len(cache_files) == 0:
        # Nothing in cache. No need to run the LRU cacher
        break

    date, log_cached_file = log.split()
    log_cached_file = log_cached_file.rstrip()

    date = datetime.strptime(date, "%Y-%m-%d").date()
    today_date = date.today()
    delta = today_date - date

    if delta.days > 20:
        # To stop checking logs after 20 days in past as LRU cache runs every day
        break

    if log_cached_file in cache_files:
        if delta.days > 1:
            os.remove(log_cached_file)