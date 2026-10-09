import numpy as np
import pandas as pd
from io import StringIO

PATH = '../data/raw/graduacao_resumo_cursos_20{0:d}.csv'

# Encodings e separadores dos CSVs dos anos correspondentes
CONFIG = {
    18: ('latin1', ';'),
    19: ('latin1', ';'),
    20: ('latin1', ';'),
    21: ('latin1', ';'),
    22: ('latin1', ';'),
    23: ('latin1', ';'),
    24: ('utf-8',  ','),
    25: ('utf-8',  ','),
    26: ('utf-8',  ',')
}

csv_path = lambda year: PATH.format(year)

# Os nomes das colunas de alguns CSVs possuem particularidades

def standardize_columns(columns):
    return list(map(lambda column: (
        column.lower()
            .replace('nome_', '')
            .replace('curso_', '')
            .replace('_total', '')
            .replace('\"', '')
            .replace('\n', '')
    ), columns))

# As colunas do CSV de 2018 se parecem com a maioria dos outros, então é utilizada como padrão

def std_columns():
    with open(csv_path(18), 'r', encoding=CONFIG[18][0]) as f:
        cols_line = f.readline().split(';')
        return standardize_columns(cols_line)

# O ano 2024 é o mais problemático:
# - apresenta caracteres corrompidos (latin1)
# - aspas imprecisas, gerando shifting nas colunas e valores nulos
# - colunas extras que apenas os anos 2020 e 2021 também possuem (isto é resolvido na
#   função create_special_dfs)

def fix_csv_24():
    with open(csv_path(24), 'r') as f:
        csv_txt = (
            f.read()
                .replace('\"NOME_CURSO', '\"NOME_CURSO\"')
                .replace('\"\"\"', '\"')
                .replace('\"\"', '\"')
                .replace('\ufeff', '') # Caractere não codificado por latin1
                .encode('latin1').decode('utf-8')
        )

        cols_line_len = len(csv_txt.split('\n')[0])
        csv_txt = (
            csv_txt[:cols_line_len] +
            csv_txt[cols_line_len:].replace('\"\n', '\n').replace('\n\"', '\n')
        )

        return csv_txt

def create_special_dfs(years, sources):
    dfs = []
    
    for year, src in zip(years, sources):
        df = pd.read_csv(src, encoding=CONFIG[year][0], sep=CONFIG[year][1])

        if year == 26:
            # Neste ano não há a coluna de concluintes, mas para a concatenação ela é criada
            # e preenchida com valor nulo

            df['concluintes'] = np.nan
            df.columns = std_columns()
        else:
            df.columns = standardize_columns(df.columns)
            df = df[std_columns()] # Elimina colunas extras
        dfs.append(df)

    return dfs

def create_dfs():
    special_years = [20, 21, 24, 26] # Anos com tratamento especial

    dfs = [
        pd.read_csv(
            csv_path(year),
            encoding=CONFIG[year][0],
            sep=CONFIG[year][1],
            names=std_columns(),
            header=0
        ) for year in range(min(CONFIG), max(CONFIG)+1) if year not in special_years
    ]

    special_csv_sources = [
        csv_path(special_years[0]),
        csv_path(special_years[1]),
        StringIO(fix_csv_24()),
        csv_path(special_years[3])
    ]
    dfs.extend(create_special_dfs(special_years, special_csv_sources))

    return dfs

def validate_data_len(df, dfs):
    len_expected = 0
    for dataf in dfs:
        assert (dataf.columns == std_columns()).all()
        len_expected += len(dataf)
        
    assert len(df) == len_expected

def load_data():
    dfs = create_dfs()
    df = pd.concat(dfs, ignore_index=True)
    validate_data_len(df, dfs)

    return df