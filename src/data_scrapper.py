import os
import json
import csv
import time
import asyncio
import logging
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telethon import TelegramClient
from tqdm.asyncio import tqdm_asyncio  # Async version of tqdm


class TelegramScraper:
    def __init__(self, env_path="../.env", log_dir="../logs", data_dir="../data", test_mode=False):
        # Load environment variables
        load_dotenv(env_path)
        self.api_id = os.getenv("TG_API_ID")
        self.api_hash = os.getenv("TG_API_HASH")
        if not self.api_id or not self.api_hash:
            raise ValueError("Missing Telegram API credentials in .env")
        
        self.test_mode = test_mode

        # Logging setup
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "scraper.log")
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
        )

        # Directories
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw" / "telegram_messages"
        self.image_dir = self.data_dir / "images"
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.image_dir, exist_ok=True)

        # Telegram client
        self.session_path = Path("../scraper/scraping_session")
        os.makedirs(self.session_path.parent, exist_ok=True)
        self.client = TelegramClient(str(self.session_path), self.api_id, self.api_hash)

    async def scrape_channel(self, channel_username, msg_limit=1000):
        start_time = time.time()
        today_str = datetime.today().strftime("%Y-%m-%d")
        output_dir = self.raw_dir / today_str
        os.makedirs(output_dir, exist_ok=True)
        
        json_path = output_dir / f"{channel_username[1:]}.json"
        csv_path = output_dir / f"{channel_username[1:]}.csv"

        if json_path.exists() and csv_path.exists():
            logging.info(f"Skipped (already exists): {channel_username}")
            print(f"{channel_username} already scraped — skipping.")
            return

        logging.info(f"Starting scrape: {channel_username}")
        print(f"Scraping from {channel_username} ...")

        messages = []

        if self.test_mode:
            for i in range(1, 6):
                messages.append({
                    "channel_title": f"Mock {channel_username[1:]}",
                    "channel_username": channel_username,
                    "id": 1000 + i,
                    "text": f"Mock message #{i}",
                    "date": (datetime.now() - timedelta(minutes=i*5)).isoformat(),
                    "views": i*10,
                    "media_type": "document" if i == 3 else "photo" if i % 2 == 0 else None,
                    "media_path": None if i % 2 == 0 else f"/mock/path/{channel_username[1:]}_{i}.jpg"
                })
        else:
            entity = await self.client.get_entity(channel_username)
            channel_title = entity.title
            async for msg in tqdm_asyncio(
                self.client.iter_messages(entity, limit=msg_limit), 
                total=msg_limit, 
                desc=f"Scraping {channel_username}"
            ):
                msg_dict = {
                    "channel_title": channel_title,
                    "channel_username": channel_username,
                    "id": msg.id,
                    "text": msg.message,
                    "date": msg.date.isoformat() if msg.date else None,
                    "views": msg.views or 0,
                    "media_type": None,
                    "media_path": None
                }

                if msg.media and hasattr(msg.media, "photo"):
                    msg_dict["media_type"] = "photo"
                    image_path = self.image_dir / f"{channel_username[1:]}_{msg.id}.jpg"
                    os.makedirs(image_path.parent, exist_ok=True)
                    await self.client.download_media(msg, image_path)
                    msg_dict["media_path"] = str(image_path)

                elif msg.media and hasattr(msg.media, "document"):
                    msg_dict["media_type"] = "document"

                messages.append(msg_dict)

        # Save JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)

        # Save CSV
        if messages:
            with open(csv_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=messages[0].keys())
                writer.writeheader()
                writer.writerows(messages)

        duration = time.time() - start_time
        logging.info(f"{channel_username} scraped in {duration:.2f} sec. {len(messages)} messages saved.")
        print(f"{channel_username} scraped in {duration:.2f} sec. Messages saved to {json_path} and {csv_path}")

    async def scrape_channels(self, channels, msg_limit=1000):
        if not self.test_mode:
            await self.client.start()
        for channel in channels:
            try:
                await self.scrape_channel(channel, msg_limit)
            except Exception as e:
                logging.error(f"Error scraping {channel}: {e}")
                print(f"Skipping {channel} due to error: {e}")
