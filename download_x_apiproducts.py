
import os
from re import A
import requests
import json
from dotenv import load_dotenv
from pathlib import Path
from ApigeeAuth import ApigeeAuth

load_dotenv()

def get_api_products(target_organisation, expand=False):
    """
    Example:
    {
    "apiProduct": [
            {
                "name": "Ecommerce Newsletter"
            },
            {
                "name": "Ecommerce i18n"
            },
            {
                "name": "Flagsmith API"
            },
            {
                "name": "Ecommerce Appbackend Conrad CH"
            }
        ]
    }
    """
    print("\n[REQUESTS] Getting api products in: " + target_organisation)
    url = os.environ['APIGEE_X_API_BASE_URL'] + '/v1/organizations/' + target_organisation + '/apiproducts'
    params = {'expand': expand}
    response = requests.get(url, auth=ApigeeAuth(), params=params)
    with open("all_apiproducts.txt", 'w') as apiroducts:
        apiroducts.write(response.text)
# get_api_products('apigee-x-nonprod', expand=False)

def download_apiproducts(target_organisation):
    print("\n[REQUESTS] Fetching API Products from file...")
    with open('all_apiproducts.txt', 'r') as all_apiproducts_file:
        all_apiproducts= json.load(all_apiproducts_file)
        count=0
        for apiproduct in all_apiproducts['apiProduct']:
            apiproduct_name=apiproduct['name']
            print(f"\n[REQUESTS] Fetching API Product details for {apiproduct_name}...")
            url = os.environ['APIGEE_X_API_BASE_URL'] + '/v1/organizations/' + target_organisation+ '/apiproducts/'+f"{apiproduct_name}"
            response = requests.get(url, auth=ApigeeAuth())
            print(f"\n[DONE]")
            print(f"\n[FILE] Writing API Product details {apiproduct_name} to file...")
            path = f'ApigeeDownloads'+"/apigee-x-apiproducts/"
            print(f"\n[PATH CREATED] This API Product will be downloaded to {path}...")
            Path(path).mkdir(parents=True, exist_ok=True)
            target_path = path+'/'+apiproduct_name+".json"
            print(f"\n[REQUESTS] Downloading {apiproduct_name} for {target_organisation}  ...")
            with open(target_path, "wb") as handle:
                for chunk in response.iter_content(chunk_size=512):
                    if chunk:  # filter out keep-alive new chunks
                        handle.write(chunk)
            print("*************************************************")
            count+=1
            print(f"\n[COUNT] API Product No: {count}")
            continue
        print(f"\n[DONE] All API Products have been downloaded to specified path")
download_apiproducts('apigee-x-nonprod')
