import requests
import gzip  
import os 
import timeit
import streamlit as st

@st.cache_data
def download_SQLiteDb():

    output_folder = "data" 
    output_file = os.path.join(output_folder, "latest.db")

    sqlite_URL = "https://storage.covid19datahub.io/latest.db.gz"  

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    headers = {
        "authority" : "storage.covid19datahub.io", 
        "path" : "/latest.db.gz",
        "scheme": "https"
    } 

    response = requests.get(url=sqlite_URL, headers=headers) 

    try:
        if response.status_code == 200:
            FINISHED = False
            
            while FINISHED is False:
                print("The file is being downloaded")
                unzipped_file = gzip.decompress(response.content)
                FINISHED = True 

            #Saving the file 
            with open(output_file, 'wb') as f:
                f.write(unzipped_file) 

            print("The file was downloaded and saved into the data folder")

        else:
            print("Unable to download the file")
    except BaseException as e:
        raise e
