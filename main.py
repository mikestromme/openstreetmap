import overpy
import folium

def data_mine_osm_data(bbox):
    api = overpy.Overpass()
    query = f'''
    (
      node["building"]({bbox});
      way["building"]({bbox});
      relation["building"]({bbox});
    );
    (._;>;);
    out;
    '''
    response = api.query(query)
    
    # Process the response
    buildings = []
    for result in response.nodes + response.ways:
        if isinstance(result, overpy.Node):
            lat = result.lat
            lon = result.lon
            buildings.append((lat, lon))
        elif isinstance(result, overpy.Way):
            for node in result.nodes:
                lat = node.lat
                lon = node.lon
                buildings.append((lat, lon))
    
    return buildings

# Example usage
bbox = "51.5074, -0.1278, 51.5174, -0.1178"  # London bounding box as a string
results = data_mine_osm_data(bbox)

# Create a folium map centered on the first coordinate
map_center = results[0]
m = folium.Map(location=map_center, zoom_start=15)

# Add markers for each coordinate
for lat, lon in results:
    folium.Marker(location=[lat, lon]).add_to(m)

# Display the map
m.save("map.html")  # Save the map as an HTML file
