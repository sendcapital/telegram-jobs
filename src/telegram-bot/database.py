from google.cloud import bigquery
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv() 

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'

TABLE_ID = os.getenv("TABLE_ID")

def init_client():
  client = bigquery.Client()
  schema = client.schema_from_json('schema.json')
  table = bigquery.Table(TABLE_ID, schema = schema)
  print(
      "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
  )
  return client

def load_data(client, table, jobs_df):
  errors = client.insert_rows_from_dataframe(table, jobs_df)
  if errors == []:
      print("Data loaded into table")
  else:
      print(errors)

def build_query(column: str, table: str):
  query = f'SELECT {column} FROM `{table}`'
  return query

def run_query(client, query):
  query_job = client.query(query)
  result = query_job.result()
  return result  

def fetch_all(client): 
  FETCH_ALL_QUERY = build_query("*", "linkedin-profile-392109.linkedin_jobs.jobs")
  df = client.query(FETCH_ALL_QUERY).to_dataframe()
  return df
  