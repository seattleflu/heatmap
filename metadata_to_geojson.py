import argparse
import pandas as pd
import geojson
import random
import string

def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_sample_to_metadata(metadata_file):
    '''
    Return dict of sample barcode to dict of
    {"residence_census_tract", "age_category", "site_category"}
    '''
    mapping = {}
    entries = pd.read_csv(metadata_file, sep='\t')
    for index, row in entries.iterrows():
        if str(row['strain']) != 'nan':
            sample = str(row['strain'])
        if str(row['residence_census_tract']) != 'nan':
            census_tract = str(int(row['residence_census_tract']))
        if str(row['age_category']) != 'nan':
            age_category = str(row['age_category'])
        if str(row['site_category']) != 'nan':
            site_category = str(row['site_category'])
        if str(row['residence_census_tract']) != 'nan' and str(row['site_category']) != 'nan' and str(row['site_category']) != 'nan':
            mapping[sample] = {
                'census_tract': census_tract,
                'age_category': age_category,
                'site_category': site_category
            }
    return mapping

def get_census_tract_to_lat_long(lat_longs_file):
    '''
    Return dict of census tract id to dict of {"lat", "long"}
    '''
    mapping = {}
    entries = pd.read_csv(lat_longs_file, sep='\t')
    for index, row in entries.iterrows():
        if str(row['census_tract']) != 'nan':
            census_tract = str(int(row['census_tract']))
        if str(row['lat']) != 'nan':
            lat = float(row['lat'])
        if str(row['long']) != 'nan':
            long = float(row['long'])
        mapping[census_tract] = {
            'lat': lat,
            'long': long
        }
    return mapping

def get_feature_collection(sample_to_metadata, census_tract_to_lat_long, site_categories, age_categories):
    features = []
    for sample, metadata in sample_to_metadata.items():
        if metadata['census_tract'] in census_tract_to_lat_long:
            if metadata['site_category'] in site_categories and metadata['age_category'] in age_categories:
                lat = census_tract_to_lat_long[metadata['census_tract']]['lat']
                long = census_tract_to_lat_long[metadata['census_tract']]['long']
                sample_feature = geojson.Feature(geometry=geojson.Point((long, lat)), properties={"id": id_generator()})
                features.append(sample_feature)
        else:
            print("missing lat/long for", sample)
    return geojson.FeatureCollection(features)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Export GeoJSON from metadata TSV",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('--metadata', type=str, required=True, help="Seattle metadata file as used by augur (not to be committed)")
    parser.add_argument('--lat-longs', type=str, required=True, help="census tract to lat long mapping file")
    parser.add_argument('--site-categories', nargs='+', type=str, default=['hospital', 'community'], help="site categories to include")
    parser.add_argument('--age-categories', nargs='+', type=str, default=['adult', 'child'], help="age categories to include")
    parser.add_argument('--output', type=str, help="output GeoJSON file")
    args = parser.parse_args()

    sample_to_metadata = get_sample_to_metadata(args.metadata)
    census_tract_to_lat_long = get_census_tract_to_lat_long(args.lat_longs)

    feature_collection = get_feature_collection(sample_to_metadata, census_tract_to_lat_long, args.site_categories, args.age_categories)
    with open(args.output, 'w', encoding='utf-8') as outfile:
        geojson.dump(feature_collection, outfile, indent=1)
