import folium
from folium import plugins
import pandas as pd
import os
import json
from IPython.display import display
import pickle


class navigator:
    def __init__(self, destination):
        self.geoResources = {}
        self.hospitalLocation =(49.49226339787344, 8.487303256988524)
        self.position = 'w'
        self.destination = destination

        for root, dirs, files in os.walk('HospitalNavigator/GeoResources'):  
            for file in files:
                self.geoResources[file.split('.')[0]] = root+'/'+file

    def changeDestination(self,newDestination):
        self.destination = newDestination
        self.redrawMap()

    def changeStartPoint(self, newStartPoint):
        
        #self.position = newStartPoint #does not work yet
        print(f'Selected Start: {newStartPoint}; Selected Target: {self.destination}')
        #self.redrawMap()
        

    def drawPathWay(self,hospitalMap):
      
      def switchPosition(coordinate):
        temp = coordinate[0]
        coordinate[0] = coordinate[1]
        coordinate[1] = temp
        return coordinate

      searchString = self.position + self.destination.split('Haus')[1]
      with open(self.geoResources[searchString]) as f:
           testWay = json.load(f)

      for feature in testWay['features']:
        path = feature['geometry']['coordinates']

      finalPath = list(map(switchPosition,path))
      folium.plugins.AntPath(finalPath).add_to(hospitalMap)

    def drawBuilding(self,hospitalMap):
        hauseOutline = self.geoResources[self.destination]
        folium.GeoJson(hauseOutline, name="geojson").add_to(hospitalMap)

    def redrawMap(self):
        #print(f'position {self.position}, destination {self.destination}')
        hospitalMap = folium.Map(location = self.hospitalLocation, width = "75%", zoom_start = 17)
        self.drawPathWay(hospitalMap)
        self.drawBuilding(hospitalMap)
        display(hospitalMap)

    def save_state(self, filename='navigator_state.pkl'):
        state = {
            'geoResources': self.geoResources,
            'hospitalLocation': self.hospitalLocation,
            'position': self.position,
            'destination': self.destination,
        }

        with open(filename, 'wb') as file:
            pickle.dump(state, file)

    def load_state(self, filename='navigator_state.pkl'):
        with open(filename, 'rb') as file:
            state = pickle.load(file)

        self.geoResources = state['geoResources']
        self.hospitalLocation = state['hospitalLocation']
        self.position = state['position']
        self.destination = state['destination']

        self.redrawMap()
