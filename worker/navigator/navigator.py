import networkx as nx
import osmnx as ox
import json
from geopy.geocoders import Nominatim
from networkx.classes.multidigraph import MultiDiGraph
import sys
import pickle
import os
from typing import Optional, Tuple


class Navigator:

    def __init__(self):
        self.INVALID_VALUES = ["", None]

    def get_address_coordinates(self, address: str):
        address_locator = Nominatim(user_agent="ELeNa")
        location = address_locator.geocode(address)

        return location.latitude, location.longitude

    def get_navigation_coordinates(self, from_address: str, to_address: str):

        if from_address in self.INVALID_VALUES or to_address in self.INVALID_VALUES:
            print("Invalid values")
            return None

        from_coordinates = self.get_address_coordinates(from_address)
        to_coordinates = self.get_address_coordinates(to_address)

        return from_coordinates, to_coordinates

    def get_shortest_path(self, graph: MultiDiGraph, from_address: str, to_address: str, weight="length"):
        location_orig, location_dest = self.get_navigation_coordinates(from_address, to_address)
        from_node = ox.nearest_nodes(graph, location_orig[1], location_orig[0])
        to_node = ox.nearest_nodes(graph, location_dest[1], location_dest[0])
        shortest_path = nx.shortest_path(graph, from_node, to_node, weight=weight)
        return shortest_path, location_orig, location_dest

    def get_all_shortest_paths(self, graph: MultiDiGraph, from_address: str, to_address: str, weight="elevation_cost"):
        location_orig, location_dest = self.get_navigation_coordinates(from_address, to_address)
        from_node = ox.nearest_nodes(graph, location_orig[1], location_orig[0])
        to_node = ox.nearest_nodes(graph, location_dest[1], location_dest[0])
        shortest_paths_by_elevation = nx.all_shortest_paths(graph, from_node, to_node, weight=weight)
        shortest_path_by_distance = nx.shortest_path(graph, from_node, to_node, weight="length")
        shortest_paths_by_elevation_lengths = []

        for path in shortest_paths_by_elevation:
            length = sum(ox.utils_graph.get_route_edge_attributes(graph, path, 'length'))
            shortest_paths_by_elevation_lengths.append((length, path))

        shortest_paths_by_elevation_lengths = sorted(shortest_paths_by_elevation_lengths, key=lambda x: x[0])
        return shortest_paths_by_elevation_lengths, shortest_path_by_distance, location_orig, location_dest

    def filter_paths_by_tolerance(self, graph, all_shortest_path_data, tolerance):
        shortest_path = all_shortest_path_data[1]
        elevation_based_paths = all_shortest_path_data[0]
        location_orig = all_shortest_path_data[2]
        location_dest = all_shortest_path_data[3]
        shortest_path_length = sum(ox.utils_graph.get_route_edge_attributes(graph, shortest_path, 'length'))
        shortest_path_elevation_gain = 0

        for ele_gain in ox.utils_graph.get_route_edge_attributes(graph, shortest_path, 'elevation_gain'):
            if ele_gain > 0:
                shortest_path_elevation_gain += ele_gain

        max_path_length = tolerance * shortest_path_length

        path_found = True if elevation_based_paths[0][0] <= max_path_length else False
        shortest_path_elevation_based = elevation_based_paths[0][1]
        shortest_path_elevation_based_elevation_gain = 0

        for ele_gain in ox.utils_graph.get_route_edge_attributes(graph, shortest_path_elevation_based,
                                                                 'elevation_gain'):
            if ele_gain > 0:
                shortest_path_elevation_based_elevation_gain += ele_gain

        elevation_reduction = 100 * ((shortest_path_elevation_gain - shortest_path_elevation_based_elevation_gain) / shortest_path_elevation_gain)
        path_length_increase = 100 * ((elevation_based_paths[0][0] - shortest_path_length) / shortest_path_length)

        output_dict = {
            "found": path_found,
            "path": shortest_path_elevation_based,
            "original_elevation_gain": shortest_path_elevation_gain,
            "elevation_reduction": elevation_reduction,
            "original_path_length": shortest_path_length,
            "path_length_increase": path_length_increase,
            "location_orig": location_orig,
            "location_dest": location_dest
        }

        return output_dict
