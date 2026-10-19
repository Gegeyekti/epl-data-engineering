# EPL Data Engineering Pipeline

An end-to-end ETL project that processes English Premier League (EPL) match data using Python and PostgreSQL.

This project focuses on building a foundational data engineering workflow: extracting raw data, transforming it into a structured format, and loading it into a relational database for further analysis.

## Project Overview

Football match datasets contain valuable information about match results, goals, shots, corners, and cards. However, raw CSV files often need to be cleaned and structured before they can be used effectively.

This project demonstrates how raw EPL match data can be processed through an ETL pipeline and stored in PostgreSQL, providing a foundation for SQL-based analysis and future data visualization.

## Objectives

- Build an ETL pipeline using Python.
- Extract EPL match data from CSV files.
- Clean and transform data using Pandas.
- Store structured match data in PostgreSQL.
- Design relational tables for teams and matches.
- Practice SQL queries for football statistics.
- Learn environment configuration and database integration.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | ETL scripting |
| Pandas | Data cleaning and transformation |
| PostgreSQL | Relational database |
| psycopg2 | Python–PostgreSQL connection |
| python-dotenv | Environment variable management |
| DBeaver | Database management and SQL execution |
| Git & GitHub | Version control and project documentation |

## Architecture

```text
Football-Data.co.uk
        |
        v
   Extract (Python)
        |
        v
    Raw CSV File
        |
        v
  Transform (Pandas)
        |
        v
   Cleaned CSV File
        |
        v
    Load (Python)
        |
        v
     PostgreSQL
      /      \
   teams    matches
        |
        v
     SQL Analysis
```

When automatic downloading is unavailable, the extraction step can use an existing local CSV file.

## Data Source

- **Provider:** [Football-Data.co.uk](https://www.football-data.co.uk/)
- **Competition:** English Premier League
- **Season configured:** 2026/2027
- **Source file:** `E0.csv`

The dataset contains match results and selected match statistics. Data availability depends on the source provider's publication schedule.

## ETL Workflow

### 1. Extract

Script: `src/extract.py`

- Retrieves the source CSV when the website is reachable.
- Saves the raw dataset to `data/E0.csv`.
- Uses the existing local CSV as a fallback when automatic extraction fails.

### 2. Transform

Script: `src/transform.py`

- Selects relevant match and statistical columns.
- Converts dates and numerical fields to appropriate data types.
- Prepares the cleaned dataset for database loading.
- Saves the output to `data/E0_clean.csv`.

### 3. Load

Script: `src/load.py`

- Connects Python to PostgreSQL.
- Stores unique team records in the `teams` table.
- Loads match results and statistics into the `matches` table.
- Uses team identifiers to establish relationships between teams and matches.

## Database Design

The database contains two main tables:

### `teams`

Stores unique football team records.

| Column | Description |
|---|---|
| `team_id` | Primary key |
| `team_name` | Unique team name |

### `matches`

Stores match results and statistics.

| Column | Description |
|---|---|
| `match_id` | Match identifier |
| `match_date` | Match date |
| `home_team_id` | Home team foreign key |
| `away_team_id` | Away team foreign key |
| `home_score` | Home team full-time goals |
| `away_score` | Away team full-time goals |
| `full_time_result` | Full-time result |
| `half_time_home_score` | Home team half-time goals |
| `half_time_away_score` | Away team half-time goals |

Additional columns store match time, referee information, shots, shots on target, corners, and cards.

## Data Quality

The transformation process prepares raw match data for structured storage.

Data quality checks to implement or verify include:

- Checking missing values.
- Validating column data types.
- Detecting duplicate matches.
- Checking consistency between scores and match results.
- Verifying team references and database relationships.

Only checks that are implemented and tested should be considered completed features.

## Example SQL Analysis

The loaded data can be queried to answer football-related questions.

### Total matches

```sql
SELECT COUNT(*) AS total_matches
FROM matches;
```

### Total goals scored

```sql
SELECT
    SUM(home_score + away_score) AS total_goals
FROM matches;
```

### Match results

```sql
SELECT
    m.match_date,
    ht.team_name AS home_team,
    at.team_name AS away_team,
    m.home_score,
    m.away_score,
    m.full_time_result
FROM matches m
JOIN teams ht
    ON m.home_team_id = ht.team_id
JOIN teams at
    ON m.away_team_id = at.team_id
ORDER BY m.match_date;
```

## Getting Started

### Prerequisites

- Python 3.11 or a compatible Python version.
- PostgreSQL.
- Git.
- DBeaver (optional, for database inspection).

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd epl-data-engineering
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root based on `.env.example`.

```dotenv
EPL_CSV_URL=https://www.football-data.co.uk/mmz4281/2627/E0.csv

DB_HOST=localhost
DB_PORT=5432
DB_NAME=epl_database
DB_USER=postgres
DB_PASSWORD=your_password_here
```

Use your own local database credentials. Never commit the actual `.env` file.

### 5. Prepare the database

Create the `epl_database` database and the required `teams` and `matches` tables before running the load script.

### 6. Run the ETL pipeline

Run each script from the project root in this order:

```bash
python src/extract.py
python src/transform.py
python src/load.py
```

If extraction cannot reach the source website, ensure a valid local `data/E0.csv` file is available.

## Project Structure

```text
epl-data-engineering/
├── data/
│   └── .gitkeep
├── src/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── sql/
│   └── queries.sql
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

CSV files, local environment variables, and virtual environment files are excluded from version control.

## Challenges and Lessons Learned

This project provides hands-on practice with:

- Handling CSV datasets and data type conversion.
- Connecting Python scripts to PostgreSQL.
- Designing relationships between teams and matches.
- Managing environment variables and database credentials.
- Troubleshooting network connectivity and data loading errors.

## Future Improvements

- Implement more comprehensive data quality checks.
- Make database loading safely repeatable without duplicate matches.
- Automate data extraction and scheduled pipeline execution.
- Add logging and error handling.
- Build a football statistics dashboard.
- Explore workflow orchestration tools.

## Disclaimer

This project is intended for educational and portfolio purposes. Match data is sourced from [Football-Data.co.uk](https://www.football-data.co.uk/). Please refer to the provider's terms and data usage guidance.
