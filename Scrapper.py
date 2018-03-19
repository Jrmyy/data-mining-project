from bs4 import BeautifulSoup
import requests
import ast
import pandas as pd

def create_url_db():

    BASE_URL = 'https://www.apartments.com/ca/'
    url_list = []
    for i in range(1, 28 + 1):
        url = BASE_URL + str(i) + '/'
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
        apartments = soup.findAll('a', class_="placardTitle js-placardTitle ")
        for element in apartments:

            link = element.attrs['href']
            if link != 'false':
                url_list += [link]
        f = open("./url-list2.txt", "w")
        f.write(str(url_list))
        f.close()

def create_dict_housing():

    f = open('./url-list.txt', 'r')
    file = f.read()
    url_list = ast.literal_eval(file)
    dict_apt = {}
    ap_id = 0
    no_rent = []
    for link in url_list:
        req = requests.get(link)
        soup = BeautifulSoup(req.text, "html.parser")
        xml =str(BeautifulSoup(req.text, "xml"))
        apartments = soup.findAll('tr', class_='rentalGridRow')
        address = soup.find('h2', itemprop='address')
        street_address = address.findChild('span', itemprop='streetAddress').contents[0]
        address_locality = address.findChild('span', itemprop='addressLocality').contents[0]
        postal_code = address.findChild('span', itemprop='postalCode').contents[0]
        if '<h3>Features</h3>' in xml:
            list_features = xml.split('<h3>Features</h3>')[1].split('</div>')[0].split('"bullet"/>')[1:]
            features = []
            for feat in list_features:
                features += [feat.split('</li>')[0]]
        else:
            features = []
        if soup.find('div', class_='parkingDetails') != None:
            park = []
            parkings = soup.findAll('div', class_='parkingDetails')
            for elem in parkings:
                parkk = elem.findChildren('h4')
                for ele in parkk:
                    if 'Garage' in ele.contents[0]:
                        park += ['Garage']
                    if 'Surface Lot and Covered' in ele.contents[0]:
                        park += ['Surface Lot and Covered']
                    if 'Surface Lot' in ele.contents[0] and 'Surface Lot and Covered' not in park:
                        park += ['Surface Lot']
                    if 'Covered' in ele.contents[0] and 'Surface Lot and Covered' not in park:
                        park += ['Covered']
        for ap in apartments:
            ap_id += 1
            dict_apt[ap_id] = {}
            dict_apt[ap_id]['features'] = features
            dict_apt[ap_id]['street_address'] = street_address
            dict_apt[ap_id]['postal_code'] = postal_code
            dict_apt[ap_id]['address_locality'] = address_locality
            if ap.attrs['data-baths'] != '':
                dict_apt[ap_id]['baths'] = float(ap.attrs['data-baths'])
            else:
                dict_apt[ap_id]['baths'] = 0
            dict_apt[ap_id]['beds'] = int(ap.attrs['data-beds'])
            dict_apt[ap_id]['parking'] = park
            rent = ap.attrs['data-maxrent']
            if rent != '':
                dict_apt[ap_id]['rent'] = float(rent)
            else:
                dict_apt[ap_id]['rent'] = 0
            dict_apt[ap_id]['model'] = ap.attrs['data-model']
            sqrft = ap.findChild('td', class_='sqft')
            print(sqrft, link)
            if sqrft.contents != []:
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

        f = open("./Data2.txt", "w")
        f.write(str(dict_apt))
        f.close()
        #print(len(dict_apt))
    #print(dict_apt)

def create_dataframe():

    f = open('./Data2.txt', 'r')
    file = f.read()
    housing_dict = ast.literal_eval(file)
    df = pd.DataFrame.from_dict(housing_dict)
    df = df.transpose()
    df.to_csv('Apartments.csv')



#TODO: les mettre dans un dataframe et sauvegarder dans un csv


create_url_db()
#create_dict_housing()
#create_dataframe()
