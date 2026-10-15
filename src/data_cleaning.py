"""
Nome:      data_cleaning.py
Descrição: Executa a limpeza dos dados justificada no notebook data_cleaning_rationale. As seções nos
           comentários correspondem às seções no notebook.
"""

import numpy as np
import pandas as pd
from data_loading import load_data



# 1. Valores inválidos e parsing de colunas
# --------------------------------------------------------------------------------------------------------------

num_cols = [
    'ano', 'vagas_ps', 'inscritos_ps', 'aprovados_ps', 'ingressantes_ps', 'vagas_sisu',
    'ingressantes_sisu', 'ingressantes_provar', 'ingressantes_outros', 'matriculados',
    'evadidos', 'concluintes', 'rel_cand_vaga'
]

def fix_invalid_data(df):
    def repl_comma(val):
        val_str = str(val)
        if val_str != '\\N':
            return val_str.replace(',', '.')
        
        return val_str

    for col_name in num_cols:
        col_vals = df[col_name].values
        new_vals = list(map(repl_comma, col_vals))
        df[col_name] = pd.to_numeric(pd.Series(new_vals), errors='coerce')

    # Apenas colunas de números inteiros (todas exceto rel_cand_vaga)
    for col_name in num_cols[:len(num_cols)-1]:
        df[col_name] = df[col_name].round().astype('Int64')

    return df



# 2. Manipulação de colunas
# --------------------------------------------------------------------------------------------------------------

def manipulates_cols(df):
    cols_drop = ['vagas_ps', 'inscritos_ps', 'aprovados_ps', 'rel_cand_vaga', 'vagas_sisu']

    return df.drop(columns=cols_drop)



# 3. Valores nulos
# --------------------------------------------------------------------------------------------------------------

def drop_na(df):
    return df.dropna()



# 4. Colunas categóricas
# --------------------------------------------------------------------------------------------------------------

def clean_cat_names(df):
    df['curso'] = df['curso'].str.replace({
        '(Parfor)':                       '',
        '(ParFor)':                       '',
        '- Curitiba':                     '',
        '- Bacharelado':                  '',
        '- Licenciatura':                 '',
        '- Palotina':                     '',
        '(Diurno)':                       '',
        '(Noturno)':                      '',
        '(Toledo)':                       '',
        'Inglês ou Portugês/Inglês':      'Inglês',
        'Português e Inglês':             'Inglês',
        'Português e Francês':            'Francês',
        'Português e Japonês':            'Japonês',
        'Português e Polonês':            'Polonês',
        'Português e Espanhol':           'Espanhol',
        'Espanhol ou Português/Espanhol': 'Espanhol',
        'Português e Alemão':             'Alemão',
        'Português e Italiano':           'Italiano',
        'Italiano ou Português/Italiano': 'Italiano',
    }).str.strip()

    df['setor'] = df['setor'].str.replace({
        'SETOR DE ARTES COMUNICAÇÃO E DESIGN': 'Artes, Comunicação e Design',
        'Setor':                               '',
        ' de':                                 '',
        '.':                                   ',',
        'Centro':                              '',
        'Toledo':                              'Ciências da Saúde', # Justificar
        'Jandaia':                             'Desconhecido', # Justificar
        'Litoral':                             'Desconhecido',
        'Palotina':                            'Desconhecido'
    }).str.strip()

    return df

def clean_missing_courses(df):
    cats = df['curso'].value_counts().index

    for cat in cats:
        for year in range(2018, 2026):
            cat_rows = df['curso'] == cat

            if len(df[cat_rows & (df['ano'] == year)]) == 0:
                df.drop(df[cat_rows].index, inplace=True)
                break

    return df