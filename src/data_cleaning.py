import numpy as np
import pandas as pd

from src.data_loading import load_data

df = load_data()

# 1. Dados inválidos e parsing das colunas

def fix_invalid_data():
    int_cols = ['ano', 'vagas_ps', 'inscritos_ps', 'aprovados_ps', 'ingressantes_ps', 'vagas_sisu',
                'ingressantes_sisu', 'ingressantes_provar', 'ingressantes_outros', 'matriculados_ano',
                'evadidos', 'concluintes']
    num_cols = int_cols + ['rel_cand_vaga']

    def repl_comma(val):
        val_str = str(val)
        if val_str != '\\N':
            return val_str.replace(',', '.')
        
        return val_str

    for col_name in num_cols:
        col_vals = df[col_name].values
        new_vals = list(map(repl_comma, col_vals))
        df[col_name] = pd.to_numeric(pd.Series(new_vals), errors='coerce')

    for col_name in int_cols:
        df[col_name] = df[col_name].round().astype('Int64')