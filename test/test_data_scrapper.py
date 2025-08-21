import pytest
import asyncio
from src.data_scrapper import TelegramScraper
from datetime import datetime

@pytest.mark.asyncio
async def test_scrape_channel_mock(tmp_path):
    scraper = TelegramScraper(
        env_path="tests/.env",
        log_dir=tmp_path,
        data_dir=tmp_path,
        test_mode=True
    )
    await scraper.scrape_channel("@mockchannel", msg_limit=5)
    today_str = datetime.today().strftime("%Y-%m-%d")
    output_dir = tmp_path / "raw" / "telegram_messages" / today_str
    json_path = output_dir / "mockchannel.json"
    csv_path = output_dir / "mockchannel.csv"
    print("JSON path:", json_path)
    print("CSV path:", csv_path)
    assert json_path.exists(), f"JSON file not found: {json_path}"
    assert csv_path.exists(), f"CSV file not found: {csv_path}"