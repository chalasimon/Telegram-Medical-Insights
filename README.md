# Telegram Medical Insights
A modern data pipeline for analyzing Ethiopian medical businesses using public Telegram channel data.  
The project integrates scraping, ELT pipelines, dbt transformations, and enrichment with YOLO-based image object detection.  
This README provides an overview of the project, its features, and how to set it up and run it locally.
## Table of Contents

- [Project Overview](#project-overview)  
- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Project Structure](#project-structure)  
- [Running the Project](#running-the-project)  
- [Environment Variables](#environment-variables)  
- [Contributing](#contributing)  

---

## Project Overview

The project builds a **reproducible data platform** for collecting, storing, transforming, and analyzing data from Telegram channels.  

Key functionalities include:

- Extracting messages and images from public Telegram channels  
- Storing raw data in a data lake (`data/raw`)  
- Transforming data into a **dimensional star schema** in PostgreSQL using **dbt**  
- Enriching data using **YOLOv8 object detection**  
- Exposing an analytical API via **FastAPI**  
- Orchestrating the pipeline with **Dagster**  

---

## Features

- **Telegram scraping**: Collect messages, media, and metadata  
- **Data lake & warehouse**: Layered structure for reliable ELT  
- **Data modeling**: Star schema with fact & dimension tables  
- **Data enrichment**: YOLOv8 object detection on images  
- **Analytical API**: Query insights such as top products, channel activity, and search messages  
- **Reproducible environment**: Dockerized Python and PostgreSQL setup  

---

## Prerequisites
 
- Python 3.12+  
- Docker & Docker Compose  
- VSCode or any code editor  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/chalasimon/Telegram-Medical-Insights.git
cd Telegram-Medical-Insights
```
2. Create a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install dependencies:

```bash
pip install -r requirements.txt
```
4. Set up Docker:
```bash
docker-compose up -d
```
5. Initialize the PostgreSQL database:

```bash
docker exec -it telegram_medical psql -U postgres
```
6. Run dbt to set up the data warehouse:

```bash
dbt run
```
7. Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```
8. Start the Dagster UI:

```bash
dagster dev
```
---
## Project Structure

```
Telegram-Medical-Insights/
├── data/                  # Data lake and warehouse
│   ├── raw/               # Raw data from Telegram
│   ├── processed/         # Processed data for dbt
│   └── dbt/               # dbt models and configurations
├── api/                   # FastAPI application
│   ├── main.py            # FastAPI entry point
├── notebooks/              # Jupyter notebooks for analysis
├── telegram_dbt/          # DBT  models and configurations
│   ├── models/            # dbt models
│   │   ├── marts/         # Fact and dimension tables
│   │   └── staging/       # Staging models
│   ├── dbt_project.yml    # dbt project configuration
│   └── profiles.yml       # dbt profiles configuration
├── dagster/               # Dagster configurations
│   ├── jobs/              # Dagster jobs
├── docs/                   # Documentation
├── screenshots/           # Screenshots for documentation
├── .gitignore
└── src/                   # Source code
└── tests/                 # Unit tests
└── requirements.txt       # Python dependencies
``` 
---
## Running the Project
To run the project, follow these steps:
1. Ensure Docker is running and the containers are up with `docker-compose up -d`.
2. Activate the Python virtual environment.
3. Run the FastAPI server with `uvicorn app.main:app --reload`.
4. Access the API at `http://localhost:8000/docs` for Swagger UI.
5. Open the Dagster UI at `http://localhost:3000` to monitor and
manage the data pipeline.
## Environment Variables
Create a `.env` file in the root directory with the following variables:
```plaintext
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash

POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=telegram_insights
```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear messages.
4. Push your branch to your forked repository.
5. Create a pull request to the main repository.
6. Ensure your code passes all tests and adheres to the project's coding standards.
7. Add documentation for any new features or changes.
## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details