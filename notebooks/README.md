# Notebooks Directory

This directory contains Jupyter notebooks documenting key stages of our data pipeline.

## Notebooks

1. **`01_datascrapping_loading.ipynb`** - Documents the Telegram data scraping and loading process using Telethon, including raw data ingestion into PostgreSQL
2. **`02_data_modelling.ipynb`** - Documents the data modeling and transformation process using dbt, including star schema creation and dimensional modeling
3. **`03_data_enrichment.ipynb`** - Documents the data enrichment process using YOLOv8 for image object detection and detection result integration

## Usage

To run these notebooks:
1. Ensure you have Jupyter installed: `pip install jupyter`
2. Install project dependencies: `pip install -r requirements.txt`
3. Start the notebook server: `jupyter notebook`
4. Open and execute the notebooks in numerical order (01 → 02 → 03)

## Notebook Dependencies

Each notebook requires:
- **01_datascrapping_loading.ipynb**: Telethon, psycopg2, python-dotenv
- **`02_data_modelling.ipynb`**: dbt-core, dbt-postgres, pandas
- **`03_data_enrichment.ipynb`**: ultralytics (YOLOv8), OpenCV, psycopg2

All dependencies are listed in the project's `requirements.txt` file.

## Database Connection

Before running notebooks, ensure your PostgreSQL database is configured and connection details are set in:
- Environment variables (for notebooks 1 & 3)
- `telegram_dbt/profiles.yml` (for notebook 2)