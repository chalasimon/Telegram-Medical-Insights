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
    # TODO: Add logic to load raw data to Postgres
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

daily_schedule = ScheduleDefinition(
    job=telegram_medical_pipeline,
    cron_schedule="0 0 * * *",  # every day at midnight
)