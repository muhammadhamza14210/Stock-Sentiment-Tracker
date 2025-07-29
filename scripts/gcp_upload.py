import pandas as pd
from google.cloud import bigquery

def upload_csv_to_bigquery(csv_path, table_name, dataset_id="stock_dataset", project_id="stock-analysis-467310"):
    # Load CSV
    df = pd.read_csv(csv_path)

    # BigQuery client
    client = bigquery.Client(project=project_id)

    # Dataset reference
    dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
    try:
        client.get_dataset(dataset_ref)
    except Exception:
        print(f"Creating dataset: {dataset_id}")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        client.create_dataset(dataset)

    # Table reference
    table_ref = dataset_ref.table(table_name)
    
    # Job config with overwrite & autodetect
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,  # Overwrite
        autodetect=True,                                             
    )

    # Upload to BigQuery
    print(f"Uploading {csv_path} to {project_id}.{dataset_id}.{table_name}...")
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()

    print(f"Uploaded {len(df)} rows to {table_name}")