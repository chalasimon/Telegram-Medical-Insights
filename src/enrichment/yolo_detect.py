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