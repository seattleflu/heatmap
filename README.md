Download metadata from IDC as `seattle_metadata.tsv`:
```
python download_sfs_metadata.py
```

Produce GeoJSON from this metadata as `samples.geojson`:
```
python metadata_to_geojson.py --metadata seattle_metadata.tsv --lat-longs lat_longs.tsv --output samples.geojson

python metadata_to_geojson.py --metadata seattle_metadata.tsv --lat-longs lat_longs.tsv --site-categories community --output samples_community.geojson

python metadata_to_geojson.py --metadata seattle_metadata.tsv --lat-longs lat_longs.tsv --site-categories clinical --output samples_clinical.geojson
```

Then open `heatmap.html` in a browser with cross-origin allowed, ie:
```
open -a Google\ Chrome --args --disable-web-security --allow-file-access-from-files
```
