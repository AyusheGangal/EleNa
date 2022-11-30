import streamlit as st
import folium
import osmnx
import networkx as nx
import leafmap.foliumap as leafmap
import json


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
                self.address_from = st.text_input("Go from", key="go_from")
                self.address_to = st.text_input("Go to", key="go_to")
                self.tolerance = st.slider(label="tolerance", min_value=1.0, max_value=5.0,
                                           label_visibility="collapsed", step=0.1,
                                           format="%f times")
                st.write("Shows path upto " + str(self.tolerance) + " times the shortest path")

                # Every form must have a submit button.
                with st.columns(3)[1]:
                    submitted = st.form_submit_button("Get Directions", type="primary")

                if submitted:
                    self.get_directions()

        self.map.to_streamlit()


    def get_directions(self) -> None:
        """
        OnClick event button for getting directions.

        1. Performs input validation

        2. Sends request to backend for route generation

        3.
        :return:
        """
        if self.address_from == "" or self.address_to == "" or self.address_from == self.address_to:
            st.warning(" Invalid Source or Destination!", icon="⚠️")
        else:
            with st.spinner("Generating shortest route"):
                import time
                time.sleep(1)

                # TODO: Add function for getting shortest path
            self.map.set_center(13,23)
            st.success('Shortest route found', icon="✅")