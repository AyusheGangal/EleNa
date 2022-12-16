import unittest
from request_makers import *
import json
import os
import warnings

warnings.filterwarnings("ignore")


class NavigatorTests(unittest.TestCase):

    def setUp(self):
        self.city = "Amherst"
        self.state = "MA"
        self.transport_mode = "walk"
        self.from_address = "Cashin Hall, Amherst, MA"
        self.to_address = "497 East Pleasant Street, Amherst, MA"

    def test_DownloadGraphRequest(self):
        ele_graph = download_graph(self.city, self.state, self.transport_mode)
        self.assertNotEqual(ele_graph, None)

    def test_GetShortestPathFound(self):
        tolerance = 3.0
        output_data = get_shortest_path(self.from_address, self.to_address, self.city, self.state, self.transport_mode,
                                        tolerance)

        output_data_oracle = {'elevation_reduction': 7.488329476731935, 'found': True,
                              'location_dest': [42.3930599, -72.5117541],
                              'location_orig': [42.397504999999995, -72.52183607573964],
                              'original_elevation_gain': 36.661381, 'original_path_length': 1305.9959999999996,
                              'path': [2264432177, 2264432173, 2264432154, 8390507022, 2264432164, 6765025803,
                                       6765025805, 6765025804, 6765025816, 5506487800, 6765025817, 6313650218, 66655982,
                                       66612825, 6313650221, 66763147, 66715883, 7765182367, 66708872, 7558975175,
                                       9050970129], 'path_length_increase': 5.979038220637756}

        self.assertEqual(output_data, output_data_oracle)

    def test_GetShortestPathNotFound(self):
        tolerance = 1.0
        output_data = get_shortest_path(self.from_address, self.to_address, self.city, self.state, self.transport_mode,
                                        tolerance)

        output_data_oracle = {'elevation_reduction': 7.488329476731935, 'found': False,
                              'location_dest': [42.3930599, -72.5117541],
                              'location_orig': [42.397504999999995, -72.52183607573964],
                              'original_elevation_gain': 36.661381, 'original_path_length': 1305.9959999999996,
                              'path': [2264432177, 2264432173, 2264432154, 8390507022, 2264432164, 6765025803,
                                       6765025805, 6765025804, 6765025816, 5506487800, 6765025817, 6313650218, 66655982,
                                       66612825, 6313650221, 66763147, 66715883, 7765182367, 66708872, 7558975175,
                                       9050970129], 'path_length_increase': 5.979038220637756}

        self.assertEqual(output_data, output_data_oracle)

    def tearDown(self):
        self.city = None
        self.state = None
        self.transport_mode = None
        self.from_address = None
        self.to_address = None


if __name__ == '__main__':
    unittest.main()
