import pandas as pd

file_path = "data/E0.csv"
df = pd.read_csv(file_path)

columns = [
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
    "AR"
]

df_clean = df[columns]

df_clean["Date"] = pd.to_datetime(
    df_clean["Date"],
    format="%d/%m/%Y"
)

df_clean["MatchDateTime"] = pd.to_datetime(
    df_clean["Date"].astype(str) + " " + df_clean["Time"]
)

df_clean.insert(0, "match_id", range(1, len(df_clean) +1))

output_path = "data/E0_clean.csv"

df_clean.to_csv(output_path, index=False)

print(f"\nData berhasil disimpan ke: {output_path}")

print(df_clean.head())
print(df_clean.shape)

print("\nJumlah data kosong:")
print(df_clean.isnull().sum())

print("\nTipe data:")
print(df_clean.dtypes)

print("\nTipe data setelah transformasi:")
print(df_clean.dtypes)