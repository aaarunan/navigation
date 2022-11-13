import folium
import webbrowser
import pandas as pd


class Map:
    def __init__(self, center, zoom_start):
        self.center = center
        self.zoom_start = zoom_start
        self.map = folium.Map(location = self.center, zoom_start = self.zoom_start)
    
    def showMap(self):
        #Create the map
        #Display the map
        self.map.save("map.html")
        webbrowser.open("map.html")
    
    def add_markers(self, nodes):
        for node in nodes:
            folium.Marker([node.lat, node.lon]).add_to(self.map)
    