import networkx as nx
import osmnx as ox
import json
from geopy.geocoders import Nominatim
from networkx.classes.multidigraph import MultiDiGraph
import sys
import pickle
import os
from typing import Optional, Tuple

with open("map", "wb") as f:
    pickle.dump(graph, f)


class Navigator:

    def __init__(self, config_file: str):

        try:
            with open(config_file) as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print("File not found")  # Replace with logger
            sys.exit(1)

        self.INVALID_VALUES = ["", None]

    def get_address_coordinates(address: str) -> (float, float):
        address_locator = Nominatim(user_agent="ELeNa")
        location = address_locator.geocode(address)

        return location.latitude, location.longitude

    def get_navigation_coordinates(self, from_address: str, to_address: str) -> Optional[
        Tuple[(float, float), (float, float)]]:

        if from_address in self.INVALID_VALUES or to_address in self.INVALID_VALUES:
            print("Invalid values")
            return None

        from_coordinates = self.get_address_coordinates(from_address)
        to_coordinates = self.get_address_coordinates(to_address)

        return from_coordinates, to_coordinates

    def get_shortest_path(self,  graph:MultiDiGraph, from_address: str, to_address: str, weight="length"):
        location_orig, location_dest = self.get_navigation_coordinates(from_address, to_address)
        from_node = ox.nearest_nodes(graph, location_orig[1], location_orig[0])
        to_node = ox.nearest_nodes(graph, location_dest[1], location_dest[0])
        shortest_path = nx.shortest_path(graph, from_node, to_node, weight="length")
        return shortest_path, location_orig, location_dest

    def get_all_shortest_paths(self,  graph:MultiDiGraph, from_address: str, to_address: str, weight="elevation_cost"):
        pass