from google.cloud import bigquery

PROJECT_ID = "tonal-justice-507110-s6"

client = bigquery.Client(project=PROJECT_ID)

query = """
SELECT 'BigQuery connection successful!' AS message
"""

query_job = client.query(query)

for row in query_job:
    print(row.message)