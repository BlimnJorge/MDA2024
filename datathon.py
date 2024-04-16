#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import os
import unicodedata
import geopandas as gpd
import matplotlib.pyplot as plt
import googlemaps


# In[3]:


file_path = os.path.expanduser('~/Documents/Datathon files/aed_locations.xlsx')
aed_df = pd.read_excel(file_path)

cad9_df = pd.read_excel(os.path.expanduser('~/Documents/Datathon files/cad9.xlsx'))
ambulance_df = pd.read_excel(os.path.expanduser('~/Documents/Datathon files/ambulance_locations.xlsx'))
interventionsbxl1_df = pd.read_excel(os.path.expanduser('~/Documents/Datathon files/interventions_bxl.xlsx'))
interventionsbxl2_df = pd.read_excel(os.path.expanduser('~/Documents/Datathon files/interventions_bxl2.xlsx'))
interventions1_df = pd.read_excel(os.path.expanduser('~/Documents/Datathon files/interventions1.xlsx'))
interventions2_df = pd.read_excel(os.path.expanduser('~/Documents/Datathon files/interventions2.xlsx'))
interventions3_df = pd.read_excel(os.path.expanduser('~/Documents/Datathon files/interventions3.xlsx'))
mug_df = pd.read_excel(os.path.expanduser('~/Documents/Datathon files/mug_locations.xlsx'))
pit_df = pd.read_excel(os.path.expanduser('~/Documents/Datathon files/pit_locations.xlsx'))


# In[4]:


aed_df['type'] = aed_df['type'].str.lower()
aed_df['address'] = aed_df['address'].str.lower()
aed_df['municipality'] = aed_df['municipality'].str.lower()
aed_df['province'] = aed_df['province'].str.lower()


# In[5]:


aed_df = aed_df.fillna('unknown')

aed_df = aed_df.drop_duplicates()


# In[6]:


aed_df['address'] = aed_df['address'].apply(lambda val: unicodedata.normalize('NFKD', val).encode('ascii', 'ignore').decode())
aed_df['municipality'] = aed_df['municipality'].apply(lambda val: unicodedata.normalize('NFKD', val).encode('ascii', 'ignore').decode())
aed_df['province'] = aed_df['province'].apply(lambda val: unicodedata.normalize('NFKD', val).encode('ascii', 'ignore').decode())


# In[7]:


aed_df['location_aed'] = aed_df['address'] + ',' + aed_df['postal_code'].astype(str) + ',' + aed_df['municipality'] + ',' + 'Belgium'


# In[8]:


aed_df.drop(columns=['type', 'location', 'public', 'available', 'hours', 'number', 'postal_code', 'municipality', 'address'], inplace=True)


# In[9]:


gmaps = googlemaps.Client(key='AIzaSyBMtPkh3SeIaxEse9bN6cQSLKp_FwU0p5M')


# In[10]:


