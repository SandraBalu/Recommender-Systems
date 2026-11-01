import os
import math
import time
import pandas as pd
from dotenv import load_dotenv
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import SetItemValues, Batch
from recombee_api_client.exceptions import APIException

# Credentialele se citesc din fisierul .env
load_dotenv()
DB_NAME = os.getenv('RECOMBEE_DB_NAME')
PRIVATE_TOKEN = os.getenv('RECOMBEE_PRIVATE_TOKEN')
REGION = Region.EU_WEST

client = RecombeeClient(DB_NAME, PRIVATE_TOKEN, region=REGION)

# Dataset-ul de filme folosit la Lab 02
PATH_DATASET = '../lab02/movies.csv'

def safe_int(value):
    """Converteste valoarea la int, returnand None daca e NaN"""
    try:
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return None
        return int(value)
    except (ValueError, TypeError):
        return None

def safe_float(value):
    """Converteste valoarea la float, returnand None daca e NaN"""
    try:
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return None
        return float(value)
    except (ValueError, TypeError):
        return None

def safe_str(value):
    """Converteste valoarea la string, returnand None daca e NaN"""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    return str(value)

def send_batch(requests, retries=3):
    """Trimite un batch cu retry automat la erori temporare (502, 503)"""
    for attempt in range(retries):
        try:
            client.send(Batch(requests))
            return
        except Exception as e:
            if attempt < retries - 1:
                print(f"  Eroare temporara ({e}), reincercare in 3s...")
                time.sleep(3)
            else:
                raise

def send_items():
    """Citeste dataset-ul si trimite item-urile in Recombee folosind Batch"""
    df = pd.read_csv(PATH_DATASET)
    print(f"Se trimit {len(df)} item-uri in Recombee (baza de date: '{DB_NAME}')...")

    requests = []
    trimise = 0

    for index, row in df.iterrows():
        # ID-ul unic al filmului: folosim indexul randului ca string
        item_id = str(index)

        # Maparea proprietatilor definite in Lab 02
        properties = {}
        if safe_str(row['genre'])    is not None: properties['genre']    = safe_str(row['genre'])
        if safe_int(row['year'])     is not None: properties['year']     = safe_int(row['year'])
        if safe_float(row['score'])  is not None: properties['score']    = safe_float(row['score'])
        if safe_str(row['director']) is not None: properties['director'] = safe_str(row['director'])
        if safe_str(row['rating'])   is not None: properties['rating']   = safe_str(row['rating'])
        if safe_int(row['runtime'])  is not None: properties['runtime']  = safe_int(row['runtime'])

        # SetItemValues creaza automat item-ul daca nu exista (cascade_create=True)
        requests.append(SetItemValues(item_id, properties, cascade_create=True))

        # Trimitem in loturi de cate 100 pentru eficienta
        if len(requests) == 100:
            send_batch(requests)
            trimise += len(requests)
            requests = []
            print(f"  Trimise pana acum: {trimise}/{len(df)}")

    # Trimitem restul ramas (daca numarul total nu e multiplu de 100)
    if requests:
        send_batch(requests)
        trimise += len(requests)

    print(f"\nToate cele {trimise} item-uri au fost trimise cu succes in Recombee!")

if __name__ == "__main__":
    send_items()
