import geopandas as gpd
import pandas as pd

gdf_2015 = gpd.read_file('35117_2015.geojson')
gdf_2019 = gpd.read_file('35117_2019.geojson')

# Reproject to UTM Zone 17N
gdf_2015 = gdf_2015.to_crs(epsg=32617)
gdf_2019 = gdf_2019.to_crs(epsg=32617)

matches = []

for idx_2015, row_2015 in gdf_2015.iterrows():
    for idx_2019, row_2019 in gdf_2019.iterrows():
        # Calculate intersection area
        intersection = row_2015['geometry'].intersection(row_2019['geometry'])
        # Calculate overlap ratio (intersection area / 2015 PD area)
        if intersection.area > 0:
            overlap_ratio = intersection.area / row_2015['geometry'].area
            # If overlap ratio > 99%, consider them a match
            if overlap_ratio > 0.99:
                matches.append({
                    'poll_2015': row_2015['PD_NUM'],
                    'poll_2019': row_2019['PD_NUM']
                })

# Create DataFrame and save to CSV
concordance_df = pd.DataFrame(matches)
concordance_df.to_csv('pd_concordance.csv', index=False)