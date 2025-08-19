from dagster import op, job
from dagster import ScheduleDefinition

@op
def scrape_telegram_data():
    from src.data_scrapper import TelegramScraper
    import asyncio

    # Example channels to scrape
    channels = [
            "@lobelia4cosmetics",
            "@tikvahpharma",
            "@yetenaweg",
            "@ethiopianfoodanddrugauthority",
            "@CheMed123",
            "@newoptics",
    ]

    scraper = TelegramScraper(env_path="../.env", log_dir="../logs", data_dir="../data", test_mode=False)
    asyncio.run(scraper.scrape_channels(channels, msg_limit=1000))
    return "Scraping completed"


@op
def load_raw_to_postgres():
    import subprocess
    # Run the notebook using papermill
    result = subprocess.run([
        "papermill",
        "notebooks/02_data_modelling.ipynb",
        "notebooks/02_data_modelling_output.ipynb"
    ], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Notebook execution failed: {result.stderr}")
    return "Raw data loaded to Postgres via notebook"

@op
def run_dbt_transformations():
    import subprocess
    # Run dbt transformations
    result = subprocess.run(["dbt", "run"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"dbt run failed: {result.stderr}")
    return "dbt transformations completed"

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

daily_schedule = ScheduleDefinition(
    job=telegram_medical_pipeline,
    cron_schedule="0 0 * * *",  # every day at midnight
)