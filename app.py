from flask import Flask, render_template, request
import folium
import os
import json
from folium import plugins

def switchPosition(coordinate):
    temp = coordinate[0]
    coordinate[0] = coordinate[1]
    coordinate[1] = temp
    return coordinate

app = Flask(__name__)

class Navigator:
    def __init__(self):
        self.geoResources = {}
        self.hospitalLocation = (49.49226339787344, 8.487303256988524)
        self.position = 'w'
        self.destination = 'Haus1'

        for root, dirs, files in os.walk('HospitalNavigator/GeoResources'):  
            for file in files:
                self.geoResources[file.split('.')[0]] = root+'/'+file

    def changeDestination(self, newDestination):
        self.destination = newDestination
        return self.get_map()

    def changeStartPoint(self, newStartPoint):
        self.position = newStartPoint
        return self.get_map()

    def switchPosition(position):
        return [position[1], position[0]]

    def drawPathWay(self, hospitalMap):
        searchString = self.position + self.destination.split('Haus')[1]
        with open(self.geoResources[searchString]) as f:
            testWay = json.load(f)

        for feature in testWay['features']:
            path = feature['geometry']['coordinates']

        finalPath = list(map(switchPosition, path))
        folium.plugins.AntPath(finalPath).add_to(hospitalMap)

    def drawBuilding(self, hospitalMap):
        hauseOutline = self.geoResources[self.destination]
        folium.GeoJson(hauseOutline, name="geojson").add_to(hospitalMap)

    def get_map(self):
        hospitalMap = folium.Map(location=self.hospitalLocation, width="75%", zoom_start=17)
        self.drawPathWay(hospitalMap)
        self.drawBuilding(hospitalMap)
        return hospitalMap._repr_html_()

myNavigator = Navigator()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        destination = request.form['destination']
        myNavigator.changeDestination(destination)

    return render_template('index.html', map_html=myNavigator.get_map())

if __name__ == '__main__':
    app.run(debug=True)
