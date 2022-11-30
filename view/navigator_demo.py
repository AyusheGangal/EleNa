import networkx as nx
import osmnx as ox
import leafmap.foliumap as leafmap

def get_location_from_address(address: str) -> (float, float):
    """
    Get (lat, long) coordintates from address
    Args:
        address: string with address
    Returns:
        location: (lat, long) coordinates
    Example:
        location_orig = get_location_from_address("Gare du Midi, Bruxelles")
    """
    from geopy.geocoders import Nominatim

    locator = Nominatim(user_agent = "myapp")
    location = locator.geocode(address)

    return location.latitude, location.longitude

def get_location_coord(address_orig: str, address_dest: str):
    """
    Convert the origin and destination addresses into (lat, long) coordinates and find the
    graph of streets from the bounding box.
    Args:
        address_orig: departure address
        address_dest: arrival address
    Returns:
        graph: street graph from OpenStreetMap
        location_orig: departure coordinates
        location_dest: arrival coordinates
    Example:
        graph, location_orig, location_dest = get_graph("Gare du Midi, Bruxelles", "Gare du Nord, Bruxelles")
    """

    MARGIN = 0.1

    # find location by address
    location_orig = get_location_from_address(address_orig)
    location_dest = get_location_from_address(address_dest)

    return location_orig, location_dest

def get_graph():
    query = {"city":"Amherst", "state": "MA", "country": "USA"}
    graph = ox.graph_from_place(query, network_type="walk")
    return graph


def get_shortest_path(address_orig: str, address_dest: str, graph):
    location_orig, location_dest = get_location_coord(address_orig, address_dest)
    node_orig = ox.nearest_nodes(graph, location_orig[1], location_orig[0])
    node_dest = ox.nearest_nodes(graph, location_dest[1], location_dest[0])
    paths = nx.shortest_path(graph, node_orig, node_dest, weight="length")
    return paths, location_orig, location_dest

