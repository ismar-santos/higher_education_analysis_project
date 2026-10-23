from pathlib import Path
from data_loading import load_data
from data_cleaning import clean_data

if __name__ == '__main__':
    df0 = load_data()
    df, *_ = clean_data(df0)

    Path('data/interim').mkdir(parents=True, exist_ok=True)
    Path('data/processed').mkdir(parents=True, exist_ok=True)

    df0.to_csv('data/interim/data_loaded.csv', index=False)
    df.to_csv('data/processed/data_cleaned.csv', index=False)