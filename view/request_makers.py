import requests
import json
import os
from time import sleep
import pickle
import osmnx as ox
import networkx as nx


def download_graph(city, state, transport_mode):
    with open("./config.json") as f:
        config = json.load(f)

    api_hostname = config["API_ADDRESS"]

    url = f"{api_hostname}/download_graph"
    data = {'city': city, 'state': state, 'transport_mode': transport_mode}
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)

    if r.status_code == 200:
        cache_path = str(r.text)
    else:
        raise TimeoutError("Cannot get the graph. Try again.")

    poll_limit = 0
    while (not os.path.exists(cache_path)):
        if poll_limit > 500:
            raise TimeoutError("Cannot get the graph. Try again.")
        poll_limit += 1
        sleep(0.5)

    print(cache_path)
    if os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            elevation_graded_graph = pickle.load(f)
    else:
        raise TimeoutError("Cannot get the graph. Try again.")

    return elevation_graded_graph


def get_shortest_path(from_address, to_address, city, state, transport_mode, tolerance):
    with open("./config.json") as f:
        config = json.load(f)

    api_hostname = config["API_ADDRESS"]

    url = f"{api_hostname}/get_shortest_path"
    data = {'city': city, 'state': state, 'transport_mode': transport_mode, "from_address": from_address,
            "to_address": to_address, "tolerance": tolerance}
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)

    if r.status_code == 200:
        output_data = r.json()
    else:
        raise TimeoutError("Cannot get the shortest path. Try again.")

    return output_data
