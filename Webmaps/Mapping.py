# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 22:27:48 2017

@author: KIRAN
"""

import folium
import pandas
data = pandas.read_csv("Volcanoes_USA.txt")

lat = list(data["LAT"])
lon = list(data["LON"])

elev = list(data["ELEV"])

def color_producer(elevation):
    if elevation < 1000:
        return  'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location=[38.58, -99.09], zoom_start= 6, tiles= "Mapbox Bright" )


fg = folium.FeatureGroup(name = "My Map")




for lt, ln, el in zip(lat, lon, elev):
#for coordinates in [[12.85, 77.80],[12.90, 77.58]]:
    #fg.add_child(folium.Marker(location = [lt, ln], popup = "Hi I am a Marker", icon = folium.Icon(color= 'blue')))
    #fg.add_child(folium.Marker(location = [lt, ln], popup = folium.Popup(str(el) + " m" , parse_html=True), icon = folium.Icon(color= color_producer())))
    fg.add_child(folium.CircleMarker(location = [lt, ln], radius = 6, popup = str(el) + " m" ,
    fill_color = color_producer(el), color = 'grey', fill= True, fill_opacity = 0.7))
    
                                     
                                     
    #fg.add_child(folium.Marker(location = [12.90, 77.58], popup = "Hi I am a Marker", icon = folium.Icon(color= 'blue')))


fg.add_child(folium.GeoJson(data= (open('world.json', 'r', encoding='utf-8-sig').read())))

map.add_child(fg)



#map.add_child(folium.Marker(location = [12.85, 77.80], popup = "Hi I am a Marker", icon = folium.Icon(color= 'blue')))


#map.save("Mapbg.html")
map.save("Mapbg2.html")