def geocode_address(address):
    result = gmaps.geocode(address)
    if result:
        location = result[0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        return None, None


# In[11]:


aed_df['latitude'], aed_df['longitude'] = zip(*aed_df['location_aed'].apply(geocode_address))


# In[12]:


aed_df


# In[13]:


world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
belgium = world[world.name == 'Belgium']


# In[14]:


gdf = gpd.GeoDataFrame(aed_df, geometry=gpd.points_from_xy(aed_df.longitude, aed_df.latitude))


# In[15]:


fig, ax = plt.subplots(figsize=(10, 8))
belgium.plot(ax=ax, color='lightgrey', edgecolor='black')
gdf.plot(ax=ax, color='red', marker='o', markersize=50, label='AED Locations')
    
plt.title('Automated External Defibrillator (AED) Locations in Belgium')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.grid(True)
plt.show()


# In[16]:


interventions_df = pd.concat([interventions1_df, interventions2_df, interventions3_df])


# In[17]:


filtered_cad9 = cad9_df[cad9_df['EventType Trip'].isin(['P003 - HARTSTILSTAND - DOOD - OVERLEDEN', 
                                             'P008 - PATIËNT MET DEFIBRILLATOR OF PACEMAKER', 
                                             'P039 - CARDIAAL PROBLEEM (NIET PIJN OP DE BORST)'])]

filtered_interventions = interventions_df[interventions_df['EventType Trip'].isin(['P039 - Cardiac problem (other than thoracic pain)', 
                                                        'P003 - Cardiac arrest', 
                                                        'P008 - Patient with defibrillator - pacemaker'])]

filtered_interventions_bxl1 = interventionsbxl1_df[interventionsbxl1_df['eventtype_trip'].isin(['P039 - Cardiac problem (other than thoracic pain)',
                                                                                         'P003 - Cardiac arrest', 
                                                                                         'P008 - Patient with defibrillator - pacemaker'])]

temp = interventionsbxl2_df['EventType and EventLevel'].str.extract(r'(.*)(N[0-9]{2})(.*)')
interventionsbxl2_df['EventType'] = temp[0].str.strip() + temp[2]
interventionsbxl2_df['EventLevel'] = temp[1].str.strip()

filtered_interventions_bxl2 = interventionsbxl2_df[interventionsbxl2_df['EventType'].isin(['P003 - HARTSTILSTAND - DOOD - OVERLEDEN', 
                                                                                       'P008 - PATIËNT MET DEFIBRILLATOR OF PACEMAKER', 
                                                                                       'P039 - CARDIAAL PROBLEEM (NIET PIJN OP DE BORST)'])]


# In[18]:


import geopandas as gpd
from shapely.geometry import Point


# In[19]:


#filtered_interventions_bxl1['latitude_intervention'] = filtered_interventions_bxl1['latitude_intervention'].str.replace(',', '.').astype(float)
#filtered_interventions_bxl1['longitude_intervention'] = filtered_interventions_bxl1['longitude_intervention'].str.replace(',', '.').astype(float)


# In[20]:


# filtered_interventions_bxl1['latitude_intervention'] = filtered_interventions_bxl1['latitude_intervention'].astype(int).astype(str).str[:2] + '.' + filtered_interventions_bxl1['latitude_intervention'].astype(int).astype(str).str[2:]
# filtered_interventions_bxl1['longitude_intervention'] = filtered_interventions_bxl1['longitude_intervention'].astype(int).astype(str).str[:1] + '.' + filtered_interventions_bxl1['longitude_intervention'].astype(int).astype(str).str[1:]

#filtered_interventions_bxl1['latitude_intervention'] = filtered_interventions_bxl1['latitude_intervention'].astype(float)
#filtered_interventions_bxl1['longitude_intervention'] = filtered_interventions_bxl1['longitude_intervention'].astype(float)


# In[21]:


#filtered_interventions_bxl2['Latitude intervention'] = filtered_interventions_bxl2['Latitude intervention'].astype(int).astype(str).str[:2] + ',' + filtered_interventions_bxl2['Latitude intervention'].astype(int).astype(str).str[2:]
#filtered_interventions_bxl2['Longitude intervention'] = filtered_interventions_bxl2['Longitude intervention'].astype(int).astype(str).str[:1] + ',' + filtered_interventions_bxl2['Longitude intervention'].astype(int).astype(str).str[1:]
#filtered_interventions_bxl2['Latitude intervention'] = filtered_interventions_bxl2['Latitude intervention'].str.replace(',', '.').astype(float)
#filtered_interventions_bxl2['Longitude intervention'] = filtered_interventions_bxl2['Longitude intervention'].str.replace(',', '.').astype(float)


# In[22]:


interventions_lat_long = filtered_interventions[['Latitude intervention', 'Longitude intervention']]
interventionsbxl1_lat_long = filtered_interventions_bxl1[['latitude_intervention', 'longitude_intervention']]
interventionsbxl2_lat_long = filtered_interventions_bxl2[['Latitude intervention', 'Longitude intervention']]
cad9_lat_long = filtered_cad9[['Latitude intervention', 'Longitude intervention']]


# In[23]:


lat_long_df = [
    interventions_lat_long.rename(columns={'Latitude intervention': 'latitude', 'Longitude intervention': 'longitude'}),
    interventionsbxl1_lat_long.rename(columns={'latitude_intervention': 'latitude', 'longitude_intervention': 'longitude'}),
    interventionsbxl2_lat_long.rename(columns={'Latitude intervention': 'latitude', 'Longitude intervention': 'longitude'}),
    cad9_lat_long.rename(columns={'Latitude intervention': 'latitude', 'Longitude intervention': 'longitude'})
]


# In[24]:


combined_int_lat_long = pd.concat(lat_long_df, ignore_index=True)


# In[25]:


combined_int_lat_long = combined_int_lat_long.dropna()
combined_int_lat_long


# In[26]:


from sklearn.cluster import DBSCAN
import numpy as np


# In[27]:


cardiac_arrests_gdf = gpd.GeoDataFrame(
    combined_int_lat_long,
    geometry=gpd.points_from_xy(combined_int_lat_long.longitude, combined_int_lat_long.latitude)
)


# In[28]:


coords = np.radians(cardiac_arrests_gdf[['latitude', 'longitude']].values)
kms_per_radian = 6371.0088
epsilon = 0.1 / kms_per_radian


# In[29]:


db = DBSCAN(eps=epsilon, min_samples=5, algorithm='ball_tree', metric='haversine').fit(coords)
cluster_labels = db.labels_


# In[30]:


cardiac_arrests_gdf['cluster'] = cluster_labels


# In[31]:


cluster_centroids = cardiac_arrests_gdf.groupby('cluster').apply(lambda x: x.unary_union.centroid if x.unary_union else None)


# In[32]:


from shapely.ops import nearest_points
from geopandas import GeoSeries


# In[33]:


proposed_aed_locations = GeoSeries(cluster_centroids, crs='EPSG:4326')


# In[34]:


def distance_to_nearest_aed(proposed_location, existing_aeds):
    nearest_aed_point = nearest_points(proposed_location, existing_aeds.unary_union)[1]
    return proposed_location.distance(nearest_aed_point)


# In[35]:


aed_gdf = gdf

distances_to_nearest_aed = proposed_aed_locations.apply(lambda x: distance_to_nearest_aed(x, aed_gdf.geometry))


# In[36]:


proposed_aed_locations_df = proposed_aed_locations.to_frame(name='geometry')
proposed_aed_locations_df['distance_to_nearest_aed_km'] = distances_to_nearest_aed * 100


# In[37]:


min_distance_threshold = 0.1


# In[38]:


adequate_coverage_df = proposed_aed_locations_df[proposed_aed_locations_df['distance_to_nearest_aed_km'] > min_distance_threshold]


# In[39]:


import folium

m = folium.Map(location=[50.8503, 4.3517], zoom_start=8)


# In[40]:


aed_gdf = aed_gdf.dropna(subset=['latitude', 'longitude'])
cardiac_arrests_gdf = cardiac_arrests_gdf.dropna(subset=['latitude', 'longitude'])
adequate_coverage_df = adequate_coverage_df.dropna(subset=['geometry'])


# In[41]:


#for idx, row in aed_gdf.iterrows():
    #folium.Marker([row['latitude'], row['longitude']], icon=folium.Icon(color="red")).add_to(m)


# In[42]:


#for idx, row in cardiac_arrests_gdf.iterrows():
    #folium.CircleMarker([row['latitude'], row['longitude']], radius=3, color="blue", fill=True).add_to(m)


# In[43]:


for idx, row in adequate_coverage_df.iterrows():
    folium.Marker([row['geometry'].y, row['geometry'].x], icon=folium.Icon(color="green")).add_to(m)


# In[44]:


adequate_coverage_df


# In[45]:


proposed_aed_locations_df


# In[46]:


cost_per_aed = 1500  
installation_cost_per_aed = 250  
annual_maintenance_cost_per_aed = 75

total_cost_first_year = (cost_per_aed + installation_cost_per_aed + annual_maintenance_cost_per_aed) * len(adequate_coverage_df)

print(f'Total cost for the first year: {total_cost_first_year}')


# In[47]:


m


# In[49]:


new_aed_df = pd.DataFrame({
    'longitude': adequate_coverage_df.geometry.x,
    'latitude': adequate_coverage_df.geometry.y
})

new_aed_df.to_excel(os.path.expanduser('~/Documents/new_aed_locations.xlsx'), index=False)


# In[ ]:




