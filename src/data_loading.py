import numpy as np
import pandas as pd

PATH = '../data/raw/graduacao_resumo_cursos_20{0:d}.csv'

# Encodings previamente identificados utilizando chardet
ENCODING_SEP_CONFIG = [
    (22, 'ISO-8859-1', ';'),
    (23, 'ISO-8859-1', ';'),
    (24, 'UTF-8-SIG',  ','),
    (25, 'utf-8',      ',')
]

def get_columns(path):
    with open(path.format(22), 'r', encoding='ISO-8859-1') as f:
        columns = f.readline().split(';')
        return list(map(str.lower, columns))

def create_dfs(path, encoding_sep_config):
    columns = get_columns(path)
    
    dfs = [
        pd.read_csv(
            path.format(year),
            encoding=encoding,
            sep=sep,
            names=columns,
            header=0
        ) for year, encoding, sep in encoding_sep_config
    ]

    df_26 = pd.read_csv(path.format(26))
    df_26['concluintes'] = np.nan
    df_26.columns = columns
    dfs.append(df_26)

    return dfs

def validate_data_len(path, df, dfs):
    len_expected = 0
    for dataf in dfs:
        assert (dataf.columns == get_columns(path)).all()
        len_expected += len(dataf)
        
    assert len(df) == len_expected

def load_data():
    dfs = create_dfs(PATH, ENCODING_SEP_CONFIG)
    df = pd.concat(dfs, ignore_index=True)
    validate_data_len(PATH, df, dfs)

    return df