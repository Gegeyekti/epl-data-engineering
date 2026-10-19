import os
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_values

PROJECT_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_DIR / "data" / "E0_clean.csv"

load_dotenv(PROJECT_DIR / ".env")

def get_connection():
    """Membuat koneksi ke PostgreSQL."""
    required_vars = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD"
    ]
    
    missing  = [key for key in required_vars if not os.getenv(key)]
    if missing:
        raise ValueError(
            f"Konfigurasi .env belum lengkap: {', '.join(missing)}"
        )
    
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    
def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"File CSV tidak ditemukan: {CSV_PATH}"
        )
    
    df = pd.read_csv(CSV_PATH)
    
    required_columns = [
        "match_id",
        "Date",
        "Time",
        "HomeTeam",
        "AwayTeam",
        "FTHG",
        "FTAG",
        "FTR",
        "HTHG",
        "HTAG",
        "HTR",
        "Referee",
        "HS",
        "AS",
        "HST",
        "AST",
        "HC",
        "AC",
        "HY",
        "AY",
        "HR",
        "AR",
        "MatchDateTime",
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]
    if missing_columns:
        raise ValueError(
            f"Kolom CSV tidak ditemukan: {missing_columns}"
        )

    df["Date"] = pd.to_datetime(
        df["Date"],  errors = "raise"
    ).dt.date

    df["Time"] = pd.to_datetime(
        df["Time"].astype(str),format="%H:%M", errors="raise"
    ).dt.time

    df["MatchDateTime"] = pd.to_datetime(
        df["MatchDateTime"], errors="raise")

    team_names = sorted(
        set(df["HomeTeam"].dropna())
        | set(df["AwayTeam"].dropna())
    )
    
    if df["HomeTeam"].isna().any() or df["AwayTeam"].isna().any():
        raise ValueError("Ada nama tim yang kosong di CSV.")
    
    conn = get_connection()
    
    try:
        with conn:
            with conn.cursor() as cursor:
                execute_values(
                    cursor,
                    """
                    INSERT INTO teams (team_name)
                    VALUES %s
                    ON CONFLICT (team_name) DO NOTHING
                    """,
                    [(name,) for name in team_names],
                )
                
                cursor.execute(
                    "SELECT team_id, team_name FROM teams"
                )
                team_ids = {
                    name: team_id
                    for team_id, name in cursor.fetchall()
                }
                
                columns = [
                    "match_id",
                    "match_date",
                    "match_time",
                    "home_team_id",
                    "away_team_id",
                    "home_score",
                    "away_score",
                    "full_time_result",
                    "half_time_home_score",
                    "half_time_away_score",
                    "half_time_result",
                    "referee",
                    "home_shots",
                    "away_shots",
                    "home_shots_on_target",
                    "away_shots_on_target",
                    "home_corners",
                    "away_corners",
                    "home_yellow_cards",
                    "away_yellow_cards",
                    "home_red_cards",
                    "away_red_cards",
                    "match_datetime",
                ]
                
                values = []
                for row in df.itertuples(index=False):
                    values.append((
                        int(row.match_id),
                        row.Date,
                        row.Time,
                        team_ids[row.HomeTeam],
                        team_ids[row.AwayTeam],
                        int(row.FTHG),
                        int(row.FTAG),
                        row.FTR,
                        int(row.HTHG),
                        int(row.HTAG),
                        row.HTR,
                        row.Referee,
                        int(row.HS),
                        int(row.AS),
                        int(row.HST),
                        int(row.AST),
                        int(row.HC),
                        int(row.AC),
                        int(row.HY),
                        int(row.AY),
                        int(row.HR),
                        int(row.AR),
                        row.MatchDateTime.to_pydatetime(),
                    ))
                
                query = f"""
                    INSERT INTO matches ({", ".join(columns)})
                    VALUES %s
                    ON CONFLICT (match_id) DO UPDATE SET
                        match_date = EXCLUDED.match_date,
                        match_time = EXCLUDED.match_time,
                        home_team_id = EXCLUDED.home_team_id,
                        away_team_id = EXCLUDED.away_team_id,
                        home_score = EXCLUDED.home_score,
                        away_score = EXCLUDED.away_score,
                        full_time_result = EXCLUDED.full_time_result,
                        half_time_home_score = EXCLUDED.half_time_home_score,
                        half_time_away_score = EXCLUDED.half_time_away_score,
                        half_time_result = EXCLUDED.half_time_result,
                        referee = EXCLUDED.referee,
                        home_shots = EXCLUDED.home_shots,
                        away_shots = EXCLUDED.away_shots,
                        home_shots_on_target = EXCLUDED.home_shots_on_target,
                        away_shots_on_target = EXCLUDED.away_shots_on_target,
                        home_corners = EXCLUDED.home_corners,
                        away_corners = EXCLUDED.away_corners,
                        home_yellow_cards = EXCLUDED.home_yellow_cards,
                        away_yellow_cards = EXCLUDED.away_yellow_cards,
                        home_red_cards = EXCLUDED.home_red_cards,
                        away_red_cards = EXCLUDED.away_red_cards,
                        match_datetime = EXCLUDED.match_datetime
                """
                
                execute_values(cursor, query, values)
                
                cursor.execute("SELECT COUNT(*) FROM teams")
                total_teams = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM matches")
                total_matches = cursor.fetchone()[0]
                
            print("Proses load selesai.")
            print(f"Jumlah tim di database: {total_teams}")
            print(f"Jumlah pertandingan di database: {total_matches}")

    finally:
        conn.close()
        
if __name__ == "__main__":
    main()                