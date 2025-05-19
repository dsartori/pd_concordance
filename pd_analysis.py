import geopandas as gpd
import pandas as pd

gdf_2015 = gpd.read_file('35117_2015.geojson')
gdf_2021 = gpd.read_file('35117_2021.geojson')

# Reproject to UTM Zone 17N 
gdf_2015 = gdf_2015.to_crs(epsg=32617)
gdf_2021 = gdf_2021.to_crs(epsg=32617)

results = []

# Analyze overlaps
for idx_2015, row_2015 in gdf_2015.iterrows():
    for idx_2021, row_2021 in gdf_2021.iterrows():
        # Calculate intersection 
        intersection = row_2015.geometry.intersection(row_2021.geometry)
        if not intersection.is_empty:
            # Calculate overlap  
            overlap_percentage = (intersection.area / row_2015.geometry.area) * 100
            
            # Only include overlaps > 1%
            if overlap_percentage > 1:
                if overlap_percentage > 99:
                    overlap_percentage = 100.0
                results.append({
                    'poll_2015': row_2015['PD_NUM'],
                    'poll_2021': row_2021['PD_NUM'],
                    'overlap_percentage': round(overlap_percentage, 2)
                })

results_df = pd.DataFrame(results)
results_df.to_csv('pd_overlap.csv', index=False)