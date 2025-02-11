from airflow import DAG
from airflow.operators.python import PythonOperator 
from datetime import datetime
import pandas as pd
import os
from dotenv import load_dotenv
import re



PATH_AUTO_CSV  = '/opt/airflow/data/output/csv/auto.csv'
PATH_TRASNFORMED_DATA='/opt/airflow/data/outputTransfomed/processed_data.csv'

################################ Functions ################################
def fillcareName(x,y) :
    return x.upper() + '-' + y.upper()

def extractPrice(text):
    cleaned_text = re.sub(r'[^\d]', '', text)  
    return int(cleaned_text[:-1]) 

price_mapping = {
    "Très bon prix": 3,
    "Bon prix": 2,
    "Prix correct": 1,
    "Pas d'information": 0
}

def extract_kilometrage(text):
    return int(re.sub(r'[^\d]', '', text))
def extract_month(dates):
    dates_series = pd.Series(dates)
    dates_series = pd.to_datetime(dates_series, errors='coerce')
    months = dates_series.dt.month
    return months

def extract_year(dates):
    dates_series = pd.Series(dates)
    dates_series = pd.to_datetime(dates_series, errors='coerce')
    year = dates_series.dt.year
    return year
def extract_puissance(text):
    match = re.search(r'(\d{2,3})\s?kW', text)
    if match:
        return int(match.group(1))  # Convert to int
    return None

# Function to extract Transmission type (manual or automatic)
def extract_transmission(text):
    match = re.search(r'(Boîte .+?)\s(\d)', text)
    if match:
        return match.group(1)  # Return as string
    return None

def extract_cylindree(detail):
    # Extract the cubic centimeters value and remove any spaces or special characters
    match = re.search(r'(\d{1,3}(?:[ ,]\d{3})*)\s*cm³', detail)
    if match:
        # Convert to integer and remove any spaces within the number
        return int(match.group(1).replace(' ', '').replace(',', ''))
    return None

# Function to extract Vitesses (Number of gears)
def extract_vitesses(text):
    match = re.search(r'(\d)\s?(\d)', text)
    if match:
        return int(match.group(1))  # Convert to int
    return None

# Function to extract Cylindres (Number of cylinders)
def extract_weight(text):
    match = re.search(r'(\d+\s?\d+)\s?kg', text)
    if match:
        return int(match.group(1).replace('\u202f', '').replace(' ', ''))  # Remove special spaces and return as int
    return None
def extract_number_ch(text):
    match = re.search(r'\((\d+)\s*CH\)', text) 
    if match:
        return int(match.group(1))  
    return None

################################ END ################################

def extract_data() :
    data = pd.read_csv(PATH_AUTO_CSV)
    return data


def transform_data(**kwargs):
    ti = kwargs['ti']
    data2 = ti.xcom_pull(task_ids='extract_data')
    data2['fillcareName'] = data2.apply(lambda row : fillcareName(row['car_name'], row['carModele']), axis = 1)
    data2['Price'] = data2['CarPrice'].apply(extractPrice)
    data2['etatCategory'] = data2['Etat'].map(price_mapping)
    data2['Milieage'] = data2['Milieage'].apply(extract_kilometrage) 
    data2['Month'] = extract_month(data2['Annee'])
    data2['Year'] = extract_year(data2['Annee'])
    data2['PuissanceV2'] = data2['Options'].apply(extract_puissance)
    data2['TransmissionV2'] = data2['Options'].apply(extract_transmission)
    data2['CylindréeV2'] = data2['Options'].apply(extract_cylindree)
    data2['VitessesV2'] = data2['Options'].apply(extract_vitesses)
    data2['CylindresV2'] = data2['Options'].apply(extract_weight)
    data2['HorsePower'] = data2['CarPui'].apply(extract_number_ch)
    data2.drop(["car_name", "carModele", "CarPrice", "Annee", "CarPui", "Options", "link"], axis = 1, inplace=True)
    return data2

def load_data(**kwargs):
    ti = kwargs['ti']
    df_transformed = ti.xcom_pull(task_ids='transform_data')
    
    df_transformed.to_csv(PATH_TRASNFORMED_DATA, index=False)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 2, 9),
    'retries': 1,
}

dag = DAG(
    'ETL',
    default_args=default_args,
    description='Un exemple simple d\'ETL avec Pandas et Airflow',
    schedule_interval='@daily',
)


extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    provide_context=True,
    dag=dag,
)

extract_task >> transform_task >> load_task
















