"""
Purpose: 
    This script takes Altmetric API and doi of an article,
    and return 1) detail metadata and metrics if set argument as "metadata"
     or        2) counts if argument set to be "counts"
    The result would be saved in json file

Author: 
    Wanying Zhao

"""

import requests
import pandas as pd
import json
import sys
import gzip
import time

DOI_PATH = sys.argv[1]
OUTPUT_PATH = sys.argv[2]
DATA_TYPE = sys.argv[3]


HOST = "http://api.altmetric.com/"
API_KEY = "fe611223be9b4f171b9d9edbfc26b749"


def read_doi(file_path = DOI_PATH):
    """
        This function read a csv file under path DOI_PATH
        and return a list of doi 
    """
    doi_df = pd.read_csv(file_path, sep = '\t').dropna()
    print(f"{len(doi_df)} dois need to be collected")
    return list(doi_df["doi"])


def fetch_data(doi, api_version = "v1/fetch/"):
    """
        This function take one doi and api type, which could be 
        "fetch/" by default or "v1/", then generate 
        correponding url for retriveing its metadata
    """
    
    base_url = HOST + api_version
    api_key = f"?key={API_KEY}"

    url =  base_url + f"doi/{doi}" + api_key

    try: 
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
            if response.status_code == 404 and response.reason == 'Not Found':
                return None
            raise HTTPException(response.status_code, response.reason)

        

if __name__ == "__main__":
    dois = read_doi()
    
    with gzip.open(OUTPUT_PATH, "wb") as f:
        for idx, doi in enumerate(dois):
            record = fetch_data(doi.lower(), api_version = DATA_TYPE)
            record_in_bytes = f"{json.dumps(record)}\n".encode(encoding="utf-8")
            f.write(record_in_bytes)
            if idx%500 == 0:
                
                print(f"...{idx} records collected....")
                time.sleep(4)


    





