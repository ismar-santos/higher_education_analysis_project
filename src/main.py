from pathlib import Path
from data_loading import load_data
from data_cleaning import clean_data

if __name__ == '__main__':
    df = load_data()
    clean_df, *_ = clean_data(df.copy())

    Path('data/interim').mkdir(parents=True, exist_ok=True)
    Path('data/processed').mkdir(parents=True, exist_ok=True)

    df.to_csv('data/interim/data_loaded.csv', index=False)
    clean_df.to_csv('data/processed/data_cleaned.csv', index=False)