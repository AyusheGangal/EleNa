import streamlit as st
import folium
import osmnx
import networkx as nx
import leafmap.foliumap as leafmap
import json


class gui:
    def __init__(self, filename="config.json"):
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
            lat, lon = 42.4529, -72.5653
            self.map = leafmap.Map(center=(lat, lon), zoom=16)
            self.map.add_basemap(self.basemap)
            self.map.to_streamlit()

    def generate_and_show_gui(self):

        with st.sidebar:
            st.markdown("<h1 style='text-align: center;font-size:60px;'>🧭</h1>", unsafe_allow_html=True)
            st.markdown("<h1 style='text-align: center;'>EleNa: Elevation Based Navigation System</h1>",
                        unsafe_allow_html=True)

            self.basemap = st.selectbox("Map Type", self.config['BASEMAPS'])
            if self.basemap in self.config['BASEMAPS'][1:]:
                self.basemap = self.basemap.upper()

            self.transport = st.selectbox("Method of Transportation", self.config['TRAVEL_MODE'])

            self.address_from = st.text_input("Go from", key="go_from")
            self.address_to = st.text_input("Go to", key="go_to")

            st.markdown("<h3 style='text-align: center;'>Tolerance</h3>", unsafe_allow_html=True)
            self.tolerance = st.slider(label="", min_value=1.0, max_value=5.0, label_visibility="collapsed", step=0.1,
                                       format="%f times")
            st.write("Shows path upto " + str(self.tolerance) + " times the shortest path")

            with st.columns(3)[1]:
                st.button("Clear", on_click=self.clear_text)

        with st.columns(7)[3]:
            st.button("Get Directions", on_click=self.get_directions, type="primary")

    def get_directions(self):
        if self.address_from == "" or self.address_to == "" or self.address_from == self.address_to:
            st.warning(" Invalid Source or Destination!", icon="⚠️")
        else:
            with st.spinner("Generating shortest route"):
                import time
                time.sleep(10)
                #TODO: Add function for getting shortest path

            st.success('Shortest route found', icon="✅")

    def clear_text(self):
        st.session_state["go_from"] = ""
        st.session_state["go_to"] = ""
