"""
Defines functions to send HTTP requests to the worker
"""
import requests
import json
import os
from time import sleep
import pickle
import osmnx as ox
import networkx as nx
import os
from logger import logger


def download_graph(city: str, state: str, transport_mode: str):
    """
    Send HTTP request to the worker to download a graph

    :param city: City for which to download the graph
    :param state: State for which to download the graph
    :param transport_mode: Transport mode (walk, bike)
    :return: Elevation graded MultiDiGraph
    """
    api_hostname = os.environ.get("API_ADDRESS")

    url = f"{api_hostname}/download_graph"
    data = {'city': city, 'state': state, 'transport_mode': transport_mode}
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)

    if r.status_code == 200:
        cache_path = str(r.text)
        logger.info(cache_path)
    else:
        raise TimeoutError("Cannot get the graph. Try again.")

    poll_limit = 0
    while (not os.path.exists(cache_path)):
        if poll_limit > 5000:
            raise TimeoutError("Cannot get the graph. Try again.")
        poll_limit += 1
        sleep(0.5)

    sleep(1)  # Sometimes, it takes time for file system to update
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "rb") as f:
                elevation_graded_graph = pickle.load(f)
        except:
            raise FileNotFoundError("Cannot get the graph. Try again.")
    else:
        raise TimeoutError("Cannot get the graph. Try again.")

    return elevation_graded_graph


def get_shortest_path(from_address: str, to_address: str, city: str, state: str, transport_mode: str, tolerance: float):
    """
    Sends HTTP request to the worker to get the shortest elevation based path with statistics.

    :param from_address: Origin address
    :param to_address: Destination address
    :param city: City for which to download the graph
    :param state: State for which to download the graph
    :param transport_mode: Transport mode (walk, bike)
    :param tolerance: Tolerance for the shortest elevation based path
    :return: Dictionary with shortest path and statistics to display
    """
    api_hostname = os.environ.get("API_ADDRESS")

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
