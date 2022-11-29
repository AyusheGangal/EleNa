import streamlit as st
import folium
import osmnx
import networkx as nx
import leafmap.foliumap as leafmap
import json

class gui:
    def __init__(self, filename = "config.json"):
        with open(filename) as config_file:
            self.config = json.load(config_file)
    
    def clear_text(self):
        st.session_state["go_from"] = ""
        st.session_state["go_to"] = ""

    def generate_and_show_gui(self):
        with st.sidebar:
            st.markdown("<h1 style='text-align: center;font-size:100px;'>🧭</h1>", unsafe_allow_html=True)
            st.markdown("<h1 style='text-align: center;'>EleNa: Elevation Based Navigation System</h1>", unsafe_allow_html=True)

            basemap = st.selectbox("Select Map Type", self.config['BASEMAPS'])
            if basemap in self.config['BASEMAPS'][:-1]:
                basemap=basemap.upper()
            
            transport = st.selectbox("Choose transport", self.config['TRAVEL_MODE'])
            
            address_from = st.text_input("Go from", key="go_from")
            address_to = st.text_input("Go to", key="go_to")
    
            st.markdown("<h3 style='text-align: center;'>Tolerance</h3>", unsafe_allow_html=True)
            tolerance = st.slider('Select tolerance for elevation', min_value = 1.0, max_value = 5.0)
            st.write("Shows path upto "+ str(tolerance) +" times the shortest path")
            
            col1, col2 = st.columns([1,1])
            with col1:
                st.button("Clear Choice", on_click=clear_text)
            with col2:
                st.button("Get Directions", on_click=get_directions)
        
        lat, lon = 42.4529, -72.5653
        m = leafmap.Map(center=(lat, lon), zoom=16)
        m.add_basemap(basemap)
        m.to_streamlit()
        
    def get_directions(self):
        #if (address_from != address_to):
        pass