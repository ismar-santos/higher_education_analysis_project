"""
Nome:      data_cleaning.py
Descrição: Executa a limpeza dos dados justificada no notebook data_cleaning_rationale. As seções nos
           comentários correspondem às seções no notebook.
"""

import pandas as pd

def affected_data_calc(df0, df):
    rows_affected = df0.loc[~(df0 == df).all(axis=1).values]
    cols_affected = df0.columns[~(df0 == df).all().values]

    return len(rows_affected), len(cols_affected)



# 1. Valores inválidos e parsing de colunas
# --------------------------------------------------------------------------------------------------------------

num_cols = [
    'ano', 'vagas_ps', 'inscritos_ps', 'aprovados_ps', 'ingressantes_ps', 'vagas_sisu',
    'ingressantes_sisu', 'ingressantes_provar', 'ingressantes_outros', 'matriculados',
    'evadidos', 'concluintes', 'rel_cand_vaga'
]

def fix_invalid_data(df):
    df0 = df.copy()

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

    return df, affected_data_calc(df0, df)



# 2. Manipulação de colunas
# --------------------------------------------------------------------------------------------------------------

def manipulates_cols(df):
    cols_drop = ['vagas_ps', 'inscritos_ps', 'aprovados_ps', 'rel_cand_vaga', 'vagas_sisu']
    
    return df.drop(columns=cols_drop), (0, len(cols_drop))



# 3. Valores nulos
# --------------------------------------------------------------------------------------------------------------

def drop_na(df):
    rows_with_na = df[df.columns].isna().any(axis=1).values
    # cols_with_na = df[df.columns].isna().any().values

    return df.dropna(), (len(df.index[rows_with_na]), 0)



# 4. Colunas categóricas
# --------------------------------------------------------------------------------------------------------------

def clean_curso_names(df):
    df0 = df.copy()

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
        'Inglês ou Portugês/Inglês':      'Inglês', # Isto também elimina o erro de escrita "Portugês"
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

    return df, affected_data_calc(df0, df)

def clean_setor_names(df):
    df0 = df.copy()

    df['setor'] = df['setor'].str.replace({
        'SETOR DE ARTES COMUNICAÇÃO E DESIGN': 'Artes, Comunicação e Design',
        'Setor':                               '',
        ' de':                                 '',
        '.':                                   ',',
        'Centro':                              '',
        'Toledo':                              'Ciências da Saúde',
        'Jandaia':                             'Desconhecido',
        'Litoral':                             'Desconhecido',
        'Palotina':                            'Desconhecido'
    }).str.strip()

    return df, affected_data_calc(df0, df)

def clean_campus_names(df):
    df0 = df.copy()
    df['campus'] = df['campus'].str.replace('Campus', '').str.strip()

    return df, affected_data_calc(df0, df)

def clean_grau_names(df):
    df0 = df.copy()

    df.loc[df['grau'] == 'Licenciatura (Matemática)', 'curso'] = 'Matemática'
    df.loc[df['grau'] == 'Licenciatura (Física)', 'curso'] = 'Física'
    df.loc[df['grau'] == 'Licenciatura (Química)', 'curso'] = 'Química'

    df['grau'] = df['grau'].str.replace({
        'Licenciatura (Matemática)': 'Licenciatura',
        'Licenciatura (Física)': 'Licenciatura',
        'Licenciatura (Química)': 'Licenciatura'
    })

    df.loc[~df['grau'].isin([
        'Bacharelado',
        'Licenciatura',
        'Segunda Licenciatura',
        'Múltiplo',
        'Tecnológico'
    ]), 'grau'] = 'Desconhecido'

    return df, affected_data_calc(df0, df)



# 5. Colunas categóricas
# --------------------------------------------------------------------------------------------------------------

def clean_missing_courses(df):
    cats = df['curso'].value_counts().index
    affected_rows = 0

    for cat in cats:
        for year in range(2018, 2026):
            cat_rows = (df['curso'] == cat)

            if len(df[cat_rows & (df['ano'] == year)]) == 0:
                affected_rows += len(df[df['curso'] == cat])
                df = df.drop(df[cat_rows].index)
                break

    return df, (affected_rows, 0)



# 6. Cursos duplicados
# --------------------------------------------------------------------------------------------------------------

def del_duplicates(df):
    cols = ['curso', 'setor', 'campus', 'grau', 'turno', 'ano']
    keep_first = [
        'Ciências Exatas', 'Física', 'Música', 'Ciências',
        'Letras - Francês', 'Letras - Japonês', 'Letras - Polonês',
        'Letras - Espanhol', 'Administração'
    ]
    keep_last = 'Letras - Português'
    affected_rows = 0

    def del_exec(df, course, keep):
        cond = (
            df.duplicated(subset=cols, keep=keep) &
            (df['curso'] == course) &
            (df['grau'] != 'Desconhecido')
        )
        df = df[~cond]

        return df, cond.sum()

    for course in keep_first:
        df, aff_aux = del_exec(df, course, 'first')
        affected_rows += aff_aux
    df, aff_aux = del_exec(df, keep_last, 'last')
    affected_rows += aff_aux

    return df, (affected_rows, 0)



# Execução
# --------------------------------------------------------------------------------------------------------------

def clean_data(df):
    clean_ops = [
        fix_invalid_data,
        manipulates_cols,
        drop_na,
        clean_curso_names,
        clean_setor_names,
        clean_campus_names,
        clean_grau_names,
        clean_missing_courses,
        del_duplicates
    ]

    affs = []
    for func in clean_ops:
        df, aff = func(df)
        affs.append(aff)

    return (
        df,
        [aff[0] for aff in affs],
        [aff[1] for aff in affs]
    )