"""
Defines the MapGraph
"""
import os
import pickle
import osmnx as ox
from typing import Optional, Tuple
from navigator.cost_functions import *
from networkx.classes.multidigraph import MultiDiGraph


class MapGraph:
    """
    MapGraph class to prepare, save, and download elevation graded graphs
    """

    def __init__(self, city: str, state: str, transport_mode: str, penalization_function: str, api_key: str,
                 cache_path: str):
        """
        Constructor method for the MapGraph

        :param city: city name for graph
        :param state: state name for graph
        :param transport_mode: transport mode (walk, bike)
        :param penalization_function: penalization function to use.
        :param api_key: api key for google maps elevation api
        :param cache_path: cache path for the graphs
        """
        self.INVALID_VALUES = ["", None]

        if city in self.INVALID_VALUES or state in self.INVALID_VALUES or transport_mode in self.INVALID_VALUES:
            raise ValueError(f"City, state and transport mode values cannot be {self.INVALID_VALUES}. Expected str")

        ox.settings.use_cache = False
        self.city = city
        self.state = state
        self.transport_mode = transport_mode
        self.__api_key = api_key
        self.cache_path = cache_path
        self.penalization_function = cost_functions_map[penalization_function]
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)

        self.graph = None

    def get_cached_graph_path(self):
        """
        Gets the cached graph path based on city, state and transport made
        :return: cache_file_path
        """
        cache_file_name = f'{self.city.lower()}_{self.state.lower()}_{self.transport_mode.lower()}_eleGraded.map'
        cache_file_path = os.path.join(self.cache_path, cache_file_name)
        return cache_file_path

    def download_graph(self):
        """
        Downloads the graph using city and state
        :return: MultiDiGraph for the specified city
        """

        query = {"city": self.city, "state": self.state, "country": "USA"}
        graph = ox.graph_from_place(query, network_type=self.transport_mode)
        return graph

    def add_elevation_grading(self, graph: MultiDiGraph):
        """
        Adds elevation grading to a graph using Google Maps Elevation API

        :param graph: Graph to be elevation graded
        :return: elevation graded graph
        """
        elevation_graph = ox.elevation.add_node_elevations_google(graph, api_key=self.__api_key)
        elevation_graded_graph = ox.elevation.add_edge_grades(elevation_graph)
        for u, v, k, data in elevation_graded_graph.edges(keys=True, data=True):
            data['elevation_cost'] = self.penalization_function(data['length'], data['grade'])
            data['elevation_gain'] = data['length'] * data['grade']

        return elevation_graded_graph

    def prepare_graph(self):
        """
        Integration function to download, cache, load and elevation grade the graph

        :return: None
        """
        cached_graph_path = self.get_cached_graph_path()
        if os.path.exists(cached_graph_path):
            with open(cached_graph_path, "rb") as f:
                elevation_graded_graph = pickle.load(f)
        else:
            graph = self.download_graph()
            elevation_graded_graph = self.add_elevation_grading(graph)
            self.save_graph(elevation_graded_graph, cached_graph_path)

        self.graph = elevation_graded_graph

    def get_graph(self):
        """
        Getter method for the elevation graded graph

        :return: elevation graded graph
        """
        return self.graph

    @staticmethod
    def save_graph(graph: MultiDiGraph, path: str):
        """
        Saves graph to the given path as pickle.

        throws FileNotFoundError if invalid path
        :param graph: graph to save
        :param path: save path
        :return: None
        """
        try:
            with open(path, "wb") as f:
                pickle.dump(graph, f)
        except FileNotFoundError:
            raise FileNotFoundError("Could not save the graph. Path does not exist")
