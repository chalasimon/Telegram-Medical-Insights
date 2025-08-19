# import libraries
import os
import sys
import time
import logging
from pathlib import Path
from dotenv import load_dotenv

import psycopg2
from psycopg2.extras import execute_values
from ultralytics import YOLO
from PIL import Image

# ---- logging ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def select_images_to_process(conn, limit=None, rerun=False):
    """
    Returns rows: (message_id, image_path)
    - If rerun=False: only images/messages with NO detections yet.
    - If rerun=True: process all images with a file present (recompute).
    """
    with conn.cursor() as cur:
        if rerun:
            sql = """
            select id as message_id, media_path as image_path
            from raw.telegram_messages
            where media_path is not null
            """
        else:
            sql = """
            select m.id as message_id, m.media_path as image_path
            from raw.telegram_messages m
            where m.media_path is not null
              and not exists (
                    select 1 from raw.image_detections d
                    where d.message_id = m.id
                )
            """
        if limit:
            sql += " limit %s"
            cur.execute(sql, (limit,))
        else:
            cur.execute(sql)

        rows = cur.fetchall()
    # Filter to ones that actually exist on disk
    filtered = [(mid, ipath) for mid, ipath in rows if ipath and Path(ipath).exists()]
    missing  = len(rows) - len(filtered)
    if missing > 0:
        logging.warning(f"Skipping {missing} images that are missing on disk.")
    return filtered