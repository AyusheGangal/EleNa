import unittest
from navigator.map_graph import MapGraph
import json
import os
import warnings
warnings.filterwarnings("ignore")

class MapGraphTests(unittest.TestCase):
    """
    Tests for MapGraph
    """

    def setUp(self) -> None:
        with open("./config.json") as f:
            config = json.load(f)

        city = "Amherst"
        state = "MA"
        transport_mode = "walk"

        if os.path.exists("/shared_volume/cache/amherst_ma_walk_eleGraded.map"):
            os.remove("/shared_volume/cache/amherst_ma_walk_eleGraded.map")

        if os.path.exists("/shared_volume/cache/test.map"):
            os.remove("/shared_volume/cache/test.map")

        self.mapGraphObj = MapGraph(city=city,
                               state=state,
                               transport_mode=transport_mode,
                               penalization_function=config["penalization_function"],
                               api_key=config["apikey"],
                               cache_path=config["cache_path"])

    def test_MapGraphObjectCreation(self):
        self.assertNotEqual(self.mapGraphObj, None)

    def test_MapGraphDownloadGraph(self):
        graph = self.mapGraphObj.download_graph()
        self.assertNotEqual(graph, None)

    def test_MapGraphAddElevationGrading(self):
        graph = self.mapGraphObj.download_graph()
        ele_graded_graph = self.mapGraphObj.add_elevation_grading(graph)
        edge = list(ele_graded_graph.edges(data=True))[0]
        edge_attributes = list(edge[2].keys())
        self.assertIn("elevation_cost", edge_attributes)
        self.assertIn("elevation_gain", edge_attributes)

    def test_MapGraphPrepareGraph(self):
        self.mapGraphObj.prepare_graph()
        self.assertNotEqual(self.mapGraphObj.get_graph(), None)

    def test_MapGraphSaveGraph(self):
        graph = self.mapGraphObj.download_graph()
        MapGraph.save_graph(graph, "/shared_volume/cache/test.map")
        exists = os.path.exists("/shared_volume/cache/test.map")
        self.assertEqual(exists, True)

    def tearDown(self) -> None:
        self.mapGraphObj = None

if __name__ == '__main__':
    unittest.main()
