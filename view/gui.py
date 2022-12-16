"""
Defines GUI for the web app
"""
import streamlit as st
import folium
import osmnx
import networkx as nx
import leafmap.foliumap as leafmap
import json
from request_makers import *
import pickle


class elena_gui:
    """
    EleNa Streamlit GUI. Generates GUI and connects with backend to display the route.
    """

    def __init__(self, filename: str = "config.json"):
        """
        Constructor for elena_gui. Performs initialization from the provided configuration file
        :param filename: Path to configuration file
        """
        with open(filename) as config_file:
            self.config = json.load(config_file)

        self.address_to = ""
        self.address_from = ""
        self.transport = self.config['TRAVEL_MODE'][0]
        self.basemap = self.config['BASEMAPS'][0]
        self.tolerance = 1.0

        st.set_page_config(layout="wide")
        hide_menu_style = """
                <style>
                #MainMenu {visibility: hidden;}
                </style>
                """
        st.markdown(hide_menu_style, unsafe_allow_html=True)
        lat, lon = self.config['DEFAULT_LAT_LONG']
        self.map = leafmap.Map(center=(lat, lon), zoom=16)
        self.map.add_basemap(self.basemap)

    def generate_and_show_gui(self) -> None:
        """
        Generate and shows GUI for the app
        :return: None
        """
        with st.sidebar:
            st.markdown("<h1 style='text-align: center;font-size:60px;'>🧭</h1>", unsafe_allow_html=True)
            st.markdown("<h1 style='text-align: center;'>EleNa: Elevation Based Navigation System</h1>",
                        unsafe_allow_html=True)

            with st.form("Navigation Form"):
                self.transport = st.selectbox("Method of Transportation", self.config['TRAVEL_MODE'])
                self.address_from = st.text_input("From", key="go_from")
                self.address_to = st.text_input("To", key="go_to")
                self.tolerance = st.slider(label="tolerance", min_value=1.0, max_value=5.0,
                                           label_visibility="collapsed", step=0.1,
                                           format="%f times")
                st.write("Shows path upto " + str(self.tolerance) + " times the shortest path")

                # Every form must have a submit button.
                with st.columns(3)[1]:
                    submitted = st.form_submit_button("Get Directions", type="primary")

                if submitted:
                    self.get_directions()

        self.basemap = st.selectbox("Choose Map Type", self.config['BASEMAPS'])
        if self.basemap in self.config['BASEMAPS'][1:]:
            self.basemap = self.basemap.upper()
        self.map.add_basemap(self.basemap)

        self.map.to_streamlit()

    def get_directions(self) -> None:
        """
        OnClick event button for getting directions.

        1. Performs input validation

        2. Sends request to backend for route generation

        3. Updates map on the screen with the path
        :return:
        """

        if len(self.address_to.split(",")) < 3 or len(self.address_to.split(",")) < 3:
            st.warning(" Invalid Source or Destination!", icon="⚠️")
        else:
            to_city = self.address_to.split(",")[-2].strip().capitalize()
            to_state = self.address_to.split(",")[-1].strip().upper()

            from_city = self.address_from.split(",")[-2].strip().capitalize()
            from_state = self.address_from.split(",")[-1].strip().upper()

            if self.address_from == "" or self.address_to == "" or self.address_from == self.address_to:
                st.warning(" Invalid Source or Destination!", icon="⚠️")
            elif to_city != from_city or to_state != from_state:
                st.warning(" Source and Destination must be in the same city!", icon="⚠️")
            else:
                with st.spinner("Generating shortest route"):

                    graph = download_graph(from_city, from_state, self.transport.lower())
                    output_data = get_shortest_path(self.address_from, self.address_to,
                                                                            from_city, from_state,
                                                                            self.transport.lower(), self.tolerance)

                self.map.add_marker(location=list(output_data["location_orig"]),
                                    icon=folium.Icon(color='green', icon='map-pin', prefix='fa-solid'),
                                    tooltip=self.address_from)
                self.map.add_marker(location=list(output_data["location_dest"]),
                                    icon=folium.Icon(color='red', icon='map-pin', prefix='fa-solid'),
                                    tooltip=self.address_to)
                osmnx.plot_route_folium(graph, output_data["path"], self.map)

                if output_data["found"]:
                    st.success(f"Shortest elevation-based route found matching your requirements. \n It has {output_data['elevation_reduction']:.2f}% lesser elevation gain and {output_data['path_length_increase']:.2f}% longer than the shortest path", icon="✅")
                else:
                    st.warning(f"Shortest elevation-based route not found matching your requirements. This closest path has {output_data['elevation_reduction']:.2f}% lesser elevation gain and {output_data['path_length_increase']:.2f}% longer than the shortest path", icon="😔")