import unittest
from navigator.map_graph import MapGraph
from navigator.navigator import Navigator
import json
import os
import warnings

warnings.filterwarnings("ignore")


class NavigatorTests(unittest.TestCase):
    """
    Tests for navigator
    """

    def setUp(self) -> None:
        with open("./config.json") as f:
            config = json.load(f)

        city = "Amherst"
        state = "MA"
        transport_mode = "walk"

        self.mapGraphObj = MapGraph(city=city,
                                    state=state,
                                    transport_mode=transport_mode,
                                    penalization_function=config["penalization_function"],
                                    api_key=config["apikey"],
                                    cache_path=config["cache_path"])

        self.mapGraphObj.prepare_graph()
        self.navigator_worker = Navigator()

        self.from_address = "Cashin Hall, Amherst, MA"
        self.to_address = "497 East Pleasant Street, Amherst, MA"

    def test_NavigatorObjectCreation(self):
        self.assertNotEqual(self.navigator_worker, None)

    def test_NavigatorGetAddressCoordinates(self):
        orig_coordinates = self.navigator_worker.get_address_coordinates(self.from_address)
        dest_coordinates = self.navigator_worker.get_address_coordinates(self.to_address)

        self.assertEqual(orig_coordinates, (42.397504999999995, -72.52183607573964))
        self.assertEqual(dest_coordinates, (42.3930599, -72.5117541))

    def test_NavigatorGetNavigationCoordinates(self):
        coordinates = self.navigator_worker.get_navigation_coordinates(self.from_address, self.to_address)
        self.assertEqual(coordinates, ((42.397504999999995, -72.52183607573964), (42.3930599, -72.5117541)))

    def test_NavigatorGetNavigationCoordinatesInvalid(self):
        coordinates = self.navigator_worker.get_navigation_coordinates(None, self.to_address)
        self.assertEqual(coordinates, None)

    def test_NavigatorGetShortestPath(self):
        shortest_path, location_orig, location_dest = self.navigator_worker.get_shortest_path(
            self.mapGraphObj.get_graph(),
            self.from_address, self.to_address)
        shortest_path_oracle = [2264432177, 2264432173, 2264432154, 8390507022, 2264432164, 6765025803,
                                6765025805, 6765025804, 6765025816, 5506487800, 4517215717, 4591913295,
                                4591913289, 4591919993, 4591919996, 4591919467, 4594410294, 5261586230,
                                4591913762, 66655982, 66612825, 6313650221, 66763147, 66715883, 7765182367,
                                66708872, 7558975175, 9050970129]

        self.assertEqual(shortest_path, shortest_path_oracle)
        self.assertEqual(location_orig, (42.397504999999995, -72.52183607573964))
        self.assertEqual(location_dest, (42.3930599, -72.5117541))

    def test_NavigatorGetAllShortestPaths(self):
        shortest_paths_by_elevation_lengths, shortest_path_by_distance, location_orig, location_dest = self.navigator_worker.get_all_shortest_paths(
            self.mapGraphObj.get_graph(), self.from_address, self.to_address)

        shortest_paths_by_elevation_lengths_oracle = [(1384.0819999999999,
                                                       [2264432177, 2264432173, 2264432154, 8390507022, 2264432164,
                                                        6765025803, 6765025805, 6765025804, 6765025816, 5506487800,
                                                        6765025817, 6313650218, 66655982, 66612825, 6313650221,
                                                        66763147, 66715883, 7765182367, 66708872, 7558975175,
                                                        9050970129])]

        shortest_paths_by_distance_oracle = [2264432177, 2264432173, 2264432154, 8390507022, 2264432164, 6765025803,
                                             6765025805, 6765025804, 6765025816, 5506487800, 4517215717, 4591913295,
                                             4591913289, 4591919993, 4591919996, 4591919467, 4594410294, 5261586230,
                                             4591913762, 66655982, 66612825, 6313650221, 66763147, 66715883, 7765182367,
                                             66708872, 7558975175, 9050970129]

        self.assertEqual(shortest_paths_by_elevation_lengths, shortest_paths_by_elevation_lengths_oracle)
        self.assertEqual(shortest_path_by_distance, shortest_paths_by_distance_oracle)
        self.assertEqual(location_orig, (42.397504999999995, -72.52183607573964))
        self.assertEqual(location_dest, (42.3930599, -72.5117541))

    def test_NavigatorFilterPathByToleranceFound(self):
        tolerance = 3.0
        graph = self.mapGraphObj.get_graph()
        all_shortest_path_data = self.navigator_worker.get_all_shortest_paths(
            graph, self.from_address, self.to_address)
        output = self.navigator_worker.filter_paths_by_tolerance(graph, all_shortest_path_data, tolerance)

        output_oracle = {'found': True,
                         'path': [2264432177, 2264432173, 2264432154, 8390507022, 2264432164, 6765025803, 6765025805,
                                  6765025804, 6765025816, 5506487800, 6765025817, 6313650218, 66655982, 66612825,
                                  6313650221, 66763147, 66715883, 7765182367, 66708872, 7558975175, 9050970129],
                         'original_elevation_gain': 36.661381, 'elevation_reduction': 7.488329476731935,
                         'original_path_length': 1305.9959999999996, 'path_length_increase': 5.979038220637756,
                         'location_orig': (42.397504999999995, -72.52183607573964),
                         'location_dest': (42.3930599, -72.5117541)}
        self.assertEqual(output, output_oracle)

    def test_NavigatorFilterPathByToleranceNotFound(self):
        tolerance = 1.0
        graph = self.mapGraphObj.get_graph()
        all_shortest_path_data = self.navigator_worker.get_all_shortest_paths(
            graph, self.from_address, self.to_address)
        output = self.navigator_worker.filter_paths_by_tolerance(graph, all_shortest_path_data, tolerance)

        output_oracle = {'found': False,
                         'path': [2264432177, 2264432173, 2264432154, 8390507022, 2264432164, 6765025803, 6765025805,
                                  6765025804, 6765025816, 5506487800, 6765025817, 6313650218, 66655982, 66612825,
                                  6313650221, 66763147, 66715883, 7765182367, 66708872, 7558975175, 9050970129],
                         'original_elevation_gain': 36.661381, 'elevation_reduction': 7.488329476731935,
                         'original_path_length': 1305.9959999999996, 'path_length_increase': 5.979038220637756,
                         'location_orig': (42.397504999999995, -72.52183607573964),
                         'location_dest': (42.3930599, -72.5117541)}
        self.assertEqual(output, output_oracle)

    def tearDown(self) -> None:
        self.mapGraphObj = None
        self.Navigator = None
        self.from_address = None
        self.to_address = None


if __name__ == '__main__':
    unittest.main()
