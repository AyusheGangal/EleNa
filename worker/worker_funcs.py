from navigator.map_graph import MapGraph
from navigator.navigator import Navigator
from flask import request, after_this_request, Response, jsonify
import json
from time import sleep

with open("./config.json") as f:
    config = json.load(f)


def download_graph():
    data = request.get_json()
    city = data["city"]
    state = data["state"]
    transport_mode = data["transport_mode"]

    mapGraphObj = MapGraph(city=city,
                           state=state,
                           transport_mode=transport_mode,
                           penalization_function=config["penalization_function"],
                           api_key=config["apikey"],
                           cache_path=config["cache_path"])

    cache_path = Response(mapGraphObj.get_cached_graph_path())

    @cache_path.call_on_close
    def start_download():
        mapGraphObj = MapGraph(city=city,
                               state=state,
                               transport_mode=transport_mode,
                               penalization_function=config["penalization_function"],
                               api_key=config["apikey"],
                               cache_path=config["cache_path"])
        mapGraphObj.prepare_graph()

    return cache_path, 200


def get_shortest_path():
    data = request.get_json()
    from_address = data["from_address"]
    to_address = data["to_address"]
    city = data["city"]
    state = data["state"]
    transport_mode = data["transport_mode"]
    tolerance = data["tolerance"]

    mapGraphObj = MapGraph(city=city,
                           state=state,
                           transport_mode=transport_mode,
                           penalization_function=config["penalization_function"],
                           api_key=config["apikey"],
                           cache_path=config["cache_path"])

    mapGraphObj.prepare_graph()
    graph = mapGraphObj.get_graph()
    navigator_worker = Navigator()
    all_shortest_paths_data = navigator_worker.get_all_shortest_paths(graph, from_address, to_address)
    path_and_stats = navigator_worker.filter_paths_by_tolerance(graph, all_shortest_paths_data, tolerance)

    return jsonify(path_and_stats), 200

