import os
import pickle
import osmnx as ox
from typing import Optional, Tuple
from cost_functions import *
from networkx.classes.multidigraph import MultiDiGraph


class MapGraph:

    def __init__(self, city, state, transport_mode, penalization_function, api_key, cache_path):
        self.INVALID_VALUES = ["", None]

        if city in self.INVALID_VALUES or state in self.INVALID_VALUES or transport_mode in self.INVALID_VALUES:
            raise ValueError(f"City, state and transport mode values cannot be {self.INVALID_VALUES}. Expected str")

        self.city = city
        self.state = state
        self.transport_mode = transport_mode
        self.__api_key = api_key
        self.cache_path = cache_path
        self.penalization_function = cost_functions_map[penalization_function]
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)

        self.graph = self.prepare_graph()

    def get_cached_graph_path(self) -> str:
        cache_file_name = f'{self.city.lower()}_{self.state.lower()}_{self.transport_mode.lower()}_eleGraded.map'
        cache_file_path = os.path.join(self.cache_path, cache_file_name)
        return cache_file_path

    def download_graph(self) -> MultiDiGraph:

        query = {"city": self.city, "state": self.state, "country": "USA"}
        graph = ox.graph_from_place(query, network_type=self.transport_mode)
        return graph

    def add_elevation_grading(self, graph):
        elevation_graph = ox.elevation.add_node_elevations_google(graph, api_key=self.__api_key)
        elevation_graded_graph = ox.elevation.add_edge_grades(elevation_graph)
        for u, v, k, data in elevation_graded_graph.edges(keys=True, data=True):
            data['elevation_cost'] = self.penalization_function(data['length'], data['grade'])
            data['elevation_gain'] = data['length'] * data['grade']

        return elevation_graded_graph

    def prepare_graph(self):
        cached_graph_path = self.get_cached_graph_path()
        if os.path.exists(cached_graph_path):
            with open(cached_graph_path, "rb") as f:
                elevation_graded_graph = pickle.load(f)
        else:
            graph = self.download_graph()
            elevation_graded_graph = self.add_elevation_grading(graph)
            self.save_graph(elevation_graded_graph, cached_graph_path)

        return elevation_graded_graph

    def get_graph(self):
        return self.graph

    @staticmethod
    def save_graph(graph, path):
        try:
            with open(path, "wb") as f:
                pickle.dump(graph, f)
        except FileNotFoundError:
            raise FileNotFoundError("Could not save the graph. Path does not exist")
