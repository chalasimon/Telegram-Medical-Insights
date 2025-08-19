from dagster import op, job
@op
def scrape_telegram_data():
    # TODO: Add scraping logic
    pass

@op
def load_raw_to_postgres():
    # TODO: Add loading logic
    pass

@op
def run_dbt_transformations():
    # TODO: Add dbt run logic
    pass

@op
def run_yolo_enrichment():
    # TODO: Add YOLO enrichment logic
    pass

@job
def telegram_medical_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()