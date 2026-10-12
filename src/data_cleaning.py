"""
Nome:      data_cleaning.py
Descrição: Executa a limpeza dos dados justificada no notebook data_cleaning_rationale. As seções nos
           comentários correspondem às seções no notebook.
"""

import numpy as np
import pandas as pd
from data_loading import load_data

df = load_data()



# 1. Valores inválidos e parsing de colunas

num_cols = [
    'ano', 'vagas_ps', 'inscritos_ps', 'aprovados_ps', 'ingressantes_ps', 'vagas_sisu',
    'ingressantes_sisu', 'ingressantes_provar', 'ingressantes_outros', 'matriculados',
    'evadidos', 'concluintes', 'rel_cand_vaga'
]

def fix_invalid_data():
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



# 2. Manipulação de colunas

def manipulates_cols():
    cols_drop = ['vagas_ps', 'rel_cand_vaga']
    df.drop(columns=cols_drop, inplace=True)



# 3. Valores nulos

def drop_na():
    cols = df.columns.difference(['concluintes'])
    df.dropna(subset=cols, inplace=True)