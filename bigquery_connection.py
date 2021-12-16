from google.cloud import bigquery
from google.oauth2 import service_account

def get_bigquery_client(project_id, credentials_file):
    credentials = service_account.Credentials.from_service_account_file(credentials_file)    
    return bigquery.Client(credentials=credentials, project=project_id)

def get_data_as_dataframe(client, query):
    try:
        job = client.query(query)
        results = job.result()
        data = results.to_dataframe()
        return data
    
    except Exception as e:
        print(str(e))
        return None