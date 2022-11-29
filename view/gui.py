import streamlit as st
import folium
import osmnx
import networkx as nx
import leafmap.foliumap as leafmap
import json



width = data['width']
height = data['height']
print(width)
print(height)

class gui:
    def __init__(self):
        filename = '../config.json'
        
        with open(filename) as config_file:
            data = json.load(config_file)
        
        self.basemaps = data['BASEMAPS']
        self.travel_mode = data['TRAVEL_MODE']
        self.address_default = data['ADDRESS_DEFAULT']

