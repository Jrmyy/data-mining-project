# std
import json

# 3rd
import pandas as pd
import requests


def get_longitude_latitude(address):
    print('Finding geo for {}'.format(address))
    try:
        r = requests.get(
            'http://www.datasciencetoolkit.org/maps/api/geocode/json?'
            'sensor=false&address={}'.format(
                address
            )
        )
        geo = json.loads(r.text)['results'][0]['geometry']['location']
        print('Found geoloc {} for {}'.format(geo, address))
        return pd.Series(geo)
    except Exception:
        return pd.Series({'lat': '', 'lng': ''})


def fetch_geo():
    # We load the data
    df = pd.read_csv('data/apartments.csv')

    # We create a dataframe with the full address
    addresses_df = df['street_address'].drop_duplicates() \
        .to_frame('street_address')
    addresses_df['full_address'] = (
        df['street_address'].astype(str) + ' ' +
        df['postal_code'].astype(str) + ' ' +
        df['address_locality'].astype(str)
    ).drop_duplicates()

    # We create a dataframe with 2 new columns, by merging with the series
    # returned by the lambda functio
    addresses_df = addresses_df.merge(addresses_df.apply(
        lambda s: get_longitude_latitude(s['full_address']), axis=1
    ), left_index=True, right_index=True)

    # And then we saved, so that we don't have problems (API Limit issue)
    addresses_df.to_csv('data/geo-loc-addresses.csv', index=None)


def merge_geo():
    df = pd.read_csv('data/apartments.csv')
    addresses_df = pd.read_csv('data/geo-loc-addresses.csv')
    final_df = pd.merge(df, addresses_df, how='left', on='street_address')
    final_df = final_df.drop(['Unnamed: 0'], axis=1)
    final_df.to_csv('data/apartments-geo.csv', index=None)


if __name__ == '__main__':
    fetch_geo()
    merge_geo()
