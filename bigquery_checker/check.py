
from google.cloud import bigquery
from utils.settings import settings
from utils.helper import get_current_week_dates

class BigQueryClient:
    def __init__(self):
        self.client = bigquery.Client()
        self.dataset_id = f"{settings.PROJECT_ID}.asteroids"
        self.table_id = f"{self.dataset_id}.neows_asteroids"
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        try:
            self.client.get_table(self.table_id)
            print(f"Table {self.table_id} already exists.")
        except Exception:
            print(f"Table {self.table_id} does not exist. Creating table...")
            schema = [
                bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
                bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("absolute_magnitude", "FLOAT", mode="NULLABLE"),
                bigquery.SchemaField("estimated_diameter_min_km", "FLOAT", mode="NULLABLE"),
                bigquery.SchemaField("estimated_diameter_max_km", "FLOAT", mode="NULLABLE"),
                bigquery.SchemaField("is_potentially_hazardous", "BOOLEAN", mode="NULLABLE"),
                bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
                bigquery.SchemaField("relative_velocity_km_per_sec", "FLOAT", mode="NULLABLE"),
                bigquery.SchemaField("miss_distance_km", "FLOAT", mode="NULLABLE"),
                bigquery.SchemaField("orbiting_body", "STRING", mode="NULLABLE"),
            ]
            table = bigquery.Table(self.table_id, schema=schema)
            table = self.client.create_table(table)
            print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")

    def get_missing_dates_from_bigquery(self):
        sql = f"""
            SELECT DISTINCT date
            FROM `{settings.PROJECT_ID}.asteroids.neows_asteroids`
            WHERE DATE(date) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
        """

        query_job = self.client.query(sql)
        results = query_job.result()

        bq_dates = {
            row.date
            for row in results
        }

        expected_dates = set(get_current_week_dates())

        missing_dates = sorted(expected_dates - bq_dates)
        return missing_dates
