# std
import ast

# 3rd
from bs4 import BeautifulSoup
import pandas as pd
import requests


MAX_PAGE = 28


def create_url_db():
    base_url = 'https://www.apartments.com/ca'
    url_list = []

    try:
        # We go until the MAX_PAGE
        for i in range(1, MAX_PAGE + 1):
            url = '{}/{}/'.format(base_url, str(i))
            req = requests.get(url)
            soup = BeautifulSoup(req.text, 'html.parser')
            # We find all the apartments
            apartments = soup.findAll(
                'a', class_='placardTitle js-placardTitle '
            )

            for element in apartments:
                link = element.attrs['href']
                # If there is a link we add it
                if link != 'false':
                    url_list.append(link)

    except Exception as e:
        print('An error occurred : {}. Now saving ...'.format(str(e)))
    except InterruptedError:
        print('Interruption, saving ...')
    finally:
        # We store all the urls, so we don't have to do it again
        with open('data/urls-repertory.txt', 'w') as f:
            f.write('\n'.join(url_list))
            f.close()


def create_dict_housing():
    dict_apt = {}
    ap_id = 0
    try:
        with open('data/url-list.txt', 'r') as f:
            links = f.readlines()
            # For each link
            for link in links:
                req = requests.get(link)
                soup = BeautifulSoup(req.text, 'html.parser')
                xml = str(BeautifulSoup(req.text, 'xml'))
                # We get the list of apartments (many apartments for one link)
                apartments = soup.findAll('tr', class_='rentalGridRow')
                # We get the address
                address = soup.find('h2', itemprop='address')
                # We get address specific info
                street_address = address.findChild(
                    'span', itemprop='streetAddress'
                ).contents[0]
                address_locality = address.findChild(
                    'span', itemprop='addressLocality'
                ).contents[0]
                postal_code = address.findChild(
                    'span', itemprop='postalCode'
                ).contents[0]
                # If we have features we add it
                if '<h3>Features</h3>' in xml:
                    list_features = xml.split('<h3>Features</h3>')[1].split(
                        '</div>'
                    )[0].split('"bullet"/>')[1:]
                    features = []
                    for feat in list_features:
                        features += [feat.split('</li>')[0]]
                else:
                    # Otherwise it is empty
                    features = []
                # We check the parking
                park = []
                if soup.find('div', class_='parkingDetails') is not None:
                    parkings = soup.findAll('div', class_='parkingDetails')
                    for elem in parkings:
                        parkk = elem.findChildren('h4')
                        for ele in parkk:
                            if 'Garage' in ele.contents[0]:
                                park += ['Garage']
                            if 'Surface Lot and Covered' in ele.contents[0]:
                                park += ['Surface Lot and Covered']
                            if 'Surface Lot' in ele.contents[0] \
                                    and 'Surface Lot and Covered' not in park:
                                park += ['Surface Lot']
                            if 'Covered' in ele.contents[0] \
                                    and 'Surface Lot and Covered' not in park:
                                park += ['Covered']
                # Finally for every apartment at the address, we add the info
                for ap in apartments:
                    ap_id += 1
                    dict_apt[ap_id] = {}
                    dict_apt[ap_id]['features'] = features
                    dict_apt[ap_id]['street_address'] = street_address
                    dict_apt[ap_id]['postal_code'] = postal_code
                    dict_apt[ap_id]['address_locality'] = address_locality
                    # We get the number of bathrooms
                    if ap.attrs['data-baths'] != '':
                        dict_apt[ap_id]['baths'] = float(
                            ap.attrs['data-baths']
                        )
                    else:
                        dict_apt[ap_id]['baths'] = 0
                    # We get the number of beds
                    dict_apt[ap_id]['beds'] = int(ap.attrs['data-beds'])
                    dict_apt[ap_id]['parking'] = park
                    rent = ap.attrs['data-maxrent']
                    # If no rent, we put 0
                    if rent != '':
                        dict_apt[ap_id]['rent'] = float(rent)
                    else:
                        dict_apt[ap_id]['rent'] = 0
                    dict_apt[ap_id]['model'] = ap.attrs['data-model']
                    # We add sqare feet
                    sqrft = ap.findChild('td', class_='sqft')
                    if sqrft.contents:
                        sqrft = sqrft.contents[0]
                        sqrft = sqrft.replace(',', '')
                        sqrft = sqrft.replace('Sq Ft', '')
                        if '-' in sqrft:
                            mini = int(sqrft.split('-')[0])
                            maxi = int(sqrft.split('-')[1])
                            dict_apt[ap_id]['size'] = (mini + maxi) / 2
                        else:
                            dict_apt[ap_id]['size'] = int(sqrft)
                    else:
                        dict_apt[ap_id]['size'] = 0
    except Exception as e:
        print('An error occurred : {}. Now saving ...'.format(str(e)))
    except InterruptedError:
        print('Interruption, saving ...')
    finally:
        with open("data/dict_housing.txt", "w") as out:
            out.write(str(dict_apt))


def find_features(housing_dict):
    features = []
    for el in housing_dict.keys():
        for feature in housing_dict[el]['features']:
            if feature not in features:
                features += [feature]
    return features


def create_dataframe_with_features():
    housing_dict = {}
    try:
        with open('data/dict_housing.txt', 'r') as f_in:
            file = f_in.read()
            housing_dict = ast.literal_eval(file)
            # We find the features
            features = find_features(housing_dict)
            parking = ['Surface Lot and Covered', 'Garage', 'Surface Lot',
                       'Covered']
            # We format it
            for ele in housing_dict.keys():
                for feature in features:
                    if feature in housing_dict[ele]['features']:
                        housing_dict[ele][feature] = 1
                    else:
                        housing_dict[ele][feature] = 0
                for gar in parking:
                    if gar in housing_dict[ele]['parking']:
                        housing_dict[ele][gar] = 1
                    else:
                        housing_dict[ele][gar] = 0
    except Exception as e:
        print('An error occurred : {}. Now saving ...'.format(str(e)))
    except InterruptedError:
        print('Interruption, saving ...')
    finally:
        df = pd.DataFrame.from_dict(housing_dict)
        df = df.transpose()
        df.to_csv('data/apartments.csv')


if __name__ == '__main__':
    create_url_db()
    create_dict_housing()
    create_dataframe_with_features()
